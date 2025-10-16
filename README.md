# <p align="center">FlareWARP</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/dragon-Elec/flare-warp/main/data/icons/io.github.dragon-elec.flare-warp.svg" alt="FlareWARP Logo" width="128"/>
</p>

<p align="center">
  <em>Tame the Cloudflare WARP client on Linux with a beautiful and modern GTK4 interface.</em>
</p>

<p align="center">
  <a href="https://github.com/dragon-Elec/flare-warp/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <img src="https://www.repostatus.org/badges/latest/active.svg" alt="Project Status: Active">
</p>

---

FlareWARP is a desktop application designed to provide an intuitive, graphical frontend for the `warp-cli` on Linux. Forget the command line for daily operations; manage your connection, check stats, and switch DNS modes with a clean, simple, and responsive UI.

## See it in Action

*(Coming Soon: A GIF showcasing the main interface and features will be placed here.)*



## Why FlareWARP?

*   🚀 **Simple Connection Control:** Connect, disconnect, and monitor your WARP status at a glance.
*   📊 **Real-time Stats:** Instantly view connection data without touching the terminal.
*   🛡️ **DNS Mode Switching:** Effortlessly switch between Cloudflare's DNS filtering modes (e.g., Family, Security).
*   ✨ **Modern Desktop UI:** Built with GTK4 & Libadwaita for a clean look that integrates perfectly with modern Linux desktops.
*   🏗️ **A Solid Foundation:** Powered by the `pywarpcli` library—a robust, reusable, and standalone engine for interacting with `warp-cli`.
*   🧠 **Smart Architecture:** Designed with a clean, layered architecture that makes it reliable and easy to maintain.

## Under the Hood: A Clean Design

FlareWARP is built with a clear separation of concerns. This isn't just an app; it's an engine with a GUI on top. This design ensures stability and makes the core logic reusable for other projects.

```
+-------------------------+
|   FlareWARP (GTK4 UI)   |  <-- The Application Layer
+-------------------------+
           |
           v
+-------------------------+
|   Workflows             |  <-- Reusable, multi-step logic
+-------------------------+
           |
           v
+-------------------------+
|   pywarpcli Library     |  <-- The Core Engine (standalone)
+-------------------------+
           |
           v
+-------------------------+
|   warp-cli (binary)     |  <-- Cloudflare's CLI Tool
+-------------------------+
```

## Get Started in Minutes

### 1. Prerequisites

First, ensure you have the necessary dependencies.

*   **Cloudflare `warp-cli`:** Must be installed and registered. [Official Instructions](https://pkg.cloudflareclient.com/).
*   **Python 3.9+** and **GTK4 Libraries**:

    ```bash
    # On Debian / Ubuntu / Zorin OS
    sudo apt update && sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0

    # On Fedora
    sudo dnf install python3-gobject gtk4

    # On Arch Linux
    sudo pacman -S python-gobject gtk4
    ```

### 2. Installation & Launch

```bash
# Clone the repository
git clone https://github.com/dragon-Elec/flare-warp.git
cd flare-warp

# (Recommended) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies (A requirements.txt will be added soon)
pip install PyGObject

# Run the app!
python3 main.py
```

## Join the Journey

This project is in active development and contributions are highly welcome!

*   **Roadmap:** Our immediate focus is on perfecting the core features: connection, stats, and DNS management. Future plans include full registration management and handling for privileged commands.
*   **Contribute:** Fork the repo, create a feature branch, and submit a pull request. For a deep dive into the architecture and development plan, see the [**Project Blueprint**](FlareWARP BP.md).
*   **Feedback:** Found a bug or have a feature request? Please [open an issue](https://github.com/dragon-Elec/flare-warp/issues)!

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
