# 组会PPT：凝胶电解质体系设计思路

## 交付文件

- **单页可编辑PPT**：[MBA_GPE_Design_Concept_Slide.pptx](MBA_GPE_Design_Concept_Slide.pptx)
- **整页高清PNG**：[MBA_GPE_Design_Concept_Slide.png](MBA_GPE_Design_Concept_Slide.png)，3840 × 2160 px，16:9。
- **整页矢量SVG**：[MBA_GPE_Design_Concept_Slide.svg](MBA_GPE_Design_Concept_Slide.svg)
- **仅左右对比示意图**：[PNG](MBA_GPE_Design_Comparison_Figure.png) / [SVG](MBA_GPE_Design_Comparison_Figure.svg)，便于单独插入自己的模板。
- **绘图源程序**：[build_design_concept.py](build_design_concept.py)

本页是“体系设计/研究思路”页，建议紧接上一页“传统凝胶电解质的两大共性瓶颈”。没有覆盖此前的科学问题页。

全部图形均为原创绘制。参考用户图片的**左右对比—中心网络/溶剂化放大—两侧电极界面**叙事结构，不复制其图像像素、显微照片、分子体系或数据结论。

## 页面内容

**标题：体系设计思路：网络—溶剂化—界面协同调控**

**体系：MBA交联网络；1.0 M LiPF₆ + 0.2 M LiDFOB in DMTFA:TTE = 1:1。**

左图表现传统凝胶的典型瓶颈：极性位点过强束缚、传输/配位交换受限，以及非均匀界面膜与局部通量。

右图表现本体系的设计目标：MBA网络锁液与相容调控、溶剂/阴离子/聚合物协同配位、富LiF及B–O组分的双界面膜。右图整列已注明**“设计预期”**，不是实测机理或性能结论。

### 三条设计抓手

| 设计抓手 | 本页的简洁表达 | 需要验证的关键点 |
|---|---|---|
| **MBA：交联锁液与相容** | 双C=C参与构网；N–H···O=C相互作用辅助相容 | 能否均匀成胶/保液；氢键是否存在；交联度与力学/传输的平衡 |
| **DMTFA/TTE：溶剂化调控** | 调节配位平衡，促进Li⁺动态交换 | 溶剂、阴离子和聚合物位点的实际配位贡献；交换/脱溶剂化及传输是否改善 |
| **LiDFOB：双界面成膜调控** | 预期构筑LiF/B–O富集SEI/CEI | 两电极上的真实膜组分、厚度、空间分布及循环稳定性 |

化学标注：
- MBA：CH₂=CH–C(=O)–NH–CH₂–NH–C(=O)–CH=CH₂。右图网络画的是双键聚合后的酰胺桥连接，不是仍含C=C的完整聚合物重复单元。
- DMTFA按N,N-二甲基三氟乙酰胺表示：CF₃–C(=O)–N(CH₃)₂。其本身没有N–H；图中的候选氢键供体是MBA的N–H，受体是DMTFA的羰基氧。
- 未指定电极材料，故只标“正极/负极”；没有照搬参考图中的HV-LCO或锂金属。

## 约1分钟汇报讲稿

> 上一页提出了凝胶化后传输受限和电极界面失稳两类问题。针对这些瓶颈，我们从网络、溶剂化和成膜三个层次协同设计。
>
> 首先，利用MBA的两个双键构建交联网络，以适当的交联程度锁住电解液，并借助酰胺基团的分子间作用改善相容性，避免过度交联阻碍传输。
>
> 其次，通过DMTFA/TTE以及聚合物极性位点，调节溶剂和阴离子对Li⁺的配位平衡，探索动态配位交换和脱溶剂化的改善。
>
> 最后，在LiPF₆基础上引入LiDFOB，尝试引导含氟、含硼组分参与界面成膜，构建富LiF/B–O的SEI/CEI。
>
> 因此，右图表达的是“锁液稳网、动态配位、双界面稳定”的设计目标，具体机制和性能改善还需要后续验证。

## 科学表述边界

