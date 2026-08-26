#!/usr/bin/env python3
import sys
from pathlib import Path

MODULES_TO_ADD = [
    "drivers/bluetooth/btintel.ko",
    "drivers/bluetooth/btrtl.ko",
    "drivers/bluetooth/btusb.ko",
    "drivers/misc/eeprom/eeprom_93cx6.ko",
    "drivers/net/wireless/ath/ath.ko",
    "drivers/net/wireless/ath/ath9k/ath9k_common.ko",
    "drivers/net/wireless/ath/ath9k/ath9k_htc.ko",
    "drivers/net/wireless/ath/ath9k/ath9k_hw.ko",
    "drivers/net/wireless/ath/carl9170/carl9170.ko",
    "drivers/net/wireless/mediatek/mt76/mt76.ko",
    "drivers/net/wireless/mediatek/mt76/mt76-usb.ko",
    "drivers/net/wireless/mediatek/mt76/mt76x0/mt76x0-common.ko",
    "drivers/net/wireless/mediatek/mt76/mt76x0/mt76x0u.ko",
    "drivers/net/wireless/mediatek/mt76/mt76x02-lib.ko",
    "drivers/net/wireless/mediatek/mt76/mt76x02-usb.ko",
    "drivers/net/wireless/mediatek/mt76/mt76x2/mt76x2-common.ko",
    "drivers/net/wireless/mediatek/mt76/mt76x2/mt76x2u.ko",
    "drivers/net/wireless/mediatek/mt7601u/mt7601u.ko",
    "drivers/net/wireless/ralink/rt2x00/rt2800lib.ko",
    "drivers/net/wireless/ralink/rt2x00/rt2800usb.ko",
    "drivers/net/wireless/ralink/rt2x00/rt2x00lib.ko",
    "drivers/net/wireless/ralink/rt2x00/rt2x00usb.ko",
    "drivers/net/wireless/realtek/rtl818x/rtl8187/rtl8187.ko",
    "drivers/net/wireless/realtek/rtl8xxxu/rtl8xxxu.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_8723d.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_8723du.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_8723x.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_8821c.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_8821cu.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_8822b.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_8822bu.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_8822c.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_8822cu.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_core.ko",
    "drivers/net/wireless/realtek/rtw88/rtw88_usb.ko",
    "net/bluetooth/bnep/bnep.ko",
    "net/mac80211/mac80211.ko",
    "net/wireless/cfg80211.ko",
]


def main():
    target_path = Path(sys.argv[1] if len(sys.argv) > 1 else "modules.bzl")
    if not target_path.exists():
        print(f"Target file {target_path} not found, skipping.")
        return 0

    with target_path.open("r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines(keepends=True)

    # Filter out modules that are already present
    to_inject = [m for m in MODULES_TO_ADD if f'"{m}"' not in content]
    if not to_inject:
        print("All NetHunter wireless modules already registered in modules.bzl.")
        return 0

    formatted_lines = [f'    "{m}",\n' for m in to_inject]

    target_found = False
    for i, line in enumerate(lines):
        if any(key in line for key in ("_COMMON_MODULES = [", "_GKI_AARCH64_MODULES = [", "COMMON_MODULES = [", "gki_aarch64_modules = [")):
            lines = lines[:i + 1] + formatted_lines + lines[i + 1:]
            target_found = True
            break

    if not target_found:
        lines.append("\n_NETHUNTER_MODULES = [\n")
        lines.extend(formatted_lines)
        lines.append("]\n")

    with target_path.open("w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Successfully registered {len(to_inject)} NetHunter wireless modules in {target_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
