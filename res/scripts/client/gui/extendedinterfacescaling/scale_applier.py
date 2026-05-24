import GUI
from gui.shared import event_dispatcher
from gui.shared.utils import graphics
from gui.shared.utils.monitor_settings import g_monitorSettings
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore

from gui.extendedinterfacescaling.api_detect import get_scaling_api

_applying = False


def is_applying():
    return _applying


def _get_settings_core():
    return dependency.instance(ISettingsCore)


def _update_manager_state(manager, scale_float):
    prev = manager.get()
    if get_scaling_api() == "index":
        manager._InterfaceScaleManager__scaleValue = scale_float
    else:
        manager._InterfaceScaleManager__scaleValue = scale_float

    manager.onScaleChanged(scale_float)
    if prev != scale_float and hasattr(manager, "onScaleExactlyChanged"):
        manager.onScaleExactlyChanged(scale_float)


def apply_scale(scale_float):
    global _applying

    scale_float = float(scale_float)
    _applying = True
    try:
        width, height = GUI.screenResolution()[:2]
        event_dispatcher.changeAppResolution(width, height, scale_float)
        g_monitorSettings.setGlyphCache(scale_float)
        manager = _get_settings_core().interfaceScale
        _update_manager_state(manager, scale_float)
        graphics.onInterfaceScaleChanged(scale_float)
    finally:
        _applying = False
