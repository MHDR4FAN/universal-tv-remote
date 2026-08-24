# 📺 Universal TV Remote

A Termux-friendly universal TV remote with a common UI and brand/platform-specific backends.

## Supported brands
- LG
- Samsung
- Sony
- Philips
- Panasonic
- Toshiba

> Brand names alone do not determine the control protocol. Models can use different platforms, so discovery/control backends are kept separate.

## Scan modes
- 🤖 **Automatic** — scans supported brands one by one.
- 🛠️ **Manual** — choose a brand and scan only that brand.

## Current status
LG/webOS is the first fully wired backend through `lgtvremote-cli`. The universal UI, saved-TV system, scan menus, and backend structure are ready for additional platforms.

## Install on Termux
```bash
pkg install python
pip install -r requirements.txt
python main.py
```

For LG, the `lgtvremote-cli` package provides discovery and commands such as power, navigation, volume, channels, inputs, apps, media, picture settings and more.

## Network requirement
For network-controlled TVs, the phone/Termux device normally needs to be able to reach the TV over the same local network. The TV's IP can change, so scan/discovery can be used again when necessary.

## Project layout
```text
universal-tv-remote/
├── main.py
├── requirements.txt
├── scanners/
│   └── README.md
├── remotes/
│   └── README.md
└── README.md
```
