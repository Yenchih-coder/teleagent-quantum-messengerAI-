#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""zmx-quick-send.py - 量子密信快速发送脚本

纯坐标定位+键盘操作，无需截图确认，3-8秒完成发送。

Usage:
  python zmx-quick-send.py send <联系人> <消息>
  python zmx-quick-send.py file <联系人> <文件路径>
  python zmx-quick-send.py batch <配置文件>
  python zmx-quick-send.py check
"""

import sys
import os
import time
import subprocess
import ctypes
import ctypes.wintypes

# ── 依赖检查 ──
try:
    import pyautogui
except ImportError:
    print("ERROR: 缺少依赖 pyautogui，请运行: pip install pyautogui")
    sys.exit(1)

# ── Windows API ──
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

SW_SHOW = 5
SW_RESTORE = 9
SW_MAXIMIZE = 3

# ── 量子密信窗口特征 ──
ZMX_TITLE = "量子密信"
ZMX_CLASS = "Chrome_WidgetWin_1"
ZMX_EXE = r"D:\lzmx\zdxlz-app\量子密信.exe"

# ── 坐标比例（AI视觉校准 2026-07-29，最大化后） ──
SEARCH_X = 0.073
SEARCH_Y = 0.07
RESULT_X = 0.12
RESULT_Y = 0.16
INPUT_X = 0.52
INPUT_Y = 0.905

# ── 时序参数（秒） ──
SEARCH_WAIT = 4       # 搜索等待（量子密信一般2秒返回，4秒留余量）
CHAT_LOAD_WAIT = 2    # 进入聊天等待
SEND_WAIT = 0.3       # 发送后等待
BATCH_INTERVAL = 2.5  # 批量发送间隔

# ── pyautogui 设置 ──
pyautogui.PAUSE = 0.15
pyautogui.FAILSAFE = True


# ═══════════════════════════════════════════════════
#  窗口操作
# ═══════════════════════════════════════════════════

def _find_hwnd():
    """查找量子密信窗口句柄"""
    hwnd = user32.FindWindowW(ZMX_CLASS, ZMX_TITLE)
    if hwnd:
        return hwnd
    hwnd = user32.FindWindowW(None, ZMX_TITLE)
    if hwnd:
        return hwnd
    return 0


def _activate():
    """激活量子密信窗口：找不到则启动，最小化则恢复，然后最大化+置前"""
    hwnd = _find_hwnd()

    if not hwnd:
        if os.path.exists(ZMX_EXE):
            os.startfile(ZMX_EXE)
            for _ in range(30):
                time.sleep(0.5)
                hwnd = _find_hwnd()
                if hwnd:
                    break
        if not hwnd:
            print("ERROR: 量子密信窗口未找到，请确认已安装并登录")
            return 0

    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, SW_RESTORE)
        time.sleep(0.2)

    user32.ShowWindow(hwnd, SW_MAXIMIZE)
    time.sleep(0.2)

    result = user32.SetForegroundWindow(hwnd)
    if not result:
        fg = user32.GetForegroundWindow()
        fg_tid = user32.GetWindowThreadProcessId(fg, None)
        cur_tid = kernel32.GetCurrentThreadId()
        user32.AttachThreadInput(fg_tid, cur_tid, True)
        user32.SetForegroundWindow(hwnd)
        user32.AttachThreadInput(fg_tid, cur_tid, False)
    time.sleep(0.3)

    return hwnd


def _click_ratio(hwnd, x_ratio, y_ratio):
    """按窗口比例坐标点击"""
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    x = rect.left + int((rect.right - rect.left) * x_ratio)
    y = rect.top + int((rect.bottom - rect.top) * y_ratio)
    pyautogui.click(x, y)


def _clipboard_set(text):
    """用PowerShell设置剪贴板文本"""
    tmp = os.path.join(os.environ.get("TEMP", "."), "_zmx_q.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    ps = (
        f"$t = Get-Content -Path '{tmp}' -Encoding UTF8 -Raw; "
        f"Set-Clipboard -Value $t; Remove-Item '{tmp}' -Force"
    )
    subprocess.run(["powershell", "-Command", ps], capture_output=True)
    time.sleep(0.1)


def _clipboard_set_file(file_path):
    """用PowerShell将文件放入剪贴板（SetFileDropList）"""
    abs_path = os.path.abspath(file_path)
    ps = (
        f"Add-Type -AssemblyName System.Windows.Forms; "
        f"$files = New-Object System.Collections.Specialized.StringCollection; "
        f"$files.Add('{abs_path}') | Out-Null; "
        f"[System.Windows.Forms.Clipboard]::SetFileDropList($files)"
    )
    subprocess.run(["powershell", "-Command", ps], capture_output=True)
    time.sleep(0.2)


# ═══════════════════════════════════════════════════
#  核心流程
# ═══════════════════════════════════════════════════

def _search_contact(hwnd, name):
    """搜索联系人：点击搜索框 → 粘贴名称 → 等待"""
    _click_ratio(hwnd, SEARCH_X, SEARCH_Y)
    time.sleep(0.2)

    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)

    _clipboard_set(name)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(SEARCH_WAIT)


def _enter_chat(hwnd):
    """点击搜索结果第一条，进入聊天"""
    _click_ratio(hwnd, RESULT_X, RESULT_Y)
    time.sleep(CHAT_LOAD_WAIT)


def _send_text(hwnd, message):
    """在当前聊天窗口发送文本消息"""
    _click_ratio(hwnd, INPUT_X, INPUT_Y)
    time.sleep(0.2)

    _clipboard_set(message)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(SEND_WAIT)


def _send_file(hwnd, file_path):
    """在当前聊天窗口发送文件"""
    if not os.path.isfile(file_path):
        print(f"ERROR: 文件不存在: {file_path}")
        return False

    _click_ratio(hwnd, INPUT_X, INPUT_Y)
    time.sleep(0.2)

    _clipboard_set_file(file_path)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(2)

    pyautogui.press("enter")
    time.sleep(1)

    return True


# ═══════════════════════════════════════════════════
#  命令入口
# ═══════════════════════════════════════════════════

def cmd_check():
    """检查量子密信窗口状态"""
    hwnd = _find_hwnd()
    if hwnd:
        visible = user32.IsWindowVisible(hwnd)
        iconic = user32.IsIconic(hwnd)
        status = "最小化" if iconic else ("可见" if visible else "隐藏")
        print(f"OK: 量子密信正在运行 (hwnd={hwnd}, 状态={status})")
    else:
        print("WARN: 量子密信未运行，执行send/file命令时会自动启动")


def cmd_send(contact, message):
    """一键发送消息：激活→搜索→进入聊天→发送"""
    hwnd = _activate()
    if not hwnd:
        return

    _search_contact(hwnd, contact)
    _enter_chat(hwnd)
    _send_text(hwnd, message)

    print(f"OK: 已向 '{contact}' 发送消息: {message[:50]}{'...' if len(message) > 50 else ''}")


def cmd_file(contact, file_path):
    """一键发送文件：激活→搜索→进入聊天→发文件"""
    if not os.path.isfile(file_path):
        print(f"ERROR: 文件不存在: {file_path}")
        return

    hwnd = _activate()
    if not hwnd:
        return

    _search_contact(hwnd, contact)
    _enter_chat(hwnd)
    _send_file(hwnd, file_path)

    print(f"OK: 已向 '{contact}' 发送文件: {os.path.basename(file_path)}")


def cmd_batch(config_path):
    """批量发送：从配置文件读取联系人|消息，逐条发送"""
    if not os.path.isfile(config_path):
        print(f"ERROR: 配置文件不存在: {config_path}")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip() and "|" in l]

    if not lines:
        print("ERROR: 配置文件为空或格式不正确（每行格式：联系人|消息）")
        return

    print(f"INFO: 共 {len(lines)} 条待发送")

    hwnd = _activate()
    if not hwnd:
        return

    for i, line in enumerate(lines, 1):
        contact, message = line.split("|", 1)
        contact = contact.strip()
        message = message.strip()

        _search_contact(hwnd, contact)
        _enter_chat(hwnd)
        _send_text(hwnd, message)

        print(f"OK: [{i}/{len(lines)}] 已向 '{contact}' 发送: {message[:30]}")

        if i < len(lines):
            time.sleep(BATCH_INTERVAL)

    print(f"OK: 批量发送完成，共 {len(lines)} 条")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "check":
        cmd_check()
    elif cmd == "send":
        if len(sys.argv) < 4:
            print("ERROR: 用法: zmx-quick-send.py send <联系人> <消息>")
            sys.exit(1)
        cmd_send(sys.argv[2], sys.argv[3])
    elif cmd == "file":
        if len(sys.argv) < 4:
            print("ERROR: 用法: zmx-quick-send.py file <联系人> <文件路径>")
            sys.exit(1)
        cmd_file(sys.argv[2], sys.argv[3])
    elif cmd == "batch":
        if len(sys.argv) < 3:
            print("ERROR: 用法: zmx-quick-send.py batch <配置文件>")
            sys.exit(1)
        cmd_batch(sys.argv[2])
    else:
        print(f"ERROR: 未知命令 '{cmd}'")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
