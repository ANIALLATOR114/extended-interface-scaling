import math

LESTA_SCALES = (
    (1920, 1200, (0.0, 1.0)),
    (2048, 1546, (0.0, 1.0, 1.25, 1.5)),
    (2560, 1600, (0.0, 1.0, 1.25, 1.5, 1.75)),
    (3200, 2048, (0.0, 1.0, 1.25, 1.5, 1.75, 2.0)),
    (4096, 2160, (0.0, 1.0, 1.25, 1.5, 1.75, 2.0)),
)

MAX_SCALE_STEP = 1
MIN_SCREEN_WIDTH = 1024
MIN_SCREEN_HEIGHT = 768

GOOD_FRACTION_SCALES = (
    0.75,
    1.0,
    1.25,
    1.5,
    1.75,
    2.0,
    2.25,
    2.5,
    3.0,
    4.0,
)


def glyph_cache_size(scale):
    return int(1024 * math.ceil(scale))


def effective_ui_size(screen_width, screen_height, scale):
    if scale <= 0:
        return screen_width, screen_height
    return screen_width / scale, screen_height / scale


def _is_quarter_step(scale):
    return abs(scale * 4.0 - round(scale * 4.0)) < 0.001


def score_sharpness(scale, optimal_scales):
    if any(abs(scale - candidate) < 0.001 for candidate in optimal_scales):
        return "optimal"
    if _is_quarter_step(scale):
        return "good"
    return "soft"


def get_lesta_optimal_scales(screen_width, screen_height):
    for max_width, max_height, scales in LESTA_SCALES:
        if screen_width <= max_width or screen_height <= max_height:
            return [value for value in scales if value > 0.0]

    max_scale = int(
        max(
            min(
                float(screen_width) / MIN_SCREEN_WIDTH,
                float(screen_height) / MIN_SCREEN_HEIGHT,
            ),
            1.0,
        )
    )
    result = [1.0]
    for step in xrange(0, max_scale):
        result.append(1.0 + MAX_SCALE_STEP * step)
    return result


def get_eu_optimal_scales(screen_width, screen_height):
    ref_width = max(screen_width, MIN_SCREEN_WIDTH)
    ref_height = max(screen_height, MIN_SCREEN_HEIGHT)

    scale_power = max(
        min(
            int(math.log(max(float(ref_width) / MIN_SCREEN_WIDTH, 1.0), 2)),
            int(math.log(max(float(ref_height) / MIN_SCREEN_HEIGHT, 1.0), 2)),
        ),
        0,
    )

    result = []
    for power in xrange(scale_power + 1):
        result.append(2.0 ** power)
    return sorted(set(result))


def get_optimal_scales(screen_width, screen_height, api):
    if api == "float":
        return get_lesta_optimal_scales(screen_width, screen_height)
    return get_eu_optimal_scales(screen_width, screen_height)


def get_good_candidate_scales(optimal_scales):
    candidates = set(optimal_scales)
    candidates.update(GOOD_FRACTION_SCALES)
    return sorted(candidates)


def build_recommendations(screen_width, screen_height, api):
    optimal = get_optimal_scales(screen_width, screen_height, api)
    candidates = get_good_candidate_scales(optimal)
    recommendations = []

    for scale in candidates:
        if scale < 0.75 or scale > 4.0:
            continue
        rating = score_sharpness(scale, optimal)
        eff_w, eff_h = effective_ui_size(screen_width, screen_height, scale)
        recommendations.append(
            {
                "scale": scale,
                "rating": rating,
                "glyphCache": glyph_cache_size(scale),
                "effectiveWidth": int(round(eff_w)),
                "effectiveHeight": int(round(eff_h)),
            }
        )

    order = {"optimal": 0, "good": 1, "soft": 2}
    recommendations.sort(key=lambda item: (order[item["rating"]], item["scale"]))
    return recommendations


def get_display_info(screen_width, screen_height, scale, api):
    optimal = get_optimal_scales(screen_width, screen_height, api)
    eff_w, eff_h = effective_ui_size(screen_width, screen_height, scale)
    aspect = float(screen_width) / float(screen_height) if screen_height else 0.0

    return {
        "screenWidth": screen_width,
        "screenHeight": screen_height,
        "aspectRatio": round(aspect, 3),
        "currentScale": scale,
        "glyphCacheSize": glyph_cache_size(scale),
        "sharpness": score_sharpness(scale, optimal),
        "effectiveWidth": int(round(eff_w)),
        "effectiveHeight": int(round(eff_h)),
        "apiType": api,
        "recommendations": build_recommendations(screen_width, screen_height, api),
    }
