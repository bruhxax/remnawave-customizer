import unittest

from remnawave_customizer.config import DEFAULT_CONFIG
from remnawave_customizer.effects import EFFECT_KEYS, render_effects_css
from remnawave_customizer.themes import PRESETS, render_css, theme_from_preset


class EffectTests(unittest.TestCase):
    def test_defaults_are_disabled(self):
        effects = DEFAULT_CONFIG['theme']['effects']
        self.assertEqual(set(effects), set(EFFECT_KEYS))
        self.assertTrue(all(value is False for value in effects.values()))

    def test_no_effect_css_when_disabled(self):
        theme = theme_from_preset(PRESETS[0])
        theme['effects'] = {key: False for key in EFFECT_KEYS}
        self.assertEqual(render_effects_css(theme), '')
        css = render_css(theme)
        self.assertNotIn('rwc-soft-snow', css)
        self.assertNotIn('rwc-ambient-particles', css)
        self.assertNotIn('rwc-soft-aurora', css)
        self.assertNotIn('rwc-floating-orbs', css)
        self.assertNotIn('rwc-soft-sweep', css)

    def test_snow_is_theme_aware_and_fades_near_half_screen(self):
        theme = theme_from_preset(PRESETS[1])
        theme['effects'] = {key: key == 'snow' for key in EFFECT_KEYS}
        css = render_css(theme)
        self.assertIn('.rwc-fx-snow::before', css)
        self.assertIn('@keyframes rwc-soft-snow', css)
        self.assertIn('rgba(var(--rwc-fx-accent)', css)
        self.assertIn('translate3d(3.6vw, 52vh, 0)', css)

    def test_all_effects_use_dedicated_overlay(self):
        theme = theme_from_preset(PRESETS[-1])
        theme['effects'] = {key: True for key in EFFECT_KEYS}
        css = render_css(theme)
        self.assertIn('#rwc-effects', css)
        self.assertIn('.rwc-fx-particles::before', css)
        self.assertIn('@keyframes rwc-soft-aurora', css)
        self.assertIn('@keyframes rwc-floating-orbs', css)
        self.assertIn('@keyframes rwc-soft-sweep', css)
        self.assertIn('@media (prefers-reduced-motion: reduce)', css)
        self.assertIn('pointer-events: none', css)

    def test_effects_load_no_external_assets(self):
        theme = theme_from_preset(PRESETS[0])
        theme['effects'] = {key: True for key in EFFECT_KEYS}
        css = render_effects_css(theme)
        self.assertNotIn('http://', css)
        self.assertNotIn('https://', css)
        self.assertNotIn('url(', css)


if __name__ == '__main__':
    unittest.main()
