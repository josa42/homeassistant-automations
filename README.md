# Home Assistant Automations

Automation blueprints I use in my own Home Assistant setup.

Every blueprint can be installed with the import button below, or by pasting the
blueprint URL into **Settings → Automations & scenes → Blueprints → Import blueprint**.

## Blueprints

<!-- blueprints:start -->

### [Example Blueprint](blueprints/automation/example.yaml)

Placeholder blueprint used to validate the repository setup. Runs a user-defined set of actions whenever a sensor turns on, optionally after a delay.

[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/josa42/homeassistant-automations/blob/main/blueprints/automation/example.yaml)

### [Motion Light](blueprints/automation/motion-light.yaml)

Switch lights on when motion is detected and off again once every motion sensor has been clear for a while.

Turning on can be gated on ambient light, on a time window, and on a bypass entity. Turning off is only blocked by the bypass, so lights can never be stranded on by a lux reading or by the end of the time window.

Lights switched on by hand are also switched off once the room clears.

[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/josa42/homeassistant-automations/blob/main/blueprints/automation/motion-light.yaml)

<!-- blueprints:end -->

## Development

Blueprints live in `blueprints/<domain>/`. After adding or changing one, refresh the
list above and check the blueprint itself:

```sh
make readme    # regenerate the list above
make check     # lint, validate the blueprints, check the README is in sync
```

Both create a `.venv/` with the development dependencies on first run. Run `make help`
for all targets. CI runs `make check` on every push and pull request.
