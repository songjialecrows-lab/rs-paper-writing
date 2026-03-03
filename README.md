# RS-Paper-Writing Skill

遥感论文写作全流程专家助手。从研究idea初期到最终投稿，提供全方位、全阶段的专业指导。

## 🎯 核心功能

### 早期阶段
- 研究idea评估与创新性分析
- 文献综述与研究定位（集成Semantic Scholar语义搜索）
- 研究gap识别与问题陈述

### 中期阶段
- 研究方法论与实验设计
- 代码库解析与论文素材提炼
- 结果分析与消融实验指导

### 后期阶段
- 论文结构化构建与内容充实
- 学术引用管理与验证（CCF/JCR/影响因子/作者H-index评估）
- 写作质量优化与表达改进
- 会议/期刊格式适配与投稿准备

### 特色功能

#### 🔄 自动引用补全（异步后台处理）
- 分析论文结构，按章节自动识别
- 智能提取关键概念和研究主题
- 根据章节类型调整搜索深度
  - 引言：深度搜索（20+引用/页）
  - 相关工作：标准搜索（10+引用/页）
  - 其他部分：轻量搜索（2-5引用/页）
- 自动搜索相关高质量文献
- 完全异步后台处理（不占用对话上下文）
- 支持进度跟踪和结果查询
- 支持90页大规模论文（3-5分钟完成）

#### 📄 Word格式自动调整
- 支持学校毕业论文模板的一键格式转换
- 自动调整标题、正文、图表、参考文献格式
- 支持多个学校模板的预设和自定义
- 保持论文内容完整，只改变格式
- 支持批量处理多个文档

#### 📚 引用管理
- 基于Semantic Scholar API的语义化文献检索
- 多维度质量评估（CCF分级、JCR分区、中科院分区、影响因子）
- 作者H-index和引用量查询
- arXiv文章智能判断
- BibTeX自动生成

## 🚀 快速开始

### 自动引用补全（三步完成）

**第1步：启动任务**
```bash
bash rs-paper-writing/scripts/auto_cite_async.sh thesis.docx
# 输出：任务ID: auto_cite_20260304_001
```

**第2步：离开，稍后回来**
- 任务在后台运行（3-5分钟）
- 不占用对话上下文
- 你可以做其他事情

**第3步：获取结果**
```bash
bash rs-paper-writing/scripts/get_result.sh auto_cite_20260304_001
# 输出：thesis_with_citations.docx（已添加117个引用）
```

**查询进度（可选）**
```bash
bash rs-paper-writing/scripts/check_progress.sh auto_cite_20260304_001
# 输出：████████░░ 80% 完成
```

### Word格式调整

```bash
bash rs-paper-writing/scripts/format_word.sh thesis.docx school_name
```

### 文献搜索

```bash
# 单个搜索
bash rs-paper-writing/scripts/s2_search.sh "remote sensing deep learning" 10

# 批量搜索（含年份过滤）
bash rs-paper-writing/scripts/s2_bulk_search.sh "remote sensing" "2020-" 10

# 作者H-index查询
bash rs-paper-writing/scripts/author_info.sh "AUTHOR_ID"

# 期刊质量查询
bash rs-paper-writing/scripts/venue_info.sh "IEEE Transactions on Geoscience and Remote Sensing"

# CCF分级查询
bash rs-paper-writing/scripts/ccf_lookup.sh "IGARSS"

# 影响因子查询
bash rs-paper-writing/scripts/if_lookup.sh "IEEE TGRS"
```

## 📁 项目结构

```
rs-paper-writing/
├── SKILL.md                          # Skill定义和工作流程
├── AUTO_CITE_ASYNC_GUIDE.md          # 自动引用补全详细指南
├── WORD_FORMAT_GUIDE.md              # Word格式调整指南
├── scripts/
│   ├── auto_cite_async.py            # 异步处理主程序
│   ├── auto_cite_async.sh            # 启动脚本
│   ├── check_progress.sh             # 进度查询脚本
│   ├── get_result.sh                 # 结果获取脚本
│   ├── list_tasks.sh                 # 任务列表脚本
│   ├── chapter_analyzer.py           # 章节分析模块
│   ├── smart_search.py               # 智能搜索模块
│   ├── task_manager.py               # 任务管理模块
│   ├── citation_inserter.py          # 引用插入模块
│   ├── format_to_word.py             # Word格式转换
│   ├── format_word.sh                # 格式调整脚本
│   ├── s2_search.sh                  # Semantic Scholar搜索
│   ├── s2_bulk_search.sh             # 批量搜索
│   ├── author_info.sh                # 作者信息查询
│   ├── venue_info.sh                 # 期刊信息查询
│   ├── ccf_lookup.sh                 # CCF分级查询
│   ├── if_lookup.sh                  # 影响因子查询
│   ├── doi2bibtex.sh                 # DOI转BibTeX
│   └── crossref_search.sh            # CrossRef搜索
├── data/
│   ├── search_strategies.json        # 搜索策略配置
│   ├── task_storage/                 # 任务存储目录
│   ├── templates/                    # Word模板目录
│   ├── ccf_2022.sqlite               # CCF数据库
│   └── impact_factor.sqlite3         # 影响因子数据库
└── evals/                            # 测试用例
```

