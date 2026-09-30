# 凝胶电解质课题：PPT文件索引

## 推荐使用顺序

1. **科学问题页（新重画、完全可编辑）**：`Traditional_GPE_Common_Problems_Editable.pptx`——单页16:9、206个独立原生对象，仅介绍传统凝胶的体相传输与界面问题，不提前展示本体系配方。优先使用此版本，而非下面的旧图片嵌入版。
2. **体系设计页**：`MBA_GPE_Design_Concept_Slide.pptx`——最新原生可编辑版本，展示MBA网络、DMTFA/TTE溶剂化调控和LiDFOB双界面成膜设计；所有效果为待验证的设计预期。

## 文件与编辑方式

| 文件 | 页数 | 内容 | 可编辑程度 |
| --- | ---: | --- | --- |
| `Traditional_GPE_Common_Problems_Editable.pptx` | 1 | 全新重画的传统凝胶两大共性问题页 | **206个原生可编辑对象，无嵌入图片、无锁定对象** |
| `Traditional_GPE_Common_Problems_Editable_Files.zip` | — | 本次单页的PPT、SVG、PNG及编辑说明 | 仅打包本页；不包含其他版本 |
| `Traditional_GPE_Scientific_Questions_Slide.pptx` | 5 | 传统凝胶的两类共性挑战；含整页版、两张单图和一张早期体系设计图 | 第1页标题/过渡文字为原生对象，图片可移动和缩放；图内部为嵌入PNG，不能逐个修改 |
| `MBA_GPE_Scientific_Questions_Presentation.pptx` | 5 | 上述科学问题文件的旧文件名 | **与上一文件内容完全相同，不是另一版本** |
| `MBA_GPE_Earlier_Schematics_Collection.pptx` | 5 | 三项科学问题矩阵、全电池机理、离子传输单图、界面单图、含本体系的双图布局 | 标题和草稿说明是原生文本；示意图为PNG，原SVG源另附 |
| `MBA_GPE_Design_Concept_Slide.pptx` | 1 | 最新的左右对比体系设计页 | **277个原生可编辑对象；未嵌入整页图片** |
| `GPE_PPT_Collection.zip` | — | 先前3份不重复的PPT、10份SVG源和当时的索引 | 压缩包内按01/02/03编号；**不包含本次新重画的科学问题页**；新页请用其单独打包文件 |

### 科学问题文件的5页

1. 两图并排，标题与过渡文字可改；建议作为正式科学问题页的排版起点。
2. 第1页的整页高清图片版。
3. 体相传输问题单图放大。
4. 电极/凝胶界面问题单图放大。
5. **早期体系设计概念图**；正式汇报建议替换为最新的原生可编辑设计页。

“共性问题”应理解为常见挑战，不是所有传统凝胶必然具有的性质。凝胶化不必然降低锂离子迁移数；影响取决于配位、盐解离、微结构和界面等因素。旧图中有关刚性骨架、固–固接触、枝晶等情景也不适用于所有聚合物/电极体系。

### 早期方案仅作布局与讨论归档

旧图中的LHCE、CIP/AGG、能垒下降、阴离子固定、HF清除等措辞不能作为本体系已经验证的结论。仅凭1.2 M总盐浓度和DMTFA:TTE=1:1不能证明这些机制。正式汇报应优先使用最新设计页的“设计预期/待验证”表述，详见 `MBA_GPE_Design_Concept_Notes.md`。

### 修改方法

- **新科学问题页和最新设计页**：在PowerPoint“开始 → 选择 → 选择窗格”按对象名称修改文字、网络、离子、箭头及膜层。新科学问题页对象名均唯一；曲线可右键“编辑顶点”。
- **旧图**：编辑压缩包 `SVG_sources/` 中对应矢量源，再重新插入PPT；也可在支持该功能的PowerPoint版本中尝试“SVG转换为形状”。不同版本对SVG文本、渐变和转换的支持不同，不能保证一键转换后与原图完全相同。
- 所有图件均为原创绘制；没有嵌入文献图片或实验显微照片。

## 复现与检查

已存在的PPT可直接打开，不需要安装Python。

```bash
python3 -m pip install -r gpe_scientific_questions/requirements-design.txt
# 在对应PNG、SVG和既有PPT存在的情况下重建早期合集及打包文件：
python3 gpe_scientific_questions/build_earlier_presentations.py
# 检查最新设计页、早期合集及压缩包的文件结构：
python3 -m unittest discover -s gpe_scientific_questions -p 'test_design_concept.py' -v
```

最新设计页生成程序为 `build_design_concept.py`，需要另行提供绘图字体，详见最新设计页说明。
