# Home Assistant Automations

Automation blueprints I use in my own Home Assistant setup.

Every blueprint can be installed with the import button below, or by pasting the
blueprint URL into **Settings → Automations & scenes → Blueprints → Import blueprint**.

## Blueprints

<!-- blueprints:start -->

| Blueprint | Description | |
| --- | --- | --- |
| [Example Blueprint](blueprints/automation/example.yaml) | Placeholder blueprint used to validate the repository setup. Runs a user-defined set of actions whenever a sensor turns on, optionally after a delay. | [![Add blueprint to your Home Assistant instance.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint=https%3A%2F%2Fraw.githubusercontent.com%2Fjosa42%2Fhomeassistant-automations%2Fmain%2Fblueprints%2Fautomation%2Fexample.yaml) |

<!-- blueprints:end -->

## Development

Blueprints live in `blueprints/<domain>/`. After adding or changing one, refresh the
list above and check the blueprint itself:

```sh
pip install -r requirements-dev.txt
python3 scripts/blueprints.py readme
python3 scripts/blueprints.py validate
yamllint .
```

CI runs the same checks on every push and pull request.
