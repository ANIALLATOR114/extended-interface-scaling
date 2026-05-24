def get_native_screen_resolution(monitor_index, fallback_width, fallback_height):
    import BigWorld

    native = None
    if hasattr(BigWorld, "getNativeScreenResolution"):
        native = BigWorld.getNativeScreenResolution(monitor_index)
    elif hasattr(BigWorld, "wg_getNativeScreenResoulution"):
        native = BigWorld.wg_getNativeScreenResoulution(monitor_index)

    if native and len(native) >= 2:
        return int(native[0]), int(native[1])

    return int(fallback_width), int(fallback_height)


def get_current_screen_size():
    """Return the configured game window resolution in pixels."""
    import BigWorld

    try:
        from gui.shared.utils.monitor_settings import g_monitorSettings

        if g_monitorSettings.isWindowed():
            window_size = g_monitorSettings.currentWindowSize
            width = int(window_size.width)
            height = int(window_size.height)
            if width > 0 and height > 0:
                return width, height

        if g_monitorSettings.isBorderless():
            borderless_size = g_monitorSettings.currentBorderlessSize
            width = int(borderless_size.width)
            height = int(borderless_size.height)
            if width > 0 and height > 0:
                return width, height

        video_mode = g_monitorSettings.currentVideoMode
        if video_mode is not None:
            width = int(video_mode.width)
            height = int(video_mode.height)
            if width > 0 and height > 0:
                return width, height
    except Exception:
        pass

    try:
        resolution = BigWorld.getCurrentResolution(BigWorld.getWindowMode())
        if resolution and len(resolution) >= 2:
            width = int(resolution[0])
            height = int(resolution[1])
            if width > 0 and height > 0:
                return width, height
    except Exception:
        pass

    size = BigWorld.screenSize()
    return int(size[0]), int(size[1])
