#!/system/bin/sh
# ==============================================================================
# Kali NetHunter Kernel Feature & Config Checker
# Script: checker.sh
# Target: Android Rooted Terminal (Termux / NetHunter Chroot / ADB Root Shell)
# Author: Abid Hasan Sojib (gki_kernel_builder)
# ==============================================================================

# ANSI Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

TOTAL_CHECKED=0
PASSED_COUNT=0
MODULE_COUNT=0
FAILED_COUNT=0

# Ensure Root Access
if [ "$(id -u)" -ne 0 ]; then
    echo -e "${RED}${BOLD}[!] ERROR: This script must be run as root (su).${NC}"
    echo -e "Please type ${YELLOW}su${NC} and run again."
    exit 1
fi

clear 2>/dev/null || true
echo -e "${CYAN}${BOLD}================================================================${NC}"
echo -e "${CYAN}${BOLD}       🐉 KALI NETHUNTER KERNEL COMPATIBILITY CHECKER 🐉       ${NC}"
echo -e "${CYAN}${BOLD}================================================================${NC}"
echo -e "Kernel Version : ${YELLOW}$(uname -r)${NC}"
echo -e "Kernel Arch    : ${YELLOW}$(uname -m)${NC}"
echo -e "SELinux Mode   : ${YELLOW}$(getenforce 2>/dev/null || echo 'Unknown')${NC}"
echo -e "Date & Time    : ${YELLOW}$(date)${NC}"
echo -e "${CYAN}${BOLD}================================================================${NC}\n"

# Locate kernel config
CONFIG_FILE=""
TEMP_CONFIG="/tmp/running_kernel_config"

if [ -f "/proc/config.gz" ]; then
    if gzip -dc /proc/config.gz > "$TEMP_CONFIG" 2>/dev/null; then
        CONFIG_FILE="$TEMP_CONFIG"
        echo -e "${GREEN}[✔] Loaded live kernel config from /proc/config.gz${NC}\n"
    elif zcat /proc/config.gz > "$TEMP_CONFIG" 2>/dev/null; then
        CONFIG_FILE="$TEMP_CONFIG"
        echo -e "${GREEN}[✔] Loaded live kernel config from /proc/config.gz${NC}\n"
    fi
elif [ -f "/boot/config-$(uname -r)" ]; then
    CONFIG_FILE="/boot/config-$(uname -r)"
    echo -e "${GREEN}[✔] Loaded kernel config from /boot/config-$(uname -r)${NC}\n"
fi

