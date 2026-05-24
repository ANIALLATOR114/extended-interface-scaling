import json
import os

CONFIG_DIR = "mods/configs/ANIALLATOR.extended_interface_scaling"
CONFIG_FILE = CONFIG_DIR + "/config.json"

DEFAULTS = {
    "scale": 1.0,
    "enabled": True,
}

_scale = DEFAULTS["scale"]
_enabled = DEFAULTS["enabled"]


def load():
    global _scale, _enabled

    if not os.path.isfile(CONFIG_FILE):
        save()
        return

    try:
        with open(CONFIG_FILE, "r") as handle:
            data = json.load(handle)
    except (IOError, ValueError):
        data = {}

    _scale = float(data.get("scale", DEFAULTS["scale"]))
    _scale = max(0.5, min(2.0, _scale))
    _enabled = bool(data.get("enabled", DEFAULTS["enabled"]))


def save():
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    data = {
        "scale": _scale,
        "enabled": _enabled,
    }

    with open(CONFIG_FILE, "w") as handle:
        json.dump(data, handle, indent=2)


def get_scale():
    return _scale


def set_scale(value):
    global _scale
    _scale = float(value)


def is_enabled():
    return _enabled


def set_enabled(value):
    global _enabled
    _enabled = bool(value)


def apply_values(scale=None, enabled=None):
    global _scale, _enabled

    if scale is not None:
        _scale = float(scale)
    if enabled is not None:
        _enabled = bool(enabled)

    save()
