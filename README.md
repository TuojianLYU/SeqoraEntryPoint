# Seqora Entry Point

我的个人资源入口：集中管理常用网站、Web 小工具、学习资源、Codex skills 和零散笔记。

这个仓库的 README 是主目录页；资源本体可以放在对应文件夹里，例如 `skills/`、`dist/`，外部项目则直接记录链接。

## 目录

- [Skills](#skills)
- [工具 Tools](#工具-tools)
- [网站 Websites](#网站-websites)
- [学习资源 Learning](#学习资源-learning)
- [灵感 / 笔记 Notes](#灵感--笔记-notes)
- [其他 Others](#其他-others)
- [维护规则](#维护规则)

## Skills

Codex / agent skills 放在这里统一索引。源码放在 `skills/<skill-name>/`，可下载包放在 `dist/`。

| 名称 | 路径 | 下载 | 用途 |
|------|------|------|------|
| Serenity Market Strategy | `skills/serenity-market-strategy` | [zip](https://github.com/TuojianLYU/SeqoraEntryPoint/raw/main/dist/serenity-market-strategy.zip) | 用 Serenity 启发的投资研究框架分析市场方向、标的、AI/半导体供应链瓶颈、隐藏受益方、催化剂、错价和风险 |

### Skill 安装示例

PowerShell:

```powershell
Invoke-WebRequest -Uri "https://github.com/TuojianLYU/SeqoraEntryPoint/raw/main/dist/serenity-market-strategy.zip" -OutFile "serenity-market-strategy.zip"
Expand-Archive -Path "serenity-market-strategy.zip" -DestinationPath "$env:USERPROFILE\.codex\skills" -Force
```

调用示例：

```text
Use $serenity-market-strategy to analyze NVDA, MRVL, AAOI, and the broader AI semi setup through bottlenecks, catalysts, materiality, and risks.
```

## 工具 Tools

自己做的 Web 小工具、实用在线工具、自动化小应用等。

| 名称 | 链接 | 说明 |
|------|------|------|
| 动态效果生成器 | https://vibe-motion-web-zeta.vercel.app/ | 快速生成适合视频剪辑、日常工作汇报的专业动态效果 |
| 工控探险工坊 | https://factory-quest.vercel.app/ | 用搭建一座工厂的方式，理解 PLC、I/O、Runtime 和工程流程 |

## 网站 Websites

常用网站、收藏链接、入口站点。

| 名称 | 链接 | 说明 |
|------|------|------|
| _待添加_ | https://example.com | 这里填写说明 |

## 学习资源 Learning

教程、文档、课程、书籍、文章合集。

| 名称 | 链接 | 说明 |
|------|------|------|
| _待添加_ | https://example.com | 这里填写说明 |

## 灵感 / 笔记 Notes

随手记录的想法、片段、备忘。

- _在这里添加你的笔记_

## 其他 Others

暂未分类的内容。

| 名称 | 链接 | 说明 |
|------|------|------|
| _待添加_ | https://example.com | 这里填写说明 |

## 维护规则

新增资源时优先放到对应分类表格里，保持一行一个资源。

| 类型 | 放置位置 | 记录方式 |
|------|----------|----------|
| Codex skill | `skills/<skill-name>/` 和 `dist/<skill-name>.zip` | 在 [Skills](#skills) 表格新增一行，包含源码路径、下载包和用途 |
| Web 小工具 | 外部 URL 或项目仓库 | 在 [工具 Tools](#工具-tools) 表格新增一行 |
| 网站链接 | 外部 URL | 在 [网站 Websites](#网站-websites) 表格新增一行 |
| 学习资料 | 外部 URL 或仓库文件 | 在 [学习资源 Learning](#学习资源-learning) 表格新增一行 |
| 临时想法 | README 笔记区或单独文档 | 先放 [灵感 / 笔记 Notes](#灵感--笔记-notes)，成熟后再移动到正式分类 |

新增 skill 的建议流程：

1. 在 `skills/<skill-name>/` 创建 skill 源码。
2. 在 `dist/` 生成同名 zip 下载包。
3. 在 README 的 Skills 表格新增条目。
4. 提交并推送到 GitHub。

_最后更新：2026-06-07_