if [ -z "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}[!] Notice: /proc/config.gz not found on this device.${NC}"
    echo -e "${YELLOW}[*] Checker will inspect live kernel subsystems, /dev nodes, and DLKM modules.${NC}\n"
fi

# Print Section Header
section_header() {
    echo -e "\n${BLUE}${BOLD}--- $1 ---${NC}"
}

# Check a kernel config option
check_config() {
    local config_name="$1"
    local feature_desc="$2"
    local fallback_type="$3" # dev_node, module_file, fs, socket
    local fallback_target="$4"

    TOTAL_CHECKED=$((TOTAL_CHECKED+1))

    if [ -n "$CONFIG_FILE" ] && [ -f "$CONFIG_FILE" ]; then
        local val
        val=$(grep "^${config_name}=" "$CONFIG_FILE" 2>/dev/null | cut -d'=' -f2 || true)
        
        if [ "$val" = "y" ]; then
            echo -e "  [ ${GREEN}✔ BUILT-IN${NC} ] ${BOLD}${config_name}${NC}=y  (${CYAN}${feature_desc}${NC})"
            PASSED_COUNT=$((PASSED_COUNT+1))
            return 0
        elif [ "$val" = "m" ]; then
            local mod_base="${config_name#CONFIG_}"
            mod_base=$(echo "$mod_base" | tr '[:upper:]' '[:lower:]' | tr '-' '_')
            local target_mod=""
            if [ -n "$fallback_target" ]; then
                target_mod="${fallback_target%.ko}"
                target_mod=$(echo "$target_mod" | tr '[:upper:]' '[:lower:]' | tr '-' '_')
            fi
            if lsmod 2>/dev/null | grep -qi -E "^(${mod_base}|${target_mod})([[:space:]]|$)"; then
                echo -e "  [ ${GREEN}✔ MODULE (LOADED)${NC} ] ${BOLD}${config_name}${NC}=m  (${CYAN}${feature_desc}${NC})"
            else
                echo -e "  [ ${YELLOW}● MODULE (=m)${NC} ]    ${BOLD}${config_name}${NC}=m  (${CYAN}${feature_desc}${NC})"
            fi
            MODULE_COUNT=$((MODULE_COUNT+1))
            return 0
        else
            echo -e "  [ ${RED}✘ DISABLED${NC} ]     ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC})"
            FAILED_COUNT=$((FAILED_COUNT+1))
            return 1
        fi
    fi

    # Fallback checking when config.gz is not available
    case "$fallback_type" in
        dev_node)
            if ls $fallback_target >/dev/null 2>&1; then
                echo -e "  [ ${GREEN}✔ PRESENT${NC} ] ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC} -> ${fallback_target})"
                PASSED_COUNT=$((PASSED_COUNT+1))
            else
                echo -e "  [ ${YELLOW}● DORMANT${NC} ] ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC} -> node ${fallback_target} absent)"
                MODULE_COUNT=$((MODULE_COUNT+1))
            fi
            ;;
        module_file)
            local mod_found=0
            for dir in /data/adb/modules/gki_nethunter_wireless/lkm \
                       /data/adb/modules/gki_nethunter_wireless/system/lib/modules \
                       /vendor_dlkm/lib/modules \
                       /vendor/lib/modules \
                       /system/lib/modules; do
                if [ -f "$dir/$fallback_target" ]; then
                    mod_found=1
                    break
                fi
            done
            if [ "$mod_found" -eq 1 ]; then
                if lsmod 2>/dev/null | grep -qi "${fallback_target%.ko}"; then
                    echo -e "  [ ${GREEN}✔ LOADED${NC} ] ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC} -> ${fallback_target})"
                else
                    echo -e "  [ ${YELLOW}● AVAILABLE${NC} ] ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC} -> ${fallback_target})"
                fi
                MODULE_COUNT=$((MODULE_COUNT+1))
            else
                echo -e "  [ ${RED}✘ NOT FOUND${NC} ] ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC} -> ${fallback_target})"
                FAILED_COUNT=$((FAILED_COUNT+1))
            fi
            ;;
        fs)
            if grep -qw "$fallback_target" /proc/filesystems 2>/dev/null; then
                echo -e "  [ ${GREEN}✔ SUPPORTED${NC} ] ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC} -> filesystem ${fallback_target})"
                PASSED_COUNT=$((PASSED_COUNT+1))
            else
                echo -e "  [ ${RED}✘ MISSING${NC} ] ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC})"
                FAILED_COUNT=$((FAILED_COUNT+1))
            fi
            ;;
        socket)
            if [ -e "/proc/net/$fallback_target" ]; then
                echo -e "  [ ${GREEN}✔ ACTIVE${NC} ] ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC})"
                PASSED_COUNT=$((PASSED_COUNT+1))
            else
                echo -e "  [ ${YELLOW}● INACTIVE${NC} ] ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC})"
                FAILED_COUNT=$((FAILED_COUNT+1))
            fi
            ;;
        *)
            echo -e "  [ ${YELLOW}? CHECK MANUAL${NC} ] ${BOLD}${config_name}${NC}  (${CYAN}${feature_desc}${NC})"
            ;;
    esac
}

# ==============================================================================
# 1. USB HID GADGET & BADUSB ATTACKS (KEYBOARD / MOUSE INJECTION)
# ==============================================================================
section_header "1. USB HID Gadgets & BadUSB (Rubber Ducky / DuckHunter)"
check_config "CONFIG_HID" "Core HID subsystem" "dev_node" "/sys/class/hidraw*"
check_config "CONFIG_HID_GENERIC" "Generic HID driver" "dev_node" "/sys/class/hidraw*"
check_config "CONFIG_USB_HID" "USB HID transport support" "dev_node" "/dev/hidraw*"
check_config "CONFIG_UHID" "Userspace HID (Bluetooth BLE injection)" "dev_node" "/dev/uhid"
check_config "CONFIG_USB_CONFIGFS" "USB ConfigFS support" "dev_node" "/config/usb_gadget"
check_config "CONFIG_USB_CONFIGFS_F_FS" "FunctionFS gadget support" "dev_node" "/config/usb_gadget"
check_config "CONFIG_USB_CONFIGFS_F_HID" "BadUSB HID keyboard/mouse (/dev/hidg0)" "dev_node" "/dev/hidg*"
check_config "CONFIG_USB_F_HID" "USB HID gadget driver logic" "dev_node" "/dev/hidg*"

