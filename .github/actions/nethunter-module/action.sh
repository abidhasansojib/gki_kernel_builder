#!/system/bin/sh
MODDIR=${0%/*}

echo "=========================================="
echo "              Kernel Manager              "
echo "=========================================="

# 1. Sync latest WebUI to internal storage
mkdir -p /storage/emulated/0 /storage/emulated/0/Download 2>/dev/null || true
if [ -f "$MODDIR/webroot/index.html" ]; then
  cp -f "$MODDIR/webroot/index.html" /storage/emulated/0/nethunter_webui.html 2>/dev/null || true
  cp -f "$MODDIR/webroot/index.html" /storage/emulated/0/Download/nethunter_webui.html 2>/dev/null || true
  chmod 666 /storage/emulated/0/nethunter_webui.html /storage/emulated/0/Download/nethunter_webui.html 2>/dev/null || true
fi

# 2. Launch WebUI in browser / system viewer
echo "[*] Opening Kernel Manager WebUI..."
am start -a android.intent.action.VIEW -d "file:///data/adb/modules/nethunter_wireless_modules/webroot/index.html" -t "text/html" 2>/dev/null || \
am start -a android.intent.action.VIEW -d "file:///storage/emulated/0/nethunter_webui.html" -t "text/html" 2>/dev/null || \
am start -a android.intent.action.VIEW -d "file:///storage/emulated/0/nethunter_webui.html" 2>/dev/null || true

# 3. Output quick diagnostics
echo ""
echo "[+] Kernel Release: $(uname -r 2>/dev/null || echo 'Unknown')"
echo "[+] Active CPU Governor: $(cat /sys/devices/system/cpu/cpufreq/policy0/scaling_governor 2>/dev/null || cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo 'Unknown')"
echo "[+] TCP Congestion Control: $(cat /proc/sys/net/ipv4/tcp_congestion_control 2>/dev/null || echo 'Unknown')"
echo "[+] Active Qdisc: $(cat /proc/sys/net/core/default_qdisc 2>/dev/null || echo 'Unknown')"
echo "[+] MGLRU Capabilities: $(cat /sys/kernel/mm/lru_gen/enabled 2>/dev/null || echo 'Not Supported')"
echo ""
echo "[*] WebUI Location: /storage/emulated/0/nethunter_webui.html"
echo "=========================================="
