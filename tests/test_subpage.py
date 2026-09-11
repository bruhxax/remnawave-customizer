import copy
import unittest

from remnawave_customizer.config import DEFAULT_CONFIG
from remnawave_customizer.subpage import effective_theme, ensure_config, render_css


class SubPageTests(unittest.TestCase):
    def test_default_subpage_config_is_present(self):
        config = copy.deepcopy(DEFAULT_CONFIG)
        data = ensure_config(config)
        self.assertFalse(data['enabled'])
        self.assertEqual(data['mode'], 'custom')
        self.assertIn('accent', data)
        self.assertIn('background', data)
        self.assertIn('surface', data)

    def test_subpage_css_recolors_primary_decorative_families(self):
        config = copy.deepcopy(DEFAULT_CONFIG)
        css = render_css(effective_theme(config))
        self.assertIn('--rwc-sub-accent:', css)
        self.assertIn('--mantine-color-cyan-8:', css)
        self.assertIn('--mantine-color-blue-8:', css)
        self.assertIn('--mantine-color-violet-8:', css)
        self.assertIn('.animated-background', css)
        self.assertIn('.header-wrapper', css)
        self.assertIn('.info-card-cyan', css)
        self.assertIn('scrollbar-color:', css)

    def test_subpage_inline_theme_icons_follow_selected_accent(self):
        config = copy.deepcopy(DEFAULT_CONFIG)
        css = render_css(effective_theme(config))
        self.assertIn('RWC Subscription Page: finish hardcoded decorative glow normalization', css)
        self.assertIn('.mantine-Timeline-root', css)
        self.assertIn('--tl-color: var(--rwc-sub-accent)', css)
        self.assertIn('.mantine-ThemeIcon-root[style*="34, 211, 238"]', css)
        self.assertIn('inset 0 0 20px rgba(var(--rwc-sub-accent-rgb), 0.16)', css)

    def test_active_installation_client_keeps_accent_glow(self):
        config = copy.deepcopy(DEFAULT_CONFIG)
        css = render_css(effective_theme(config))
        self.assertIn('[class*="appButtonActive"]', css)
        self.assertIn('border-left-color: var(--rwc-sub-accent)', css)
        self.assertIn('inset 4px 0 14px -4px rgba(var(--rwc-sub-accent-rgb), 0.38)', css)
        self.assertIn('[class*="appName"]', css)

    def test_sync_mode_uses_panel_theme(self):
        config = copy.deepcopy(DEFAULT_CONFIG)
        config['subpage']['mode'] = 'sync'
        config['theme']['accent'] = [245, 158, 11]
        config['theme']['background'] = [18, 13, 7]
        config['theme']['surface'] = [32, 25, 16]
        config['theme']['radius'] = 'large'
        theme = effective_theme(config)
        self.assertEqual(theme['accent'], [245, 158, 11])
        self.assertEqual(theme['background'], [18, 13, 7])
        self.assertEqual(theme['surface'], [32, 25, 16])
        self.assertEqual(theme['radius'], 'large')

    def test_sync_mode_does_not_follow_disabled_panel_theme(self):
        config = copy.deepcopy(DEFAULT_CONFIG)
        config['subpage']['mode'] = 'sync'
        config['theme']['enabled'] = False
        theme = effective_theme(config)
        self.assertEqual(theme['accent'], config['subpage']['accent'])


if __name__ == '__main__':
    unittest.main()