# ==============================================================================
# 2. USB ARSENAL & HARDWARE HACKING GADGETS
# ==============================================================================
section_header "2. USB Arsenal & Hardware Hacking Gadgets"
check_config "CONFIG_USB_ACM" "CDC-ACM host (Proxmark3 / Flipper Zero)" "module_file" "cdc-acm.ko"
check_config "CONFIG_USB_CONFIGFS_ACM" "CDC-ACM serial gadget" "dev_node" "/dev/ttyGS*"
check_config "CONFIG_USB_CONFIGFS_SERIAL" "USB Serial gadget support" "dev_node" "/dev/ttyGS*"
check_config "CONFIG_USB_CONFIGFS_OBEX" "Object Exchange (OBEX) protocol" "dev_node" "/config/usb_gadget"
check_config "CONFIG_USB_CONFIGFS_MASS_STORAGE" "USB Mass Storage (DriveDroid ISOs)" "dev_node" "/config/usb_gadget"
check_config "CONFIG_USB_F_MASS_STORAGE" "Mass storage function driver" "dev_node" "/config/usb_gadget"
check_config "CONFIG_USB_CONFIGFS_RNDIS" "RNDIS Ethernet gadget (Windows MITM)" "dev_node" "/config/usb_gadget"
check_config "CONFIG_USB_CONFIGFS_ECM" "CDC-ECM Ethernet gadget (PoisonTap)" "dev_node" "/config/usb_gadget"
check_config "CONFIG_USB_CONFIGFS_ECM_SUBSET" "CDC-ECM subset protocol" "dev_node" "/config/usb_gadget"
check_config "CONFIG_USB_CONFIGFS_NCM" "CDC-NCM high-speed Ethernet gadget" "dev_node" "/config/usb_gadget"
check_config "CONFIG_USB_CONFIGFS_EEM" "CDC-EEM Ethernet gadget" "dev_node" "/config/usb_gadget"

# ==============================================================================
# 3. USB-TO-UART SERIAL ADAPTERS
# ==============================================================================
section_header "3. USB-to-UART Adapters (Hardware Hacking / Router Serial)"
check_config "CONFIG_USB_SERIAL" "USB Serial core converter stack" "module_file" "usbserial.ko"
check_config "CONFIG_USB_SERIAL_GENERIC" "Generic USB Serial driver" "dev_node" "/dev/ttyUSB*"
check_config "CONFIG_USB_SERIAL_CH341" "WCH CH340 / CH341 (Arduino/NodeMCU)" "module_file" "ch341.ko"
check_config "CONFIG_USB_SERIAL_FTDI_SIO" "FTDI FT232R / FT2232 UART & JTAG" "module_file" "ftdi_sio.ko"
check_config "CONFIG_USB_SERIAL_CP210X" "Silicon Labs CP2102 / CP2104 (ESP32)" "module_file" "cp210x.ko"
check_config "CONFIG_USB_SERIAL_PL2303" "Prolific PL2303 USB-Serial bridge" "module_file" "pl2303.ko"

# ==============================================================================
# 4. WIRELESS CORE & PACKET INJECTION
# ==============================================================================
section_header "4. Core Wireless & Packet Injection Stack"
check_config "CONFIG_NET_CORE" "Linux Core Networking" "dev_node" "/proc/net/dev"
check_config "CONFIG_WIRELESS" "Wireless Network Subsystem" "dev_node" "/proc/net/wireless"
check_config "CONFIG_CFG80211" "cfg80211 Wireless Configuration API" "module_file" "cfg80211.ko"
check_config "CONFIG_CFG80211_WEXT" "Wireless-Extensions backward compat" "module_file" "cfg80211.ko"
check_config "CONFIG_NL80211_TESTMODE" "nl80211 Netlink Packet Injection" "module_file" "cfg80211.ko"
check_config "CONFIG_MAC80211" "mac80211 IEEE 802.11 Stack & Injection" "module_file" "mac80211.ko"
check_config "CONFIG_MAC80211_MESH" "mac80211 802.11s Mesh Networking" "module_file" "mac80211.ko"
check_config "CONFIG_MAC80211_LEDS" "mac80211 LED Activity Triggers" "module_file" "mac80211.ko"
check_config "CONFIG_MAC80211_MESSAGE_TRACING" "mac80211 Frame Tracing" "module_file" "mac80211.ko"
check_config "CONFIG_RFKILL" "RFKill Wireless Radio Control" "module_file" "rfkill.ko"

