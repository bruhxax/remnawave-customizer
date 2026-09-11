import unittest

import remnawave_customizer
from remnawave_customizer import proxy, themes
from remnawave_customizer.themes import PRESETS, theme_from_preset


class CompatTests(unittest.TestCase):
    def test_package_enables_compat_layer(self):
        self.assertEqual(remnawave_customizer.__version__, '0.3.3')
        css = themes.render_css(theme_from_preset(PRESETS[0]))
        self.assertIn('decorative accent compatibility', css)

    def test_action_and_theme_icons_follow_accent(self):
        css = themes.render_css(theme_from_preset(PRESETS[0]))
        self.assertIn('.mantine-ActionIcon-root[style*="mantine-color-cyan"]', css)
        self.assertIn('.mantine-ThemeIcon-root[style*="mantine-color-blue"]', css)
        self.assertIn('--ai-bd: 1px solid rgba(var(--rwc-accent-rgb), 0.42)', css)
        self.assertIn('--ti-bg: rgba(var(--rwc-accent-rgb), 0.09)', css)

    def test_sidebar_hover_and_active_glow_follow_accent(self):
        css = themes.render_css(theme_from_preset(PRESETS[0]))
        self.assertIn('.mantine-AppShell-navbar a:hover svg', css)
        self.assertIn('drop-shadow(0 2px 4px rgba(var(--rwc-accent-rgb), 0.28))', css)
        self.assertIn('.mantine-AppShell-navbar [data-active="true"]::after', css)

    def test_transformed_css_is_revalidated(self):
        nginx = proxy.runtime_nginx()
        self.assertIn('RWC: transformed CSS must not stay immutable', nginx)
        self.assertIn('proxy_hide_header Cache-Control;', nginx)
        self.assertIn('add_header Cache-Control "no-cache, must-revalidate" always;', nginx)


if __name__ == '__main__':
    unittest.main()
