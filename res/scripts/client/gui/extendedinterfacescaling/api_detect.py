_API = None


def detect_scaling_api():
    global _API
    if _API is not None:
        return _API

    from gui.shared.utils import graphics
    from account_helpers.settings_core.interfacescalemanager import (
        InterfaceScaleManager,
    )

    if hasattr(graphics, "_SCALES"):
        _API = "float"
    elif hasattr(InterfaceScaleManager, "getScaleByIndex"):
        _API = "index"
    else:
        _API = "unknown"

    return _API


def get_scaling_api():
    return detect_scaling_api()