# ==============================================================================
# 5. USB WI-FI ADAPTER DRIVERS
# ==============================================================================
section_header "5. USB Wi-Fi Dongle Drivers (Monitor Mode & Injection)"
# Realtek
check_config "CONFIG_WLAN_VENDOR_REALTEK" "Realtek WLAN Vendor Support" "module_file" "rtw88_core.ko"
check_config "CONFIG_RTW88" "Realtek RTW88 Core Framework" "module_file" "rtw88_core.ko"
check_config "CONFIG_RTW88_CORE" "Realtek RTW88 Core Stack" "module_file" "rtw88_core.ko"
check_config "CONFIG_RTW88_USB" "Realtek RTW88 USB Bus Support" "module_file" "rtw88_usb.ko"
check_config "CONFIG_RTW88_8822B" "Realtek 8822B core support" "module_file" "rtw88_8822b.ko"
check_config "CONFIG_RTW88_8822BU" "Alfa AWUS036ACH / RTL8812BU / RTL8822BU" "module_file" "rtw88_8822bu.ko"
check_config "CONFIG_RTW88_8822C" "Realtek 8822C core support" "module_file" "rtw88_8822c.ko"
check_config "CONFIG_RTW88_8822CU" "Realtek RTL8822CU Dual-Band AC1300" "module_file" "rtw88_8822cu.ko"
check_config "CONFIG_RTW88_8821C" "Realtek 8821C core support" "module_file" "rtw88_8821c.ko"
check_config "CONFIG_RTW88_8821CU" "Realtek RTL8811CU / RTL8821CU AC600" "module_file" "rtw88_8821cu.ko"
check_config "CONFIG_RTW88_8723D" "Realtek 8723D core support" "module_file" "rtw88_8723d.ko"
check_config "CONFIG_RTW88_8723DU" "Realtek RTL8723DU Wi-Fi + Bluetooth" "module_file" "rtw88_8723du.ko"
check_config "CONFIG_RTW88_LEDS" "RTW88 LED Indicator Support" "module_file" "rtw88_core.ko"
check_config "CONFIG_RTL8187" "Alfa AWUS036H (RTL8187L High-Power)" "module_file" "rtl8187.ko"
check_config "CONFIG_RTL8XXXU" "Realtek RTL8188EUS / TL-WN722N v2/v3" "module_file" "rtl8xxxu.ko"
check_config "CONFIG_RTL8XXXU_UNTESTED" "RTL8xxxu Experimental USB Device IDs" "module_file" "rtl8xxxu.ko"
check_config "CONFIG_RTL_CARDS" "Realtek Legacy Wireless Cards" "module_file" "rtl8192cu.ko"
check_config "CONFIG_RTL8192CU" "Realtek RTL8192CU 802.11n Dongle" "module_file" "rtl8192cu.ko"

# Atheros / Qualcomm
check_config "CONFIG_WLAN_VENDOR_ATH" "Atheros WLAN Vendor Support" "module_file" "ath9k_htc.ko"
check_config "CONFIG_ATH9K_HTC" "Atheros AR9271 / Alfa AWUS036NHA / WN722N v1" "module_file" "ath9k_htc.ko"
check_config "CONFIG_CARL9170" "Atheros AR9170 802.11a/b/g/n Dual-Band" "module_file" "carl9170.ko"
check_config "CONFIG_CARL9170_LEDS" "Carl9170 LED activity indicators" "module_file" "carl9170.ko"
check_config "CONFIG_CARL9170_WPC" "Carl9170 Wi-Fi Protected Setup trigger" "module_file" "carl9170.ko"
check_config "CONFIG_ATH6KL" "Atheros AR6003 / AR6004 Mobile Driver" "module_file" "ath6kl_usb.ko"
check_config "CONFIG_ATH6KL_USB" "Atheros AR6003 USB Bus Interface" "module_file" "ath6kl_usb.ko"

