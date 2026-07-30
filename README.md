# teleagent-quantum-messengerAI

An AI agent skill that automates Quantum Secure Messaging (量子密信) desktop via [TeleAgent](https://github.com/Yenchih-coder/teleagent-quantum-messengerAI-). Supports sending messages, images, and files to contacts through coordinate-based UI automation — no API or official SDK required.

一个 AI 智能体技能，通过 TeleAgent 控制量子密信 PC 桌面版自动发送消息、图片和文件。基于坐标定位的 UI 自动化，无需 API 或官方 SDK。

## Features

- Send text messages to any contact
- Send files (documents, images, etc.) to any contact
- Batch sending to multiple contacts
- Pure coordinate-based automation, no screenshot confirmation needed
- ~10 seconds per send (vs ~70 seconds with AI vision confirmation)
- Auto-activate and maximize the Quantum Messaging window
- Auto-launch Quantum Messaging if not running

## Prerequisites

- Windows 10/11
- [Quantum Secure Messaging (量子密信)](https://zdxlz.com/) PC desktop version installed and logged in
- Python 3.8+
- [TeleAgent](https://github.com/Yenchih-coder/) (AI agent platform)

## Installation

1. Clone this repository into your TeleAgent skills directory:

```bash
git clone https://github.com/Yenchih-coder/teleagent-quantum-messengerAI-.git ~/.config/TeleAgent/skills/zmx-quick-send
```

2. Install Python dependencies:

```bash
pip install pyautogui
```

3. Register the skill with TeleAgent (restart TeleAgent to take effect).

## Usage

### Send a message

```bash
python scripts/zmx-quick-send.py send <contact> <message>
```

Example:

```bash
python scripts/zmx-quick-send.py send 田志羿 你好，请查收报表
```

### Send a file

```bash
python scripts/zmx-quick-send.py file <contact> <filepath>
```

Example:

```bash
python scripts/zmx-quick-send.py file 田志羿 D:\reports\报表.xlsx
```

### Batch sending

Create a text file with one entry per line in the format `contact|message`:

```
田志羿|请查收本周报表
李明|会议时间已确认
```

```bash
python scripts/zmx-quick-send.py batch D:\send_list.txt
```

### Check status

```bash
python scripts/zmx-quick-send.py check
```

## How It Works

1. **Activate** — Find or launch the Quantum Messaging window, maximize it
2. **Search** — Click the search box (coordinate ratio 0.073, 0.07), paste the contact name, wait 4 seconds
3. **Enter chat** — Click the first search result (0.12, 0.16), wait 2 seconds
4. **Send** — Click the input box (0.52, 0.905), paste message/file, press Enter

All coordinates are **ratio-based** (relative to window size), so they adapt to different screen resolutions after maximizing the window.

## Configuration

Edit these constants in `scripts/zmx-quick-send.py` if needed:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ZMX_EXE` | `D:\lzmx\zdxlz-app\量子密信.exe` | Path to Quantum Messaging executable |
| `SEARCH_WAIT` | 4 | Seconds to wait for search results |
| `CHAT_LOAD_WAIT` | 2 | Seconds to wait for chat to load |
| `BATCH_INTERVAL` | 2.5 | Seconds between batch sends |

## Coordinate Calibration

If clicks miss the target (e.g. after a Quantum Messaging UI update), recalibrate by:

1. Maximize the Quantum Messaging window
2. Note the click position ratios for: search box, first search result, chat input box
3. Update the constants at the top of `scripts/zmx-quick-send.py`

## License

[MIT](LICENSE)
