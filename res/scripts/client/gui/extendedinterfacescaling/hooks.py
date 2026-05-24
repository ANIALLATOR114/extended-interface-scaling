from account_helpers.settings_core.interfacescalemanager import InterfaceScaleManager
from account_helpers.settings_core.options import InterfaceScaleSetting
from gui.extendedinterfacescaling import config
from gui.extendedinterfacescaling.override_utils import override
from gui.extendedinterfacescaling.scale_applier import apply_scale, is_applying

_installed = False


def _patched_change_scale(original, self, arg):
    if is_applying() or not config.is_enabled():
        return original(self, arg)
    apply_scale(config.get_scale())


def _patched_scale_changed(original, self):
    original(self)
    try:
        from gui.extendedinterfacescaling.mods_settings import on_screen_geometry_changed

        on_screen_geometry_changed()
    except ImportError:
        pass
    if is_applying() or not config.is_enabled():
        return
    apply_scale(config.get_scale())


def _patched_set_system_value(original, self, value):
    original(self, value)
    if is_applying() or not config.is_enabled():
        return
    apply_scale(config.get_scale())


def install():
    global _installed
    if _installed:
        return

    override(InterfaceScaleManager, "changeScale", _patched_change_scale)
    override(InterfaceScaleManager, "scaleChanged", _patched_scale_changed)
    override(InterfaceScaleSetting, "setSystemValue", _patched_set_system_value)
    _installed = True

    if config.is_enabled():
        apply_scale(config.get_scale())


def uninstall():
    global _installed
    _installed = False