# Ralink
check_config "CONFIG_WLAN_VENDOR_RALINK" "Ralink WLAN Vendor Support" "module_file" "rt2800usb.ko"
check_config "CONFIG_RT2X00" "Ralink rt2x00 Generic Stack" "module_file" "rt2x00lib.ko"
check_config "CONFIG_RT2500USB" "Ralink RT2500 USB Driver" "module_file" "rt2500usb.ko"
check_config "CONFIG_RT73USB" "Ralink RT73 / RT2571 USB Driver" "module_file" "rt73usb.ko"
check_config "CONFIG_RT2800USB" "Alfa AWUS036NH / RT3070 / RT5370" "module_file" "rt2800usb.ko"
check_config "CONFIG_RT2800USB_RT33XX" "Ralink RT33xx SoC / USB Support" "module_file" "rt2800usb.ko"
check_config "CONFIG_RT2800USB_RT35XX" "Ralink RT35xx USB Support" "module_file" "rt2800usb.ko"
check_config "CONFIG_RT2800USB_RT3573" "Ralink RT3573 Dual-band USB Support" "module_file" "rt2800usb.ko"
check_config "CONFIG_RT2800USB_RT53XX" "Ralink RT53xx USB Support" "module_file" "rt2800usb.ko"
check_config "CONFIG_RT2800USB_RT55XX" "Ralink RT55xx Dual-band USB Support" "module_file" "rt2800usb.ko"
check_config "CONFIG_RT2800USB_UNKNOWN" "Ralink Unknown / Generic Hardware IDs" "module_file" "rt2800usb.ko"

# MediaTek
check_config "CONFIG_WLAN_VENDOR_MEDIATEK" "MediaTek WLAN Vendor Support" "module_file" "mt7601u.ko"
check_config "CONFIG_MT7601U" "MediaTek MT7601U Mini USB Dongles" "module_file" "mt7601u.ko"
check_config "CONFIG_MT76_CORE" "MediaTek MT76 Core Driver Stack" "module_file" "mt76.ko"
check_config "CONFIG_MT76_USB" "MediaTek MT76 USB Subsystem" "module_file" "mt76_usb.ko"
check_config "CONFIG_MT76x02_LIB" "MediaTek MT76x02 Common Code" "module_file" "mt76x02_lib.ko"
check_config "CONFIG_MT76x02_USB" "MediaTek MT76x02 USB Common" "module_file" "mt76x02_usb.ko"
check_config "CONFIG_MT76x0U" "MediaTek MT7610U (AC600 Dual-Band)" "module_file" "mt76x0u.ko"
check_config "CONFIG_MT76x2_COMMON" "MediaTek MT76x2 Common Base" "module_file" "mt76x2_common.ko"
check_config "CONFIG_MT76x2U" "MediaTek MT7612U (Alfa AWUS036ACM / Panda PAU09)" "module_file" "mt76x2u.ko"

# ZyDAS
check_config "CONFIG_WLAN_VENDOR_ZYDAS" "ZyDAS WLAN Vendor Support" "module_file" "zd1211rw.ko"
check_config "CONFIG_ZD1211RW" "ZyDAS ZD1211 / ZD1211B USB Driver" "module_file" "zd1211rw.ko"

# ==============================================================================
# 6. USB ETHERNET & NETWORK DONGLES
# ==============================================================================
section_header "6. USB Ethernet Adapters"
check_config "CONFIG_USB_NET_DRIVERS" "USB Network Driver Subsystem" "module_file" "usbnet.ko"
check_config "CONFIG_USB_USBNET" "Generic USB Networking Core" "module_file" "usbnet.ko"
check_config "CONFIG_USB_NET_AX8817X" "ASIX AX8817x USB 2.0 10/100 Ethernet" "module_file" "asix.ko"
check_config "CONFIG_USB_NET_AX88179_178A" "ASIX AX88179 Gigabit USB 3.0 Ethernet" "module_file" "ax88179_178a.ko"
check_config "CONFIG_USB_NET_CDCETHER" "CDC-Ethernet generic USB adapters" "module_file" "cdc_ether.ko"
check_config "CONFIG_USB_NET_CDC_NCM" "CDC-NCM high-speed Gigabit adapters" "module_file" "cdc_ncm.ko"
check_config "CONFIG_USB_RTL8152" "Realtek RTL8152 (10/100) & RTL8153 (Gigabit)" "module_file" "r8152.ko"
check_config "CONFIG_USB_RTL8150" "Realtek RTL8150 USB Ethernet" "module_file" "rtl8150.ko"

