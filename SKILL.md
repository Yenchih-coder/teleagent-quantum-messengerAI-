---
name: zmx-quick-send
description: Automate Quantum Secure Messaging (量子密信) PC desktop to quickly search contacts and send personal messages or files via pure coordinate-based automation. Trigger when user mentions "量子密信快速发送", "量子密信发消息", "量子密信发文件", "给XX发量子密信", "ZMX quick send", or asks to send messages/files via 量子密信 with speed priority. Only supports 量子密信 PC desktop version on Windows.
name_cn: 量子密信快速私聊
description_cn: 通过量子密信PC桌面版快速搜索联系人并发送消息/文件，纯坐标定位，无需截图确认
---

# 量子密信快速私聊

通过量子密信PC桌面版快速搜索联系人并发送消息/文件。纯坐标定位+键盘操作，无需截图确认，约10秒完成。

## 核心特点

- 信任模式：纯坐标定位+键盘操作，无截图/AI视觉确认
- 单脚本全流程：一次python启动完成搜索→进入聊天→发送
- 量子密信无广告，搜索结果即目标，无需二次确认
- 操作前自动最大化窗口，确保比例定位稳定

## 界面坐标（AI视觉校准 2026-07-29，最大化后）

| 区域 | X | Y | 说明 |
|------|---|---|------|
| 搜索框 | 0.073 | 0.07 | 左上角，含放大镜图标 |
| 搜索结果 | 0.12 | 0.16 | 第一条联系人 |
| 聊天输入框 | 0.52 | 0.905 | 右下区域 |

## 脚本命令

```bash
python scripts/zmx-quick-send.py send <联系人> <消息>      # 一键发送消息
python scripts/zmx-quick-send.py file <联系人> <文件路径>   # 一键发送文件
python scripts/zmx-quick-send.py batch <配置文件>           # 批量发送
python scripts/zmx-quick-send.py check                     # 检查窗口状态
```

## 操作流程

### 发消息

```bash
python scripts/zmx-quick-send.py send 田志羿 你好
```

内部流程：激活窗口 → 点击搜索框 → 粘贴联系人 → 等待4秒 → 点击搜索结果 → 等待2秒 → 粘贴消息 → Enter发送

### 发文件

```bash
python scripts/zmx-quick-send.py file 田志羿 D:\报表.xlsx
```

内部流程：激活窗口 → 搜索联系人 → 进入聊天 → 剪贴板设置文件引用 → Ctrl+V粘贴 → Enter发送

### 批量发送

配置文件格式（每行：联系人|消息）：

```
田志羿|请查收报表
李明|会议已确认
```

```bash
python scripts/zmx-quick-send.py batch D:\发送列表.txt
```

## 依赖

```bash
pip install pyautogui
```

## 注意事项

- 窗口类名 Chrome_WidgetWin_1（Electron通用），按标题"量子密信"匹配
- 量子密信未运行时脚本会自动启动（需已登录状态）
- 发送速度：约4-10秒/条（含搜索等待4秒）
- 批量发送时每条间隔2.5秒，避免操作过快
