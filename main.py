import json, os, subprocess
from wcwidth import wcswidth

CONFIG = os.path.expanduser("~/.universal_tv_remotes.json")
BRANDS = ["LG", "Samsung", "Sony", "Philips", "Panasonic", "Toshiba"]
WIDTH = 60
INNER = WIDTH - 4


def display_width(text):
    width = wcswidth(str(text))
    return max(width, 0)


def fit_row(text, width=INNER):
    text = str(text)
    if display_width(text) > width:
        out = ""
        for char in text:
            if display_width(out + char) > width:
                break
            out += char
        text = out
    return text + " " * max(0, width - display_width(text))


def load_tvs():
    try:
        with open(CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def save_tvs(tvs):
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(tvs, f, indent=2)


def clear():
    os.system("clear")


def pause():
    input("\nPress Enter to continue...")


def box(title, rows=()):
    print("╔" + "═" * (WIDTH - 2) + "╗")
    print("║ " + fit_row(title.center(INNER)) + " ║")
    print("╠" + "═" * (WIDTH - 2) + "╣")
    for row in rows:
        print("║ " + fit_row(row) + " ║")
    print("╚" + "═" * (WIDTH - 2) + "╝")


def run_lgtv(ip, *args):
    try:
        result = subprocess.run(
            ["lgtv", "--tv", ip, *args],
            text=True,
            capture_output=True,
        )
        output = (result.stdout or "").strip()
        error = (result.stderr or "").strip()
        if output:
            print(output)
        if error:
            print(error)
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ lgtv command not found. Install requirements first.")
        return False


def scan_lg():
    try:
        result = subprocess.run(["lgtv", "scan"], text=True, capture_output=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip())
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ lgtvremote-cli is not installed.")
        return False


def scan_brand(brand):
    print(f"\n🔎 Scanning {brand}...")
    if brand == "LG":
        return scan_lg()
    print(f"ℹ️ {brand} discovery backend is not implemented yet.")
    return False


def scan_menu():
    while True:
        clear()
        box("🔎 SCAN TVs", [
            "1. 🤖 Automatic Scan",
            "2. 🛠️ Manual Scan",
            "",
            "0. ↩️ Back",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "1":
            automatic_scan()
        elif choice == "2":
            manual_scan()
        elif choice == "0":
            return
        else:
            print("❌ Invalid option.")
            pause()


def automatic_scan():
    clear()
    print("🤖 AUTOMATIC TV SCAN\n")
    for number, brand in enumerate(BRANDS, 1):
        print(f"[{number}/{len(BRANDS)}]", end=" ")
        scan_brand(brand)
    print("\n📺 Scan complete.")
    pause()


def manual_scan():
    while True:
        clear()
        box("🛠️ MANUAL SCAN", [*(f"{i}. {b}" for i, b in enumerate(BRANDS, 1)), "", "0. ↩️ Back"])
        choice = input("\nSelect brand: ").strip()
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(BRANDS):
            brand = BRANDS[int(choice) - 1]
            clear()
            print(f"🔎 MANUAL {brand} SCAN\n")
            scan_brand(brand)
            pause()
        else:
            print("❌ Invalid option.")
            pause()


def add_tv():
    clear()
    box("➕ ADD TV")
    name = input("\nTV name: ").strip()
    ip = input("TV IP address: ").strip()
    if not name or not ip:
        print("❌ Name and IP are required.")
        pause()
        return
    tvs = load_tvs()
    if any(tv.get("ip") == ip for tv in tvs):
        print("⚠️ This TV is already saved.")
        pause()
        return
    print("\nBrand:")
    for i, brand in enumerate(BRANDS, 1):
        print(f"{i}. {brand}")
    choice = input("Select brand: ").strip()
    brand = BRANDS[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= len(BRANDS) else "Unknown"
    tvs.append({"name": name, "ip": ip, "brand": brand})
    save_tvs(tvs)
    print("\n✅ TV added successfully!")
    pause()


def remove_tv():
    tvs = load_tvs()
    if not tvs:
        print("No TVs saved.")
        pause()
        return
    clear()
    box("🗑️ REMOVE TV", [*(f"{i}. 📺 {tv['name']} [{tv.get('brand', '?')}]" for i, tv in enumerate(tvs, 1)), "0. Cancel"])
    choice = input("\nSelect TV: ").strip()
    if choice == "0":
        return
    if choice.isdigit() and 1 <= int(choice) <= len(tvs):
        removed = tvs.pop(int(choice) - 1)
        save_tvs(tvs)
        print(f"\n✅ Removed {removed['name']}.")
    else:
        print("❌ Invalid selection.")
    pause()


def select_tv():
    tvs = load_tvs()
    if not tvs:
        print("❌ No TVs saved yet.")
        pause()
        return
    clear()
    rows = []
    for i, tv in enumerate(tvs, 1):
        rows += [f"{i}. 📺 {tv['name']} [{tv.get('brand', '?')}]", f"   {tv['ip']}"]
    rows.append("0. ↩️ Back")
    box("📺 SELECT TV", rows)
    choice = input("\nSelect TV: ").strip()
    if choice == "0":
        return
    if choice.isdigit() and 1 <= int(choice) <= len(tvs):
        control_tv(tvs[int(choice) - 1])
    else:
        print("❌ Invalid selection.")
        pause()


def control_tv(tv):
    if tv.get("brand") != "LG":
        print(f"ℹ️ {tv.get('brand', 'Unknown')} controls are not enabled yet.")
        pause()
        return
    ip, name = tv["ip"], tv["name"]
    while True:
        clear()
        box(f"📺 {name}", [
            f"🌐 {ip}", "",
            "1. 🎮 Navigation", "2. ⏻ Power", "3. 🔊 Audio",
            "4. 📺 Channels", "5. 🔌 Inputs", "6. ▶️ Media",
            "7. 📱 Apps", "8. 🖼️ Picture", "9. 🛠️ Tools", "0. ↩️ Back",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "1": navigation(ip)
        elif choice == "2": power(ip)
        elif choice == "3": audio(ip)
        elif choice == "4": channels(ip)
        elif choice == "5": inputs(ip)
        elif choice == "6": media(ip)
        elif choice == "7": apps(ip)
        elif choice == "8": picture(ip)
        elif choice == "9": tools(ip)
        elif choice == "0": return
        else:
            print("❌ Invalid option.")
            pause()


def navigation(ip):
    while True:
        clear()
        box("🎮 NAVIGATION", [
            "            ▲",
            "           [W]",
            "",
            "      [A] [OK] [D]",
            "",
            "            ▼",
            "           [S]",
            "",
            "H. 🏠 Home",
            "B. ↩️ Back",
            "0. Back",
        ])
        choice = input("\nSelect: ").lower().strip()
        actions = {"w": "up", "s": "down", "a": "left", "d": "right", "ok": "ok", "b": "back"}
        if choice == "0": return
        if choice == "h": run_lgtv(ip, "launch", "com.webos.app.home")
        elif choice in actions: run_lgtv(ip, "nav", actions[choice])
        else: print("❌ Unknown command."); pause()


def power(ip):
    actions = {
        "1": ("on",), "2": ("off",), "3": ("power",),
        "4": ("power-status",), "5": ("screen-off",), "6": ("screen-on",)
    }
    while True:
        clear()
        box("⏻ POWER", [
            "1. 🟢 Turn ON",
            "2. 🔴 Turn OFF",
            "3. 🔄 Toggle Power",
            "4. 🔍 Power Status",
            "5. 🌑 Screen OFF",
            "6. 💡 Screen ON",
            "",
            "0. Back",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "0": return
        if choice in actions:
            run_lgtv(ip, *actions[choice])
            pause()
        else:
            print("❌ Invalid option.")
            pause()


def audio(ip):
    while True:
        clear()
        box("🔊 AUDIO", [
            "1. 🔊 Volume +",
            "2. 🔉 Volume -",
            "3. 🔇 Mute",
            "4. 🔊 Unmute",
            "5. 🎚️ Set Volume",
            "6. 🎵 Sound Mode",
            "7. 🎧 Sound Output",
            "",
            "0. Back",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "0": return
        if choice == "1": run_lgtv(ip, "volume", "up")
        elif choice == "2": run_lgtv(ip, "volume", "down")
        elif choice == "3": run_lgtv(ip, "volume", "mute")
        elif choice == "4": run_lgtv(ip, "volume", "unmute")
        elif choice == "5": run_lgtv(ip, "volume", "set", input("Volume: ").strip())
        elif choice == "6": run_lgtv(ip, "sound-mode", input("Mode: ").strip())
        elif choice == "7": run_lgtv(ip, "sound-output")
        else: print("❌ Invalid option."); pause(); continue
        pause()


def channels(ip):
    actions = {"1": ("channel", "up"), "2": ("channel", "down"), "3": ("channels",), "4": ("livetv",)}
    while True:
        clear()
        box("📺 CHANNELS", [
            "1. ⬆️ Channel +",
            "2. ⬇️ Channel -",
            "3. 📋 List Channels",
            "4. 📡 Live TV",
            "",
            "0. Back",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "0": return
        if choice in actions: run_lgtv(ip, *actions[choice]); pause()
        else: print("❌ Invalid option."); pause()


def inputs(ip):
    while True:
        clear()
        box("🔌 INPUTS", [
            "1. 📋 List Inputs",
            "2. 🔌 Switch Input",
            "",
            "0. Back",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "0": return
        if choice == "1": run_lgtv(ip, "inputs"); pause()
        elif choice == "2":
            run_lgtv(ip, "inputs")
            value = input("\nInput: ").strip()
            if value: run_lgtv(ip, "input", value)
            pause()
        else: print("❌ Invalid option."); pause()


def media(ip):
    actions = {"1": "play", "2": "pause", "3": "stop", "4": "rewind", "5": "ff", "6": "skip-forward", "7": "skip-back"}
    while True:
        clear()
        box("▶️ MEDIA", [
            "1. ▶️ Play",
            "2. ⏸️ Pause",
            "3. ⏹️ Stop",
            "4. ⏪ Rewind",
            "5. ⏩ Fast Forward",
            "6. ⏭️ Skip Forward",
            "7. ⏮️ Skip Back",
            "",
            "0. Back",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "0": return
        if choice in actions: run_lgtv(ip, actions[choice]); pause()
        else: print("❌ Invalid option."); pause()


def apps(ip):
    while True:
        clear()
        box("📱 APPS", [
            "1. 📋 List Apps",
            "2. 🚀 Launch App",
            "3. 📱 Current App",
            "",
            "0. Back",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "0": return
        if choice == "1": run_lgtv(ip, "apps")
        elif choice == "2": run_lgtv(ip, "launch", input("App ID/name: ").strip())
        elif choice == "3": run_lgtv(ip, "app")
        else: print("❌ Invalid option."); pause(); continue
        pause()


def picture(ip):
    commands = {"1": "picture-mode", "2": "backlight", "3": "brightness", "4": "contrast", "5": "trumotion", "6": "energy-saving", "7": "dimming"}
    while True:
        clear()
        box("🖼️ PICTURE", [
            "1. 🖼️ Picture Mode",
            "2. 💡 Backlight",
            "3. ☀️ Brightness",
            "4. ◐ Contrast",
            "5. 🎞️ TruMotion",
            "6. 🌿 Energy Saving",
            "7. 🌑 Dimming",
            "",
            "0. Back",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "0": return
        if choice in commands:
            value = input("Value (blank to query if supported): ").strip()
            run_lgtv(ip, commands[choice], *([value] if value else [])); pause()
        else: print("❌ Invalid option."); pause()


def tools(ip):
    while True:
        clear()
        box("🛠️ TOOLS", [
            "1. 📸 Screenshot",
            "2. 🔢 Number",
            "3. 🔴 Red",
            "4. 🟢 Green",
            "5. 🟡 Yellow",
            "6. 🔵 Blue",
            "7. 🌐 Open URL",
            "8. ℹ️ Device Info",
            "",
            "0. Back",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "0": return
        if choice == "1": run_lgtv(ip, "screenshot")
        elif choice == "2": run_lgtv(ip, "number", input("Number: ").strip())
        elif choice in {"3", "4", "5", "6"}:
            run_lgtv(ip, "color", {"3":"red","4":"green","5":"yellow","6":"blue"}[choice])
        elif choice == "7": run_lgtv(ip, "open-url", input("URL: ").strip())
        elif choice == "8": run_lgtv(ip, "enrich")
        else: print("❌ Invalid option."); pause(); continue
        pause()


def main():
    while True:
        tvs = load_tvs()
        clear()
        box("📺 UNIVERSAL TV REMOTE", [
            "1. 📺 Select TV", "2. 🔎 Scan TVs", "3. ➕ Add TV",
            "4. 🗑️ Remove TV", "5. 📋 List Saved TVs", "6. ❌ Exit", "",
            f"📺 TVs saved: {len(tvs)}",
        ])
        choice = input("\nSelect: ").strip()
        if choice == "1": select_tv()
        elif choice == "2": scan_menu()
        elif choice == "3": add_tv()
        elif choice == "4": remove_tv()
        elif choice == "5":
            clear()
            rows = [f"{i}. {tv['name']} [{tv.get('brand','?')}] {tv['ip']}" for i, tv in enumerate(tvs, 1)] or ["No TVs saved."]
            box("📋 SAVED TVs", rows)
            pause()
        elif choice == "6":
            clear(); print("👋 Bye bro!"); return
        else:
            print("❌ Invalid option."); pause()


if __name__ == "__main__":
    main()