# ==============================================================================
# 7. BLUETOOTH & BLUETOOTH ARSENAL
# ==============================================================================
section_header "7. Bluetooth & Bluetooth Arsenal"
check_config "CONFIG_BT" "Core Bluetooth Subsystem" "module_file" "bluetooth.ko"
check_config "CONFIG_BT_RFCOMM" "Bluetooth RFCOMM Protocol (TTY Emulation)" "module_file" "rfcomm.ko"
check_config "CONFIG_BT_RFCOMM_TTY" "RFCOMM TTY devices (/dev/rfcomm*)" "dev_node" "/dev/rfcomm*"
check_config "CONFIG_BT_BNEP" "Bluetooth BNEP (PAN / Network Pivoting)" "module_file" "bnep.ko"
check_config "CONFIG_BT_HIDP" "Bluetooth HIDP (BLE Keystroke Injection)" "module_file" "hidp.ko"
check_config "CONFIG_BT_HCIBTUSB" "Generic USB Bluetooth Dongles" "module_file" "btusb.ko"
check_config "CONFIG_BT_HCIBTUSB_BCM" "Broadcom USB Bluetooth Dongles" "module_file" "btusb.ko"
check_config "CONFIG_BT_HCIBTUSB_RTL" "Realtek USB Bluetooth Dongles" "module_file" "btusb.ko"
check_config "CONFIG_BT_HCIUART" "HCI UART Driver" "module_file" "hci_uart.ko"
check_config "CONFIG_BT_HCIUART_H4" "HCI UART H4 Protocol" "module_file" "hci_uart.ko"
check_config "CONFIG_BT_HCIBCM203X" "Broadcom BCM203x USB Bluetooth" "module_file" "bcm203x.ko"
check_config "CONFIG_BT_HCIBPA10X" "BPA10x USB Bluetooth" "module_file" "bpa10x.ko"
check_config "CONFIG_BT_HCIBFUSB" "BlueFRITZ! USB Bluetooth" "module_file" "bfusb.ko"
check_config "CONFIG_BT_HCIVHCI" "Virtual HCI (Userspace Packet Injection)" "module_file" "hci_vhci.ko"

# ==============================================================================
# 8. SOFTWARE-DEFINED RADIO (SDR)
# ==============================================================================
section_header "8. Software-Defined Radio (SDR)"
check_config "CONFIG_MEDIA_SUPPORT" "Linux Media & DVB Subsystem" "module_file" "media.ko"
check_config "CONFIG_MEDIA_DIGITAL_TV_SUPPORT" "Digital TV & SDR tuner support" "module_file" "dvb-core.ko"
check_config "CONFIG_MEDIA_SDR_SUPPORT" "Software-Defined Radio framework" "module_file" "dvb-core.ko"
check_config "CONFIG_MEDIA_USB_SUPPORT" "USB Media & Tuner support" "module_file" "dvb-core.ko"
check_config "CONFIG_DVB_CORE" "DVB Digital TV & Demodulator Core" "module_file" "dvb-core.ko"
check_config "CONFIG_DVB_USB_V2" "DVB USB v2 Driver Framework" "module_file" "dvb_usb_v2.ko"
check_config "CONFIG_DVB_USB_RTL28XXU" "RTL-SDR USB Dongles (RTL2832U)" "module_file" "dvb-usb-rtl28xxu.ko"
check_config "CONFIG_DVB_RTL2830" "RTL2830 DVB-T Demodulator" "module_file" "rtl2830.ko"
check_config "CONFIG_DVB_RTL2832" "RTL2832 DVB-T Demodulator" "module_file" "rtl2832.ko"
check_config "CONFIG_DVB_RTL2832_SDR" "RTL2832 SDR Tuner Extension" "module_file" "rtl2832_sdr.ko"
check_config "CONFIG_DVB_SI2168" "Silicon Labs Si2168 Demodulator" "module_file" "si2168.ko"
check_config "CONFIG_DVB_ZD1301_DEMOD" "ZyDAS ZD1301 Demodulator" "module_file" "zd1301_demod.ko"
check_config "CONFIG_USB_HACKRF" "HackRF One SDR (1 MHz - 6 GHz TX/RX)" "module_file" "hackrf.ko"
check_config "CONFIG_USB_AIRSPY" "AirSpy VHF/UHF SDR Receiver" "module_file" "airspy.ko"
check_config "CONFIG_USB_MSI2500" "Mirics MSi2500 / SDRplay USB Receiver" "module_file" "msi2500.ko"

