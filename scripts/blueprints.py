#!/usr/bin/env python3
"""Validate the blueprints in this repo and keep the README list in sync."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BLUEPRINT_DIR = ROOT / "blueprints"
README = ROOT / "README.md"
REPO_URL = "https://github.com/josa42/homeassistant-automations"
BRANCH = "main"
START = "<!-- blueprints:start -->"
END = "<!-- blueprints:end -->"

REQUIRED_META = ("name", "description", "domain", "source_url")


class Input:
    """Marker for the !input tag, so blueprints can be parsed as plain YAML."""

    def __init__(self, key: str) -> None:
        self.key = key


class Loader(yaml.SafeLoader):
    pass


Loader.add_constructor("!input", lambda loader, node: Input(loader.construct_scalar(node)))


def blueprints() -> list[Path]:
    return sorted(BLUEPRINT_DIR.rglob("*.yaml"))


def load(path: Path) -> dict:
    with path.open() as fh:
        return yaml.load(fh, Loader=Loader)


def source_url(path: Path) -> str:
    return f"{REPO_URL}/blob/{BRANCH}/{path.relative_to(ROOT).as_posix()}"


def import_url(path: Path) -> str:
    return (
        "https://my.home-assistant.io/redirect/blueprint_import/"
        f"?blueprint_url={source_url(path)}"
    )


def input_keys(inputs: dict) -> set[str]:
    """Collect input keys, descending into sections."""
    keys: set[str] = set()
    for key, value in (inputs or {}).items():
        if isinstance(value, dict) and "input" in value:
            keys |= input_keys(value["input"])
        else:
            keys.add(key)
    return keys


def leaf_inputs(inputs: dict) -> dict[str, dict]:
    leaves: dict[str, dict] = {}
    for key, value in (inputs or {}).items():
        if isinstance(value, dict) and "input" in value:
            leaves.update(leaf_inputs(value["input"]))
        else:
            leaves[key] = value or {}
    return leaves


def used_inputs(node: object) -> set[str]:
    if isinstance(node, Input):
        return {node.key}
    if isinstance(node, dict):
        return set().union(*(used_inputs(v) for v in node.values())) if node else set()
    if isinstance(node, list):
        return set().union(*(used_inputs(v) for v in node)) if node else set()
    return set()


def validate() -> list[str]:
    errors: list[str] = []
    files = blueprints()
    if not files:
        return [f"no blueprints found in {BLUEPRINT_DIR.relative_to(ROOT)}/"]

    for path in files:
        rel = path.relative_to(ROOT)
        try:
            data = load(path)
        except yaml.YAMLError as exc:
            errors.append(f"{rel}: invalid YAML: {exc}")
            continue

        meta = (data or {}).get("blueprint")
        if not isinstance(meta, dict):
            errors.append(f"{rel}: missing top-level 'blueprint:' mapping")
            continue

        for key in REQUIRED_META:
            if not meta.get(key):
                errors.append(f"{rel}: blueprint.{key} is required")

        domain = meta.get("domain")
        expected_domain = path.relative_to(BLUEPRINT_DIR).parts[0]
        if domain and domain != expected_domain:
            errors.append(
                f"{rel}: blueprint.domain is '{domain}' but the file lives in "
                f"blueprints/{expected_domain}/"
            )

        if meta.get("source_url") and meta["source_url"] != source_url(path):
            errors.append(f"{rel}: blueprint.source_url should be {source_url(path)}")

        inputs = meta.get("input") or {}
        for key, spec in leaf_inputs(inputs).items():
            if not isinstance(spec, dict) or "selector" not in spec:
                errors.append(f"{rel}: input '{key}' has no selector")

        body = {k: v for k, v in data.items() if k != "blueprint"}
        unknown = used_inputs(body) - input_keys(inputs)
        for key in sorted(unknown):
            errors.append(f"{rel}: '!input {key}' has no matching input")

    return errors


def table() -> str:
    rows = [
        "| Blueprint | Description | |",
        "| --- | --- | --- |",
    ]
    for path in blueprints():
        meta = load(path)["blueprint"]
        description = " ".join(str(meta.get("description", "")).split())
        badge = (
            "[![Import Blueprint]"
            f"(https://my.home-assistant.io/badges/blueprint_import.svg)]({import_url(path)})"
        )
        rows.append(f"| [{meta['name']}]({path.relative_to(ROOT).as_posix()}) | {description} | {badge} |")
    return "\n".join(rows)


def render(check: bool) -> list[str]:
    content = README.read_text()
    pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    if not pattern.search(content):
        return [f"README.md: missing '{START}' / '{END}' markers"]

    block = f"{START}\n\n{table()}\n\n{END}"
    updated = pattern.sub(lambda _: block, content)
    if updated == content:
        return []
    if check:
        return ["README.md is out of date, run: python3 scripts/blueprints.py readme"]
    README.write_text(updated)
    print("README.md updated")
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="validate all blueprints")
    readme = sub.add_parser("readme", help="regenerate the blueprint list in README.md")
    readme.add_argument("--check", action="store_true", help="fail instead of writing")
    args = parser.parse_args()

    errors = validate() if args.command == "validate" else render(args.check)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
