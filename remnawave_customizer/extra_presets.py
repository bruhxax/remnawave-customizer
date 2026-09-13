from __future__ import annotations

from .themes import ThemePreset


# Extra presets for the stable 1.0 release. Background/surface pairs intentionally
# stay close in luminance so nested Remnawave cards, drawers and tables remain
# clean instead of turning into a stack of bright rectangles.
EXTRA_PRESETS: tuple[ThemePreset, ...] = (
    # Ice / blue / space
    ThemePreset('neon_ice', 'Neon Ice', 'Neon Ice', (103, 232, 249), (4, 11, 16), (10, 24, 31), 'medium'),
    ThemePreset('glacier', 'Glacier', 'Glacier', (147, 197, 253), (8, 14, 22), (18, 28, 40), 'large'),
    ThemePreset('crystal_blue', 'Crystal Blue', 'Crystal Blue', (96, 211, 255), (5, 13, 21), (13, 27, 39), 'medium'),
    ThemePreset('electric_ice', 'Electric Ice', 'Electric Ice', (0, 229, 255), (2, 9, 15), (8, 22, 31), 'large'),
    ThemePreset('azure_night', 'Azure Night', 'Azure Night', (59, 130, 246), (5, 9, 18), (14, 22, 36), 'medium'),
    ThemePreset('sapphire', 'Sapphire', 'Sapphire', (67, 97, 238), (7, 8, 20), (16, 19, 38), 'medium'),
    ThemePreset('cobalt', 'Cobalt', 'Cobalt', (37, 99, 235), (5, 8, 18), (13, 19, 35), 'small'),
    ThemePreset('royal_neon', 'Royal Neon', 'Royal Neon', (99, 102, 241), (8, 8, 20), (19, 19, 39), 'large'),
    ThemePreset('deep_space', 'Deep Space', 'Deep Space', (88, 166, 255), (3, 5, 12), (10, 14, 25), 'medium'),
    ThemePreset('moonlight', 'Moonlight', 'Moonlight', (186, 210, 255), (10, 12, 19), (22, 25, 35), 'large'),

    # Purple / pink
    ThemePreset('lavender_haze', 'Lavender Haze', 'Lavender Haze', (196, 181, 253), (15, 11, 23), (29, 23, 42), 'large'),
    ThemePreset('amethyst', 'Amethyst', 'Amethyst', (167, 139, 250), (12, 8, 21), (25, 18, 39), 'medium'),
    ThemePreset('orchid_bloom', 'Orchid Bloom', 'Orchid Bloom', (216, 180, 254), (17, 9, 22), (32, 20, 40), 'large'),
    ThemePreset('neon_grape', 'Neon Grape', 'Neon Grape', (192, 91, 255), (10, 5, 17), (24, 13, 33), 'medium'),
    ThemePreset('magenta_rush', 'Magenta Rush', 'Magenta Rush', (236, 72, 153), (17, 6, 15), (32, 15, 28), 'medium'),
    ThemePreset('hot_pink', 'Hot Pink', 'Hot Pink', (255, 77, 166), (18, 6, 14), (34, 16, 29), 'large'),
    ThemePreset('sakura_night', 'Sakura Night', 'Sakura Night', (251, 146, 180), (18, 10, 16), (34, 22, 30), 'large'),
    ThemePreset('cotton_candy', 'Cotton Candy', 'Cotton Candy', (244, 166, 255), (13, 10, 22), (27, 21, 39), 'xl'),
    ThemePreset('berry_noir', 'Berry Noir', 'Berry Noir', (232, 121, 249), (15, 7, 16), (29, 16, 31), 'medium'),
    ThemePreset('plum_wine', 'Plum Wine', 'Plum Wine', (196, 120, 171), (16, 9, 15), (30, 19, 29), 'small'),

    # Red / orange / gold
    ThemePreset('ruby_noir', 'Ruby Noir', 'Ruby Noir', (244, 63, 94), (16, 6, 9), (31, 15, 20), 'medium'),
    ThemePreset('blood_moon', 'Blood Moon', 'Blood Moon', (239, 68, 68), (15, 6, 7), (30, 15, 17), 'large'),
    ThemePreset('cherry_cola', 'Cherry Cola', 'Cherry Cola', (225, 29, 72), (18, 7, 10), (34, 17, 21), 'medium'),
    ThemePreset('coral_sunset', 'Coral Sunset', 'Coral Sunset', (251, 113, 133), (20, 10, 11), (36, 21, 22), 'large'),
    ThemePreset('peach_fuzz', 'Peach Fuzz', 'Peach Fuzz', (255, 168, 133), (20, 12, 9), (36, 24, 19), 'large'),
    ThemePreset('tangerine', 'Tangerine', 'Tangerine', (251, 146, 60), (18, 10, 5), (33, 21, 12), 'medium'),
    ThemePreset('pumpkin_spice', 'Pumpkin Spice', 'Pumpkin Spice', (249, 115, 22), (18, 9, 4), (34, 19, 10), 'small'),
    ThemePreset('golden_hour', 'Golden Hour', 'Golden Hour', (250, 184, 67), (19, 14, 6), (34, 27, 15), 'large'),
    ThemePreset('honey_glow', 'Honey Glow', 'Honey Glow', (245, 190, 65), (17, 13, 6), (31, 25, 14), 'medium'),
    ThemePreset('lemon_neon', 'Lemon Neon', 'Lemon Neon', (250, 225, 45), (15, 14, 4), (28, 27, 10), 'medium'),

    # Green / mint / teal
    ThemePreset('toxic_lime', 'Toxic Lime', 'Toxic Lime', (163, 230, 53), (7, 12, 4), (16, 26, 10), 'medium'),
    ThemePreset('matcha_night', 'Matcha Night', 'Matcha Night', (132, 204, 22), (8, 12, 6), (18, 27, 13), 'small'),
    ThemePreset('matrix', 'Matrix', 'Matrix', (34, 197, 94), (3, 10, 6), (10, 24, 15), 'medium'),
    ThemePreset('jade', 'Jade', 'Jade', (16, 185, 129), (4, 12, 10), (12, 26, 21), 'large'),
    ThemePreset('neon_mint', 'Neon Mint', 'Neon Mint', (94, 234, 212), (4, 13, 12), (12, 28, 25), 'large'),
    ThemePreset('seafoam', 'Seafoam', 'Seafoam', (110, 231, 183), (7, 14, 13), (16, 29, 26), 'medium'),
    ThemePreset('teal_wave', 'Teal Wave', 'Teal Wave', (45, 212, 191), (4, 13, 14), (11, 27, 29), 'medium'),
    ThemePreset('petrol_blue', 'Petrol Blue', 'Petrol Blue', (45, 176, 190), (5, 12, 15), (14, 27, 31), 'small'),

    # Neutral / metal / warm dark
    ThemePreset('storm', 'Storm', 'Storm', (148, 163, 184), (10, 12, 16), (22, 25, 31), 'medium'),
    ThemePreset('gunmetal', 'Gunmetal', 'Gunmetal', (129, 140, 159), (11, 12, 14), (24, 26, 30), 'small'),
    ThemePreset('silver_smoke', 'Silver Smoke', 'Silver Smoke', (203, 213, 225), (13, 14, 16), (27, 29, 33), 'large'),
    ThemePreset('carbon', 'Carbon', 'Carbon', (161, 161, 170), (5, 6, 7), (16, 17, 19), 'small'),
    ThemePreset('espresso', 'Espresso', 'Espresso', (214, 158, 116), (14, 9, 7), (28, 19, 15), 'medium'),
    ThemePreset('copper', 'Copper', 'Copper', (217, 119, 87), (16, 9, 6), (31, 19, 14), 'medium'),
    ThemePreset('retro_wave', 'Retro Wave', 'Retro Wave', (255, 91, 200), (8, 7, 20), (22, 17, 39), 'xl'),
)
