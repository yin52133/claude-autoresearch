English | [中文](README_CN.md)

# Claude Autoresearch

面向 [Claude Code](https://claude.ai/claude-code) 的自主目标驱动实验框架。告诉它你想改进什么，然后放手——它会修改代码、验证结果、保留或丢弃变更，然后重复。

本项目改编自 [codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch)，适配 Claude Code 的插件架构。

## 功能特性

- **自主循环**：修改 → 提交 → 验证 → 保留/丢弃 → 重复
- **三种模式**：loop（指标驱动）、debug（假设驱动）、fix（错误计数）
- **升级策略**：精炼 → 转换 → 网络搜索 → 停止（遇到瓶颈时）
- **会话恢复**：hooks 检测活跃的运行并在重启时注入上下文
- **完整审计**：每次迭代都记录到 `autoresearch-results/results.tsv`
- **守护命令**：确保现有测试始终通过，防止回归

## 安装

### 前置要求

- [Claude Code CLI](https://claude.ai/claude-code) 已安装
- Python 3.8+
- Git

### 作为插件安装

```bash
claude plugin add /path/to/claude-autoresearch
```

或克隆后安装：

```bash
git clone https://github.com/yin52133/claude-autoresearch.git
claude plugin add ./claude-autoresearch
```

## 使用方法

### 快速开始

在任何 Claude Code 会话中：

```
/autoresearch 将测试覆盖率提高到 80%
```

交互向导将：
1. 扫描你的代码仓库
2. 确认目标和指标
3. 测量基线
4. 等待确认 "go"
5. 运行自主循环

### 模式

**Loop 模式** — 驱动可测量指标：
```
/autoresearch 将 lint 警告减少到零
/autoresearch 将类型覆盖率提高到 95%
```

**Debug 模式** — 调查 bug：
```
/autoresearch 调试缓存模块的内存泄漏
```

**Fix 模式** — 消除错误：
```
/autoresearch 修复所有 TypeScript 编译错误
```

### 结果

所有结果存储在 `autoresearch-results/` 中：

| 文件 | 用途 |
|---|---|
| `results.tsv` | 迭代日志 |
| `state.json` | 当前运行状态 |
| `lessons.md` | 跨运行学习记录 |

### 状态管理

```bash
# 检查是否有活跃的运行
python3 scripts/autoresearch_state.py check

# 获取运行摘要
python3 scripts/autoresearch_state.py summary

# 暂停/恢复/完成
python3 scripts/autoresearch_state.py pause
python3 scripts/autoresearch_state.py resume
python3 scripts/autoresearch_state.py complete
```

## 工作原理

### 两阶段边界

**阶段一 — 交互式**：向导确认目标、指标和验证命令。这是唯一会提问的阶段。

**阶段二 — 自主式**：确认 "go" 后，Claude 无需人工干预运行循环。每次迭代做一个聚焦的改动并进行机械化验证。

### 升级策略

| 触发条件 | 动作 |
|---|---|
| 连续 3 次丢弃 | **精炼** — 在当前策略内调整 |
| 连续 5 次非保留 | **转换** — 根本性不同的方法 |
| 2 次转换无改进 | **网络搜索** — 寻找外部方案 |
| 3 次转换无改进 | **停止** — 报告给用户 |

### Hooks

插件使用三个 Claude Code hooks：

- **SessionStart**：检测活跃运行并提供恢复上下文
- **PostToolUse**：监控迭代进度并检测停滞
- **Stop**：在存在活跃运行时退出前警告

## 致谢

本项目改编自 [codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch)，由 [leo-lilinxiao](https://github.com/leo-lilinxiao) 开发。我们衷心感谢原作者的优秀设计和实现。

## 许可证

[MIT](LICENSE)
