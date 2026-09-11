# Security

Remnawave Customizer does not modify the Remnawave database or replace the official Panel frontend.

It stores its configuration in `/etc/remnawave-customizer`, creates backups before changing a supported reverse-proxy route, and injects only a same-origin CSS file through a separate internal proxy container.

If you discover a security issue, please report it privately to the repository owner before publishing details.