1. **不直接认定LHCE。** 仅凭总盐浓度1.2 M和DMTFA:TTE=1:1，不能认定体系已形成局部高浓结构、CIP/AGG占优，或DFOB⁻已进入第一溶剂化鞘。
2. **不把弱配位等同于高电导。** Li–阴离子、Li–聚合物作用、盐解离度和网络曲折度均可能影响电导率；本页不直接宣称σ或tLi⁺必然提高。
3. **不宣称已经降低能垒。** 两侧虚线箭头只用于定性表示受阻/调控思路，不是计算或实验测得的自由能曲线。
4. **不声称某个官能团必然锚定阴离子。** N–H可参与氢键的构想不等于已证明固定阴离子或提高迁移数。
5. **不把界面图当作组分证据。** 右图金色/绿色膜块只表示预期LiF/B–O组分，不能用于推断其占比、梯度、具体硼氧化学物种或晶体结构。
6. **不添加未给出的工艺。** MBA浓度、其他共聚单体、引发剂、聚合方式/温度、溶剂比的体积/质量/摩尔基准都未自行补充。
7. **不把设计目标当成已验证结论。** 暂不写“LiDFOB清除HF”“完全抑制枝晶”“固定轨道能级排序”等没有当前体系证据的结论。

建议验证：FTIR/Raman/NMR与MD/DFT分析配位及分子间作用；保液/溶胀/流变分析网络；电导率、迁移数及EIS分析传输；XPS/TOF-SIMS、形貌及循环前后EIS分析双界面。按实际正负极材料选择电化学测试。

## 编辑和复现

PPT为单页16:9，标题、配方、文字、酰胺桥、溶剂/阴离子符号、网络、箭头、电极和膜块均为**PowerPoint原生可编辑对象**，不是一整张背景图片。可在“选择窗格”根据中文对象名称定位修改。中文字体设为微软雅黑，英文为Arial；若设备缺少字体，可整体替换。

SVG文本仍可编辑；PNG仅作为高清预览或快速粘贴。PPT备注中附有讲稿与科学边界。

复现程序依赖Pillow、python-pptx、resvg-py，并需提供Noto Sans SC（400/700字重）和DejaVu Sans字体目录。字体文件不打包进仓库；打开现成PPT不需要运行程序。

```bash
python3 -m pip install -r gpe_scientific_questions/requirements-design.txt
python3 gpe_scientific_questions/build_design_concept.py --font-dir /path/to/fonts
```

字体目录需包含 `*chinese-simplified-400.ttf`、`*chinese-simplified-700.ttf`、`DejaVuSans.ttf` 和 `DejaVuSans-Bold.ttf`；中文字体内部 family 名应为 `Noto Sans SC`。

检查交付文件（不需要绘图字体）：

```bash
python3 -m unittest discover -s gpe_scientific_questions -p 'test_design_concept.py' -v
```

检查覆盖16:9比例、原生对象/无嵌入图片、对象边界、配方与设计假设标注、讲稿备注、SVG/PPT场景一致性和高清图尺寸；不替代PowerPoint视觉检查或实际化学机制验证。

### 背景依据（不用于替代本体系的实验验证；未引用任何文献图片）

- DMTFA/FEC与LiPF₆/LiDFOB的研究讨论了DMTFA的极性/配位调控；其中溶剂体系不同，不能直接作为本DMTFA/TTE凝胶的机理证据。[3](https://advanced.onlinelibrary.wiley.com/doi/10.1002/aenm.71380)
- TTE/BTFE作为稀释剂对溶剂化结构的影响具有体系依赖性；相关TEP体系研究同时强调了用光谱和模拟评估结构的必要性。[3](https://pubs.rsc.org/en/content/articlehtml/2023/ta/d2ta08404j)
- LiTFSI/DMTFA体系在锂金属上观察到含LiF的SEI，可作为含氟酰胺界面反应的背景依据，但不证明当前凝胶中两侧界面均已富LiF/B–O。[5](https://pubs.acs.org/doi/10.1021/jp402844r)
