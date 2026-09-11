import unittest

from remnawave_customizer.themes import PRESETS, accent_scale, dark_scale, render_css, theme_from_preset


class ThemeTests(unittest.TestCase):
    def test_all_presets_render(self):
        for preset in PRESETS:
            css = render_css(theme_from_preset(preset))
            self.assertIn('--mantine-color-body:', css)
            self.assertIn('--mantine-color-cyan-8:', css)
            self.assertIn('--mantine-color-blue-8:', css)
            self.assertIn('--mantine-color-indigo-8:', css)
            self.assertIn('--mantine-color-cyan-light:', css)
            self.assertIn('--mantine-color-blue-light:', css)
            self.assertIn('--mantine-color-indigo-light:', css)
            self.assertIn('--mantine-radius-default:', css)
            self.assertIn('--rwc-surface-deep:', css)

    def test_many_presets_are_available(self):
        self.assertGreaterEqual(len(PRESETS), 18)
        keys = {preset.key for preset in PRESETS}
        self.assertEqual(len(keys), len(PRESETS))
        self.assertIn('oled', keys)
        self.assertIn('tokyo', keys)
        self.assertIn('rose', keys)
        self.assertIn('cyber', keys)

    def test_scales_have_ten_colors(self):
        self.assertEqual(len(accent_scale((0, 169, 255))), 10)
        self.assertEqual(len(dark_scale((7, 12, 19), (13, 21, 31))), 10)

    def test_selected_accent_is_primary_shade(self):
        accent = (217, 70, 239)
        self.assertEqual(accent_scale(accent)[8], accent)

    def test_text_side_of_dark_scale_stays_neutral(self):
        green = dark_scale((6, 16, 14), (13, 29, 25))
        purple = dark_scale((13, 10, 22), (25, 19, 39))
        self.assertEqual(green[:4], purple[:4])
        self.assertNotEqual(green[4:], purple[4:])

    def test_css_avoids_broad_component_repainting(self):
        css = render_css(theme_from_preset(PRESETS[0]))
        self.assertNotIn('.mantine-Card-root', css)
        self.assertNotIn('.mantine-Modal-content', css)
        self.assertNotIn('.mantine-Drawer-content', css)
        self.assertIn('.mantine-AppShell-main', css)

    def test_sidebar_glow_uses_selected_accent(self):
        css = render_css(theme_from_preset(PRESETS[-1]))
        self.assertIn('.mantine-AppShell-navbar::before', css)
        self.assertIn('rgba(var(--rwc-accent-rgb), 0.065)', css)
        self.assertIn('.mantine-AppShell-navbar [data-active="true"] svg', css)

    def test_mrt_inline_background_is_overridden_without_js_rewrite(self):
        css = render_css(theme_from_preset(PRESETS[0]))
        self.assertIn('[style*="--mrt-base-background-color"]', css)
        self.assertIn('--mrt-base-background-color: var(--rwc-surface) !important;', css)

    def test_navigation_progress_track_is_forced_transparent(self):
        css = render_css(theme_from_preset(PRESETS[0]))
        self.assertIn('.mantine-Progress-root[style*="--nprogress-z-index"]', css)
        self.assertIn('background: transparent !important;', css)

    def test_css_has_no_external_resources(self):
        css = render_css(theme_from_preset(PRESETS[0]))
        self.assertNotIn('http://', css)
        self.assertNotIn('https://', css)


if __name__ == '__main__':
    unittest.main()
