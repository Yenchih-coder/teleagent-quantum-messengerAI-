---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: 'cb2e414f-78bf-41a9-acee-89a48986747b'
  PropagateID: 'cb2e414f-78bf-41a9-acee-89a48986747b'
  ReservedCode1: 'b8badbe1-066d-4b55-a444-e4aad009cf70'
  ReservedCode2: 'b8badbe1-066d-4b55-a444-e4aad009cf70'
---

# teleagent-quantum-messengerAI

An AI agent skill that automates Quantum Secure Messaging (量子密信) desktop via [TeleAgent](https://github.com/Yenchih-coder/teleagent-quantum-messengerAI-). Supports sending messages, images, and files to contacts through coordinate-based UI automation — no API or official SDK required.

一个 AI 智能体技能，通过 TeleAgent 控制量子密信 PC 桌面版自动发送消息、图片和文件。基于坐标定位的 UI 自动化，无需 API 或官方 SDK。

## Features / 功能特性

- Send text messages to any contact / 向任意联系人发送文本消息
- Send files (documents, images, etc.) to any contact / 向任意联系人发送文件（文档、图片等）
- Batch sending to multiple contacts / 批量向多个联系人发送
- Pure coordinate-based automation, no screenshot confirmation needed / 纯坐标定位自动化，无需截图确认
- ~10 seconds per send (vs ~70 seconds with AI vision confirmation) / 每次发送约10秒（AI视觉确认模式需约70秒）
- Auto-activate and maximize the Quantum Messaging window / 自动激活并最大化量子密信窗口
- Auto-launch Quantum Messaging if not running / 量子密信未运行时自动启动

## Prerequisites / 前置条件

- Windows 10/11
- [Quantum Secure Messaging (量子密信)](https://zdxlz.com/) PC desktop version installed and logged in / 量子密信 PC 桌面版已安装并登录
- Python 3.8+
- [TeleAgent](https://github.com/Yenchih-coder/) (AI agent platform / AI 智能体平台)

## Installation / 安装

1. Clone this repository into your TeleAgent skills directory / 将此仓库克隆到 TeleAgent 技能目录：

```bash
git clone https://github.com/Yenchih-coder/teleagent-quantum-messengerAI-.git ~/.config/TeleAgent/skills/zmx-quick-send
```

2. Install Python dependencies / 安装 Python 依赖：

```bash
pip install pyautogui
```

3. Register the skill with TeleAgent (restart TeleAgent to take effect) / 注册技能到 TeleAgent（重启后生效）。

## Usage / 使用方法

### Send a message / 发送消息

```bash
python scripts/zmx-quick-send.py send <contact> <message>
```

Example / 示例：

```bash
python scripts/zmx-quick-send.py send 田志羿 你好，请查收报表
```

### Send a file / 发送文件

```bash
python scripts/zmx-quick-send.py file <contact> <filepath>
```

Example / 示例：

```bash
python scripts/zmx-quick-send.py file 田志羿 D:\reports\报表.xlsx
```

### Batch sending / 批量发送

Create a text file with one entry per line in the format `contact|message` / 创建一个文本文件，每行格式为 `联系人|消息`：

```
田志羿|请查收本周报表
李明|会议时间已确认
```

```bash
python scripts/zmx-quick-send.py batch D:\send_list.txt
```

### Check status / 检查状态

```bash
python scripts/zmx-quick-send.py check
```

## How It Works / 工作原理

1. **Activate** — Find or launch the Quantum Messaging window, maximize it / 激活 — 查找或启动量子密信窗口并最大化
2. **Search** — Click the search box (coordinate ratio 0.073, 0.07), paste the contact name, wait 4 seconds / 搜索 — 点击搜索框（坐标比例 0.073, 0.07），粘贴联系人名称，等待4秒
3. **Enter chat** — Click the first search result (0.12, 0.16), wait 2 seconds / 进入聊天 — 点击第一条搜索结果（0.12, 0.16），等待2秒
4. **Send** — Click the input box (0.52, 0.905), paste message/file, press Enter / 发送 — 点击输入框（0.52, 0.905），粘贴消息/文件，按回车

All coordinates are **ratio-based** (relative to window size), so they adapt to different screen resolutions after maximizing the window. / 所有坐标均为**比例坐标**（相对于窗口尺寸），最大化窗口后可自适应不同分辨率。

## Configuration / 配置

Edit these constants in `scripts/zmx-quick-send.py` if needed / 按需修改 `scripts/zmx-quick-send.py` 中的常量：

| Parameter | Default | Description / 说明 |
|-----------|---------|-------------|
| `ZMX_EXE` | `D:\lzmx\zdxlz-app\量子密信.exe` | Path to Quantum Messaging executable / 量子密信可执行文件路径 |
| `SEARCH_WAIT` | 4 | Seconds to wait for search results / 搜索结果等待秒数 |
| `CHAT_LOAD_WAIT` | 2 | Seconds to wait for chat to load / 聊天加载等待秒数 |
| `BATCH_INTERVAL` | 2.5 | Seconds between batch sends / 批量发送间隔秒数 |

## Coordinate Calibration / 坐标校准

If clicks miss the target (e.g. after a Quantum Messaging UI update), recalibrate by / 如果点击位置偏移（例如量子密信更新了 UI），按以下步骤重新校准：

1. Maximize the Quantum Messaging window / 最大化量子密信窗口
2. Note the click position ratios for: search box, first search result, chat input box / 记录以下区域的点击位置比例：搜索框、第一条搜索结果、聊天输入框
3. Update the constants at the top of `scripts/zmx-quick-send.py` / 更新 `scripts/zmx-quick-send.py` 顶部的常量

## License / 许可证

[MIT](LICENSE)

> AI生成