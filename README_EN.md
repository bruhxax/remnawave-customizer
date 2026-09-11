<div align="center">

# 🎨 Remnawave Customizer

**Themes, colors, rounding and visual effects for Remnawave Panel from the console.**

[Русский](README.md) · [MIT License](LICENSE)

</div>

<p align="center">
  <img src="assets/prewiew.png" alt="Remnawave Customizer themes preview" width="100%">
</p>

> [!IMPORTANT]
> **Install this program only on the server where Remnawave Panel is installed.**

Customizer changes Panel appearance through a separate CSS layer. The official frontend, database and Remnawave files are not replaced, so normal Panel upgrades can be performed as usual.

If **Subscription Page runs on the same server as Panel**, the menu also provides separate Sub Page appearance controls: colors, rounding, presets, exact stock reset and synchronization with the Panel theme.

## Interface

<p align="center">
  <img src="assets/menu-v2.png" alt="Remnawave Customizer menu" width="90%">
</p>

## Install

```bash
git clone https://github.com/bruhxax/remnawave-customizer.git
cd remnawave-customizer
sudo ./install.sh
```

## Run

```bash
customizer
```

## Update

```bash
cd ~/remnawave-customizer
git pull
sudo ./install.sh --no-setup
```

Settings are preserved.

## Full uninstall

```bash
cd ~/remnawave-customizer
sudo ./uninstall.sh --purge
cd ~ && rm -rf ~/remnawave-customizer
```

This restores the original Remnawave Panel and local Sub Page appearance and removes Customizer, settings, runtime, backups and the local repository checkout.

---

<div align="center">
<sub>by <a href="https://github.com/bruhxax">bruhxax</a></sub>
</div>
