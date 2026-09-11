<div align="center">

# 🎨 Remnawave Customizer

**Темы, цвета, скругления и визуальные эффекты для Remnawave Panel прямо из консоли.**

[English](README_EN.md) · [MIT License](LICENSE)

<br>

<img src="assets/prewiew.png" alt="Remnawave Customizer — примеры тем" width="100%">

<sub>Примеры готовых тем</sub>

</div>

> [!IMPORTANT]
> **Устанавливайте программу исключительно на сервер, где установлена Remnawave Panel.**

Customizer меняет внешний вид Panel через отдельный CSS-слой: официальный frontend, база данных и файлы Remnawave не заменяются. Обычные обновления Panel можно выполнять как раньше.

## Интерфейс

<div align="center">
<img src="assets/menu.png" alt="Remnawave Customizer — консольное меню" width="900">
<br>
<sub>Управление темами, цветами и эффектами из консоли</sub>
</div>

## Установка

```bash
git clone https://github.com/bruhxax/remnawave-customizer.git
cd remnawave-customizer
sudo ./install.sh
```

## Запуск

```bash
customizer
```

## Обновление

```bash
cd ~/remnawave-customizer
git pull
sudo ./install.sh --no-setup
```

Настройки сохраняются.

## Полное удаление

```bash
cd ~/remnawave-customizer
sudo ./uninstall.sh --purge
cd ~ && rm -rf ~/remnawave-customizer
```

Полное удаление возвращает оригинальный вид Remnawave и удаляет Customizer, его настройки, runtime, backups и локальный клон репозитория.

---

<div align="center">
<sub>by <a href="https://github.com/bruhxax">bruhxax</a></sub>
</div>
