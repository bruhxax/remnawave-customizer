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
