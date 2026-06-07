# Seqora Entry Point

我的个人资源入口和可下载 Codex skills 仓库。这里收集常用网站、工具、学习资料，以及可以直接安装到 Codex 的自定义 skill。

## Skills

### Serenity Research Posts

从 Serenity 公开 posts 样本中提炼出的研究帖工作流 skill。它适合把 AI、半导体、供应链、硬件瓶颈、tickers、催化剂和粗略 notes 转换成结构清晰的 X/Twitter 风格研究帖。

Skill 路径：

```text
skills/serenity-research-posts
```

下载包：

```text
dist/serenity-research-posts.zip
```

GitHub raw 下载链接：

```text
https://github.com/TuojianLYU/SeqoraEntryPoint/raw/main/dist/serenity-research-posts.zip
```

PowerShell 安装：

```powershell
Invoke-WebRequest -Uri "https://github.com/TuojianLYU/SeqoraEntryPoint/raw/main/dist/serenity-research-posts.zip" -OutFile "serenity-research-posts.zip"
Expand-Archive -Path "serenity-research-posts.zip" -DestinationPath "$env:USERPROFILE\.codex\skills" -Force
```

安装后可以这样调用：

```text
Use $serenity-research-posts to turn my notes into a rigorous AI/semi supply-chain research post.
```

说明：这个 skill 不用于冒充 Serenity，也不复制原帖。它只复用公开样本中可泛化的研究结构：催化剂、证据链、技术机制、财务锚点、风险披露和 TLDR。

## 网站 Websites

| 名称 | 链接 | 说明 |
|------|------|------|
| _示例_ | https://example.com | 这里填写说明 |

## 工具 Tools

| 名称 | 链接 | 说明 |
|------|------|------|
| 动态效果生成器 | https://vibe-motion-web-zeta.vercel.app/ | 快速生成适合视频剪辑、日常工作汇报的专业动态效果 |
| 工控探险工坊 | https://factory-quest.vercel.app/ | 用搭建一座工厂的方式，理解 PLC、I/O、Runtime 和工程流程 |

## 学习资源 Learning

| 名称 | 链接 | 说明 |
|------|------|------|
| _示例_ | https://example.com | 这里填写说明 |

## 灵感 / 笔记 Notes

- _在这里添加你的笔记_

## 其他 Others

| 名称 | 链接 | 说明 |
|------|------|------|
| _示例_ | https://example.com | 这里填写说明 |

_最后更新：2026-06-07_