# ==============================================================================
# 9. CAN BUS & AUTOMOTIVE HACKING (CARSENAL)
# ==============================================================================
section_header "9. CAN Bus & Automotive Hacking (CARsenal / SocketCAN)"
check_config "CONFIG_CAN" "Linux SocketCAN Core Protocol Stack" "module_file" "can.ko"
check_config "CONFIG_CAN_RAW" "Raw CAN Protocol (candump / cansend)" "module_file" "can-raw.ko"
check_config "CONFIG_CAN_BCM" "Broadcast Manager (cangen / packet floods)" "module_file" "can-bcm.ko"
check_config "CONFIG_CAN_GW" "CAN Gateway & Packet Routing" "module_file" "can-gw.ko"
check_config "CONFIG_CAN_DEV" "CAN Device Driver Framework" "module_file" "can-dev.ko"
check_config "CONFIG_CAN_CALC_BITTIMING" "Automatic Bit-rate Calculation" "module_file" "can-dev.ko"
check_config "CONFIG_LEDS_TRIGGER_NETDEV" "Network & CAN LED Activity Triggers" "dev_node" "/sys/class/leds"
check_config "CONFIG_CAN_VCAN" "Virtual CAN (vcan0 for offline analysis)" "module_file" "vcan.ko"
check_config "CONFIG_CAN_SLCAN" "Serial CAN / Lawicel ASCII (CANable)" "module_file" "slcan.ko"
check_config "CONFIG_CAN_EMS_USB" "EMS CPC-USB CAN Interface" "module_file" "ems_usb.ko"
check_config "CONFIG_CAN_KVASER_USB" "Kvaser USB CAN Adapter" "module_file" "kvaser_usb.ko"
check_config "CONFIG_CAN_PEAK_USB" "PEAK PCAN-USB / PCAN-USB Pro" "module_file" "peak_usb.ko"
check_config "CONFIG_CAN_8DEV_USB" "8devices USB2CAN Adapter" "module_file" "usb_8dev.ko"
check_config "CONFIG_CAN_GS_USB" "Geschwister Schneider (candleLight/gs_usb)" "module_file" "gs_usb.ko"

# ==============================================================================
# 10. NETWORK FILE SYSTEMS (NFS & CIFS/SMB)
# ==============================================================================
section_header "10. Network File Systems (NFS Client/Server & CIFS/SMB)"
check_config "CONFIG_NETWORK_FILESYSTEMS" "Network Filesystem Infrastructure" "fs" "nfs"
check_config "CONFIG_NFS_FS" "NFS Client (Remote Storage & Wordlists)" "fs" "nfs"
check_config "CONFIG_NFS_V2" "NFS Protocol v2 Support" "fs" "nfs"
check_config "CONFIG_NFS_V3" "NFS Protocol v3 Support" "fs" "nfs"
check_config "CONFIG_NFS_V3_ACL" "NFS Client v3 POSIX ACL Support" "fs" "nfs"
check_config "CONFIG_NFS_V4" "NFS Protocol v4 Support" "fs" "nfs4"
check_config "CONFIG_NFSD" "In-Kernel NFS Server (Android Exfiltration)" "fs" "nfsd"
check_config "CONFIG_NFSD_V3_ACL" "NFS Server v3 POSIX ACL Support" "fs" "nfsd"
check_config "CONFIG_NFSD_V4" "NFS Server v4 Support" "fs" "nfsd"
check_config "CONFIG_CIFS" "CIFS / SMB Client (Windows Network Shares)" "fs" "cifs"

# ==============================================================================
# 11. SYSTEM IPC & CHROOT ENHANCEMENTS
# ==============================================================================
section_header "11. System IPC & Kali Chroot Enhancements"
check_config "CONFIG_SYSVIPC" "System V IPC (Metasploit PostgreSQL / KeX)" "dev_node" "/proc/sysvipc"