## 📊 性能指标

### 自动引用补全（90页论文）

| 章节 | 页数 | 引用数 | 耗时 |
|------|------|--------|------|
| 引言 | 10 | 200+ | 60s |
| 相关工作 | 8 | 80+ | 32s |
| 讨论 | 12 | 60+ | 24s |
| 方法 | 15 | 75+ | 30s |
| 实验 | 20 | 60+ | 40s |
| 结果 | 15 | 30+ | 30s |
| 结论 | 9 | 9+ | 18s |
| **总计** | **90** | **514+** | **234s (3.9分钟)** |

### 上下文占用

| 阶段 | 占用 |
|------|------|
| 系统提示 | 5K |
| Skill定义 | 10K |
| 后台任务 | 0K ✅ |
| **总计** | **15K** |

**结论**：完全异步处理，不占用对话上下文！

## 🔧 配置

### Semantic Scholar API Key（强烈推荐）

```bash
# 在skill目录创建.env文件
echo 'S2_API_KEY="your_key_here"' > ~/.claude/skills/rs-paper-writing/.env

# 获取API Key: https://www.semanticscholar.org/product/api/api-key
```

| 模式 | 速率限制 | 推荐场景 |
|------|----------|----------|
| 有API Key | 1次/秒 | 日常使用（推荐） |
| 无API Key | 共享限额 | 极易触发429 |

### arXiv引用阈值（可选）

```bash
# 默认100，可在.env中配置
echo 'ARXIV_CITATION_THRESHOLD=100' >> ~/.claude/skills/rs-paper-writing/.env
```

## 📖 详细文档

- [SKILL.md](rs-paper-writing/SKILL.md) - 完整的Skill定义和工作流程
- [AUTO_CITE_ASYNC_GUIDE.md](rs-paper-writing/AUTO_CITE_ASYNC_GUIDE.md) - 自动引用补全详细指南
- [WORD_FORMAT_GUIDE.md](rs-paper-writing/WORD_FORMAT_GUIDE.md) - Word格式调整指南

## 🎓 适用人群

- 遥感科学、地理信息系统、地球观测、环境科学等领域的研究生
- 博士生、青年学者及科研人员
- 需要高效完成学术论文写作的研究人员

## 💡 核心原则

### 基本原则
1. **用户为中心** - 始终将用户的具体需求和当前进度放在首位
2. **学术严谨性** - 所有建议基于最新学术规范和遥感领域最佳实践
3. **知识产权保护** - 严格保护用户论文内容和研究成果的保密性
4. **辅助而非替代** - 定位为指导者和辅助者，不代写论文

### 行为准则
1. **流程化指导** - 按照论文写作自然流程，分阶段提供逻辑清晰的指导
2. **知识共享** - 不仅给出建议，更解释其背后的原理和目的
3. **积极互动** - 鼓励用户提问讨论，提供及时具体的建设性反馈
4. **持续学习** - 关注遥感领域和学术写作规范的最新发展

## 📝 使用建议

**最佳实践**：
- 提供具体的研究背景和代码库信息，以获得更精准的指导
- 分阶段进行，不要试图一次性完成所有工作
- 主动提出问题和困惑，获得针对性的帮助
- 在应用建议前，理解其背后的原理

**常见场景**：
- 从研究代码转化为论文内容
- 构建论文框架和逻辑结构
- 优化论文表达和学术英语
- 适配特定会议或期刊的模板要求
- 管理和验证学术引用
- 自动补全论文引用（启动后台任务，稍后查看结果）

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个Skill！

## 📄 许可证

MIT License

## 👤 作者

Created with ❤️ by Claude Haiku 4.5

---

**需要帮助？** 查看详细文档或提交Issue。
