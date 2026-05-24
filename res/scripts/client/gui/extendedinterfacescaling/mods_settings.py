from debug_utils import LOG_NOTE

MOD_LINKAGE = "extended_interface_scaling"
SETTINGS_VERSION = 8

MIN_UI_SCALE = 0.5
MAX_UI_SCALE = 2.0

REFERENCE_SCALES = (0.5, 0.75, 0.9, 1.0, 1.1, 1.25, 1.5, 1.75, 2.0)

REFERENCE_TOOLTIP = (
    "{HEADER}Scaling reference{/HEADER}"
    "{BODY}This reference shows what the scaling multiplier will cause "
    "the UI to behave like in terms of resolution. With this mod the "
    "sharpness of the UI will remain as perfect as your native resolution, "
    "despite being \"scaled\" up or down to the reference resolution size.{/BODY}"
)


def _clamp_scale(scale):
    return max(MIN_UI_SCALE, min(MAX_UI_SCALE, float(scale)))


def _parse_scale(value, default=1.0):
    try:
        return _clamp_scale(float(value))
    except (TypeError, ValueError):
        return _clamp_scale(default)


HINT_TOOLTIP = (
    "{HEADER}In-game interface scaling{/HEADER}"
    "{BODY}When this mod is enabled, it controls interface scale. "
    "The in-game Options > Interface Scaling setting is overridden.{/BODY}"
)


def _screen_info():
    from gui.extendedinterfacescaling.display_utils import (
        get_current_screen_size,
        get_native_screen_resolution,
    )

    try:
        from gui.shared.utils.monitor_settings import g_monitorSettings

        monitor = g_monitorSettings.currentMonitor
    except Exception:
        monitor = 0

    screen_width, screen_height = get_current_screen_size()
    native_width, native_height = get_native_screen_resolution(
        monitor, screen_width, screen_height
    )
    aspect = float(screen_width) / float(screen_height) if screen_height else 0.0
    return {
        "screen": "%dx%d" % (screen_width, screen_height),
        "native": "%dx%d" % (int(native_width), int(native_height)),
        "aspect": "%.3f" % aspect,
    }


def _scaling_reference_rows():
    from gui.extendedinterfacescaling.display_utils import get_current_screen_size
    from gui.extendedinterfacescaling.scale_calculator import effective_ui_size

    screen_width, screen_height = get_current_screen_size()

    rows = []
    for scale in REFERENCE_SCALES:
        eff_w, eff_h = effective_ui_size(screen_width, screen_height, scale)
        rows.append(
            {
                "scale": scale,
                "label": "%sx" % scale,
                "width": int(round(eff_w)),
                "height": int(round(eff_h)),
            }
        )
    return rows


_last_cached_screen_size = None
_refresh_callback_id = None
_mods_window_listener_installed = False
_settings_data_hook_installed = False
_gui_reset_listener_installed = False


def _get_mods_settings_api():
    try:
        from gui.modsSettingsApi import g_modsSettingsApi
    except ImportError:
        return None
    return g_modsSettingsApi


def refresh_mod_template(force=False):
    global _last_cached_screen_size

    api = _get_mods_settings_api()
    if api is None:
        return False

    from gui.extendedinterfacescaling.display_utils import get_current_screen_size

    screen_size = get_current_screen_size()
    templates_state = api.state.get("templates", {})
    if MOD_LINKAGE not in templates_state:
        return False

    if not force and _last_cached_screen_size == screen_size:
        return False

    _last_cached_screen_size = screen_size
    api.state["templates"][MOD_LINKAGE] = _build_template()
    api.saveState()
    return True


def schedule_template_refresh():
    global _refresh_callback_id, _last_cached_screen_size

    import BigWorld

    _last_cached_screen_size = None
    if _refresh_callback_id is not None:
        BigWorld.cancelCallback(_refresh_callback_id)
    _refresh_callback_id = BigWorld.callback(0.0, _deferred_template_refresh)


def _deferred_template_refresh():
    global _refresh_callback_id

    _refresh_callback_id = None
    refresh_mod_template(force=True)


def on_screen_geometry_changed():
    schedule_template_refresh()


def _on_mods_window_opened():
    schedule_template_refresh()


def _on_gui_reset():
    schedule_template_refresh()


