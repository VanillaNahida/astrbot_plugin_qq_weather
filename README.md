# QQ天气

![:name](https://count.getloli.com/@astrbot_plugin_qq_weather?name=astrbot_plugin_qq_weather&theme=minecraft&padding=6&offset=0&align=top&scale=1&pixelated=1&darkmode=auto)

一个基于腾讯天气接口的天气查询插件，无需额外配置即可查询全国天气，并支持显示近七日天气及限行信息等。

<p align="center">
  <img src="logo.png" alt="logo">
</p>

<div align="center">

  [![GitHub license](https://img.shields.io/github/license/VanillaNahida/astrbot_plugin_qq_weather?style=flat-square)](https://github.com/VanillaNahida/astrbot_plugin_qq_weather/blob/main/LICENSE)
  [![GitHub stars](https://img.shields.io/github/stars/VanillaNahida/astrbot_plugin_qq_weather?style=flat-square)](https://github.com/VanillaNahida/astrbot_plugin_qq_weather/stargazers)
  [![GitHub forks](https://img.shields.io/github/forks/VanillaNahida/astrbot_plugin_qq_weather?style=flat-square)](https://github.com/VanillaNahida/astrbot_plugin_qq_weather/network)
  [![GitHub issues](https://img.shields.io/github/issues/VanillaNahida/astrbot_plugin_qq_weather?style=flat-square)](https://github.com/VanillaNahida/astrbot_plugin_qq_weather/issues)
  [![python3](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square)](https://www.python.org/)
  [![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-brightgreen.svg?style=flat-square)]()
  [![Author](https://img.shields.io/badge/%E4%BD%9C%E8%80%85-VanillaNahida-green)](https://github.com/VanillaNahida)


</div>

# 功能特性

- **精准的天气数据**：天气数据来源于中央气象台，实时更新，覆盖全国各省市区，精准无误。
- **省市区自动精准匹配**：支持省/市/区多级地区查询，自动精准匹配。

# 使用方法

## 安装

1. 在 AstrBot WebUI 插件市场搜索 `astrbot_plugin_qq_weather` 或 `QQ天气`
2. 点击安装插件
3. 或者通过仓库地址安装：复制 `https://github.com/VanillaNahida/astrbot_plugin_qq_weather` 粘贴到 WebUI 安装

## 环境依赖

插件依赖 Playwright 和 Chromium 浏览器。安装完成后，请在 AstrBot 运行环境中执行下面命令：

```bash
pip install playwright
playwright install chromium
```
插件启动时会自动检测依赖状态，若未安装依赖会在日志和会话中提示。

## 使用

发送下面的命令查询天气：

```
| 命令 | 示例用法 | 说明 |
|------|------|------|
| `/天气` | `/天气 广州` | 城市名查询示例 |
| `/天气` | `/天气 松江` | 区名查询示例   |
| `/天气` | `/天气 阳新` | 县名查询示例   |
```

# 命令总览

| 命令 | 示例用法 | 说明 |
|------|------|------|
| `/天气` | `/天气 广州` | 查询指定城市的天气，返回腾讯天气页面截图 |

# Bug 反馈

如果在使用过程中遇到任何问题，请通过以下方式反馈：

- [GitHub Issues](https://github.com/VanillaNahida/astrbot_plugin_qq_weather/issues)
- QQ群：
  - 三群：195260107（推荐）
  - 四群：1074471035（闲聊群）

# QQ 群

- 一群：621457510
- 二群：1031065631
- 三群：195260107（推荐）
- 四群：1074471035

# Star History

[![Star History Chart](https://api.star-history.com/svg?repos=VanillaNahida/astrbot_plugin_qq_weather&type=Date)](https://star-history.com/#VanillaNahida/astrbot_plugin_qq_weather&Date)