# ==============================================================================
# 12. FIRMWARE BINARIES AUDIT
# ==============================================================================
section_header "12. NetHunter Firmware Blobs Verification"
check_firmware() {
    local fw_rel="$1"
    local fw_desc="$2"
    local found=0
    for prefix in /vendor/firmware /vendor/etc/firmware /system/etc/firmware /data/adb/modules/gki_nethunter_wireless/vendor/firmware /data/adb/modules/gki_nethunter_wireless/system/etc/firmware; do
        if [ -f "$prefix/$fw_rel" ]; then
            found=1
            break
        fi
    done
    if [ "$found" -eq 1 ]; then
        echo -e "  [ ${GREEN}✔ FIRMWARE PRESENT${NC} ] ${BOLD}$fw_rel${NC} (${CYAN}$fw_desc${NC})"
    else
        echo -e "  [ ${YELLOW}● NOT FOUND / UNLOADED${NC} ] ${BOLD}$fw_rel${NC} (${CYAN}$fw_desc${NC})"
    fi
}

check_firmware "rtw88/rtw8822c_fw.bin"  "Realtek RTL8822CU / RTL8822CE Firmware"
check_firmware "rtw88/rtw8822b_fw.bin"  "Realtek RTL8822B / RTL8812BU Firmware"
check_firmware "rtw88/rtw8821c_fw.bin"  "Realtek RTL8821CU / RTL8811CU Firmware"
check_firmware "rtw88/rtw8723d_fw.bin"  "Realtek RTL8723DU Firmware"
check_firmware "ath9k_htc/htc_9271.fw"  "Atheros AR9271 Firmware (TL-WN722N v1)"
check_firmware "carl9170-1.fw"          "Atheros AR9170 Dual-Band Firmware"
check_firmware "mediatek/mt7662u.bin"   "MediaTek MT7612U/MT7662U 5GHz Firmware (AWUS036ACM)"
check_firmware "mt7601u.bin"            "MediaTek MT7601U Mini Dongle Firmware"
check_firmware "rt2870.bin"             "Ralink RT2870/RT3070 Firmware (AWUS036NH)"
check_firmware "rtlwifi/rtl8192cufw.bin" "Realtek RTL8192CU Firmware"
check_firmware "rtlwifi/rtl8192eu_nic.bin" "Realtek RTL8192EU NIC Firmware"

# ==============================================================================
# 13. LIVE HARDWARE NODES & PERMISSIONS AUDIT
# ==============================================================================
section_header "13. Live Hardware Nodes & Permissions Status"
nodes_to_check="/dev/hidg0 /dev/hidg1 /dev/uhid /dev/rfkill /dev/net/tun /config/usb_gadget /dev/bus/usb /dev/ttyACM0 /dev/ttyUSB0"
for node in $nodes_to_check; do
    if [ -e "$node" ]; then
        perms=$(ls -ld "$node" 2>/dev/null | awk '{print $1, $3, $4}')
        echo -e "  [ ${GREEN}✔ NODE READY${NC} ] ${BOLD}$node${NC} (${CYAN}$perms${NC})"
    else
        echo -e "  [ ${YELLOW}● DORMANT${NC}    ] ${BOLD}$node${NC} (Activates dynamically when device attached)"
    fi
done

# Cleanup temporary config file
[ -f "$TEMP_CONFIG" ] && rm -f "$TEMP_CONFIG" 2>/dev/null || true

# ==============================================================================
# FINAL SUMMARY REPORT
# ==============================================================================
echo -e "\n${CYAN}${BOLD}================================================================${NC}"
echo -e "${CYAN}${BOLD}                 NETHUNTER SUMMARY REPORT                       ${NC}"
echo -e "${CYAN}${BOLD}================================================================${NC}"
echo -e "Total NetHunter Features Checked : ${BOLD}${TOTAL_CHECKED}${NC}"
echo -e "Built-in / Active                : ${GREEN}${BOLD}${PASSED_COUNT}${NC}"
echo -e "Modular (=m) Drivers             : ${YELLOW}${BOLD}${MODULE_COUNT}${NC}"
echo -e "Missing / Disabled               : ${RED}${BOLD}${FAILED_COUNT}${NC}"
echo -e "${CYAN}${BOLD}================================================================${NC}"

if [ "$FAILED_COUNT" -eq 0 ]; then
    echo -e "${GREEN}${BOLD}🎉 EXCELLENT: Your kernel has 100% Kali NetHunter feature coverage!${NC}\n"
else
    echo -e "${YELLOW}${BOLD}⚠ NOTE: Flash Nethunter-Wireless-Module.zip in KernelSU-Next / SukiSU-Ultra / ReSukiSU to load modular drivers.${NC}\n"
fi
