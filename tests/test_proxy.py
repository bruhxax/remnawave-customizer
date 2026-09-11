import unittest

from remnawave_customizer.proxy import CUSTOM_TARGET, PANEL_TARGET, runtime_compose, runtime_nginx


class ProxyTests(unittest.TestCase):
    def test_target_replacement_is_reversible(self):
        samples = [
            'server remnawave:3000;',
            'reverse_proxy * http://remnawave:3000',
            '- url: "http://remnawave:3000"',
        ]
        for sample in samples:
            patched = sample.replace(PANEL_TARGET, CUSTOM_TARGET)
            self.assertIn(CUSTOM_TARGET, patched)
            self.assertEqual(patched.replace(CUSTOM_TARGET, PANEL_TARGET), sample)

    def test_runtime_has_no_public_ports(self):
        compose = runtime_compose()
        self.assertNotIn('ports:', compose)
        self.assertIn('external: true', compose)

    def test_injector_uses_dynamic_docker_dns(self):
        nginx = runtime_nginx()
        self.assertIn('resolver 127.0.0.11', nginx)
        self.assertIn('/__remnawave_customizer/theme.css', nginx)
        self.assertIn("sub_filter '</head>'", nginx)

    def test_only_css_and_html_are_decoded(self):
        nginx = runtime_nginx()
        self.assertIn('location ~* \\.css$', nginx)
        self.assertIn('location ^~ /api', nginx)
        self.assertIn('location ~* \\.(?:js|mjs|map|json|png|jpe?g|gif|svg|webp|ico|woff2?|ttf|otf|wasm|lottie)$', nginx)
        self.assertIn('gzip on;', nginx)
        self.assertNotIn('sub_filter_types text/css application/javascript', nginx)

    def test_injector_normalizes_known_legacy_surface_tokens(self):
        nginx = runtime_nginx()
        self.assertIn("sub_filter '#1b1f26' 'var(--rwc-surface)'", nginx)
        self.assertIn("sub_filter '#161b23' 'var(--rwc-surface-deep)'", nginx)
        self.assertIn('sub_filter_types text/css', nginx)
        self.assertIn('sub_filter_once off', nginx)

    def test_injector_rewrites_hardcoded_cyan_and_indigo_effects_in_css(self):
        nginx = runtime_nginx()
        self.assertIn("sub_filter 'rgb(6, 182, 212,' 'rgba(var(--rwc-accent-rgb),'", nginx)
        self.assertIn("sub_filter 'rgb(99, 102, 241,' 'rgba(var(--rwc-accent-rgb),'", nginx)
        self.assertIn("sub_filter 'rgba(59, 130, 246,' 'rgba(var(--rwc-accent-rgb),'", nginx)
        self.assertIn("sub_filter '#06b6d4' 'var(--rwc-accent)'", nginx)
        self.assertIn("sub_filter '#22d3ee' 'var(--mantine-color-cyan-4)'", nginx)


if __name__ == '__main__':
    unittest.main()
