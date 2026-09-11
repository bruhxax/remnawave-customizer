import unittest

from remnawave_customizer.themes import PRESETS, accent_scale, dark_scale, render_css, theme_from_preset


class ThemeTests(unittest.TestCase):
    def test_all_presets_render(self):
        for preset in PRESETS:
            css = render_css(theme_from_preset(preset))
            self.assertIn('--mantine-color-body:', css)
            self.assertIn('--mantine-color-cyan-8:', css)
            self.assertIn('--mantine-radius-default:', css)
            self.assertIn('.mantine-Card-root', css)

    def test_scales_have_ten_colors(self):
        self.assertEqual(len(accent_scale((0, 169, 255))), 10)
        self.assertEqual(len(dark_scale((7, 12, 19), (13, 21, 31))), 10)

    def test_css_has_no_external_resources(self):
        css = render_css(theme_from_preset(PRESETS[0]))
        self.assertNotIn('http://', css)
        self.assertNotIn('https://', css)


if __name__ == '__main__':
    unittest.main()