def _install_mods_window_listener():
    global _mods_window_listener_installed
    if _mods_window_listener_installed:
        return

    api = _get_mods_settings_api()
    if api is None:
        return

    api.onWindowOpened += _on_mods_window_opened
    _mods_window_listener_installed = True


def _install_settings_data_hook():
    global _settings_data_hook_installed
    if _settings_data_hook_installed:
        return

    api = _get_mods_settings_api()
    if api is None:
        return

    original_generate = api.generateSettingsData

    def generateSettingsData():
        global _last_cached_screen_size

        _last_cached_screen_size = None
        refresh_mod_template(force=True)
        return original_generate()

    api.generateSettingsData = generateSettingsData
    _settings_data_hook_installed = True


def _install_gui_reset_listener():
    global _gui_reset_listener_installed
    if _gui_reset_listener_installed:
        return

    try:
        from gui import g_guiResetters
    except ImportError:
        return

    g_guiResetters.add(_on_gui_reset)
    _gui_reset_listener_installed = True


def _build_template():
    from gui.modsSettingsApi import templates
    from gui.extendedinterfacescaling import config

    info = _screen_info()
    reference_rows = _scaling_reference_rows()
    current_scale = config.get_scale()

    reset_button = templates.createButton(
        width=70, height=23, text="1.0x", offsetTop=0, offsetLeft=8
    )

    column1 = [
        templates.createLabel(
            "When enabled, this mod controls interface scale.",
            tooltip=HINT_TOOLTIP,
        ),
        templates.createEmpty(),
        templates.createInput(
            "UI scale",
            "scale",
            str(current_scale),
            tooltip=(
                HINT_TOOLTIP
                + "{BODY}Enter a value between %.1f and %.1f (e.g. 1.22).{/BODY}"
                % (MIN_UI_SCALE, MAX_UI_SCALE)
            ),
            button=reset_button,
            width=80,
        ),
        templates.createEmpty(),
        templates.createLabel("Scaling reference", tooltip=REFERENCE_TOOLTIP),
    ]

    for item in reference_rows:
        column1.append(
            templates.createLabel(
                "  %s -> %dx%d"
                % (item["label"], item["width"], item["height"])
            )
        )

    return {
        "modDisplayName": "Extended Interface Scaling",
        "settingsVersion": SETTINGS_VERSION,
        "enabled": config.is_enabled(),
        "column1": column1,
        "column2": [
            templates.createLabel("Resolution: %s" % info["screen"]),
            templates.createLabel("Native: %s" % info["native"]),
            templates.createLabel("Aspect: %s" % info["aspect"]),
            templates.createEmpty(),
            templates.createLabel(
                "Changes apply when you click Apply in the settings window."
            ),
        ],
    }


def _apply_settings(settings):
    from gui.extendedinterfacescaling import config
    from gui.extendedinterfacescaling.scale_applier import apply_scale

    settings = dict(settings)

    scale = _parse_scale(settings.get("scale", config.get_scale()))
    enabled = bool(settings.get("enabled", config.is_enabled()))

    config.apply_values(scale=scale, enabled=enabled)

    if enabled:
        apply_scale(scale)


def _on_settings_changed(linkage, settings):
    if linkage != MOD_LINKAGE:
        return
    _apply_settings(settings)


def _on_button_clicked(linkage, varName, value):
    if linkage != MOD_LINKAGE or varName != "scale":
        return

    api = _get_mods_settings_api()
    if api is None:
        return

    saved = api.getModSettings(MOD_LINKAGE, _build_template())
    if not saved:
        return

    saved["scale"] = "1.0"
    api.updateModSettings(MOD_LINKAGE, saved)


def register_mods_settings():
    api = _get_mods_settings_api()
    if api is None:
        LOG_NOTE(
            "ModsSettings API not installed. Configure scale via "
            "mods/configs/ANIALLATOR.extended_interface_scaling/config.json"
        )
        return False

    template = _build_template()
    saved = api.getModSettings(MOD_LINKAGE, template)

    if saved:
        api.registerCallback(
            MOD_LINKAGE, _on_settings_changed, _on_button_clicked
        )
        _apply_settings(saved)
    else:
        settings = api.setModTemplate(
            MOD_LINKAGE, template, _on_settings_changed, _on_button_clicked
        )
        if settings:
            _apply_settings(settings)

    _install_mods_window_listener()
    _install_settings_data_hook()
    _install_gui_reset_listener()
    return True
