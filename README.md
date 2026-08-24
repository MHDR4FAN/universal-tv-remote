# 📺 Universal TV Remote

Every TV remote control accessible from a Termux-friendly interface.

## Supported brands
- LG
- Samsung
- Sony
- Philips
- Panasonic
- Toshiba

## Scan modes
- 🤖 Automatic — scans supported brands one by one.
- 🛠️ Manual — choose one brand and scan only that brand.

## Current backend
LG is wired to `lgtvremote-cli` for discovery and control. Other brands have isolated backend placeholders so their platform-specific protocols can be added without changing the UI.

## Run
```bash
python main.py
```

LG dependency:
```bash
pip install lgtvremote-cli
```
