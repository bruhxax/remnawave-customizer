import unittest

import remnawave_customizer
from remnawave_customizer import proxy, themes
from remnawave_customizer.themes import PRESETS, theme_from_preset


class CompatTests(unittest.TestCase):
    def test_package_enables_compat_layer(self):
        self.assertEqual(remnawave_customizer.__version__, '0.6.0')
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

    def test_effect_overlay_is_injected_into_spa_shell(self):
        nginx = proxy.runtime_nginx()
        self.assertIn('id="rwc-effects"', nginx)
        self.assertIn('rwc-fx-particles', nginx)
        self.assertIn("sub_filter '</body>'", nginx)

    def test_local_subscription_page_listener_is_available(self):
        nginx = proxy.runtime_nginx()
        compose = proxy.runtime_compose()
        self.assertIn('listen 3101;', nginx)
        self.assertIn('remnawave-subscription-page:3010', nginx)
        self.assertIn('/__remnawave_customizer/subpage.css', nginx)
        self.assertIn('./subpage.css:/usr/share/nginx/html/subpage.css:ro', compose)


if __name__ == '__main__':
    unittest.main()
