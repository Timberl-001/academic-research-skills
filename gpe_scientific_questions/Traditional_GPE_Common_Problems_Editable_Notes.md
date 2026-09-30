# 单页完全可编辑版：传统凝胶电解质的两大共性挑战

## 本次重画文件

- **主文件**：`Traditional_GPE_Common_Problems_Editable.pptx`，仅1页、16:9。
- **高清预览**：`Traditional_GPE_Common_Problems_Editable.png`，3840 × 2160 px。
- **矢量源**：`Traditional_GPE_Common_Problems_Editable.svg`。
- **本页单独打包**：`Traditional_GPE_Common_Problems_Editable_Files.zip`，含PPT、SVG、PNG及编辑说明。
- **生成程序**：`build_traditional_editable.py`，使用共享的原生对象绘制引擎 `build_design_concept.py`。

这个文件不是旧图片页的改名，也不是把SVG当作一张图片插入PPT，而是从头用**206个PowerPoint原生对象**重画。所有文字、边框、网络曲线、交联节点、溶剂符号、离子、虚线、箭头、电极、膜块和标注都能单独选择修改。PPT中没有嵌入图片、外部图像链接或锁定对象。PNG仅用于预览。

### 选中和修改

1. 在PowerPoint“开始 → 选择 → 选择窗格”中定位对象。
2. 每个对象都有唯一名称，按 `问题一-`、`问题二-`、`页面-` 和 `过渡-` 分类，方便定位。
3. 双击文字修改内容；“形状格式”修改颜色、线宽、大小和位置；自由曲线可右键“编辑顶点”。
4. 要整体移动某个示意区域，可以多选相关对象后组合；当前默认不组合，方便逐个编辑。
5. 中文字体为微软雅黑、英文/符号为Arial。如果设备缺少字体，可在PowerPoint中整体替换；SVG/PNG预览使用另行提供的Noto Sans SC/DejaVu Sans绘图字体。

## 页面逻辑

- **左图：体相离子传输。** 液态参照与传统凝胶对比，展示连续液相、曲折路径、局部配位滞留和网络不均等可能影响因素。
- **右图：电极/凝胶界面。** 展示局部接触空隙、非均匀SEI/CEI、反应膜破裂/重构及局部通量不均，宏观表现为极化和阻抗增长。
- **底部过渡：** 如何兼顾稳定骨架、高效离子传输与长期稳定电极界面？这里只提出通用设计目标，不出现本工作的具体配方。

PPT备注已附约一分钟讲稿与科学边界。

## 科学表述边界

“共性挑战”指常见问题类别，不表示所有传统凝胶必然失效。凝胶化不必然降低电导率，锂离子迁移数也不必然下降。网络与溶剂相互作用可限制迁移，也可在某些体系促进盐解离或改善传输；影响需具体验证。含液相凝胶不宜一概称为固–固接触。本图没有指定正负极材料、界面化学组分、配位数、孔径、能垒或实测膜形貌。

## 下载页面

`serve_ppt_download.py` 提供带下载按钮的同源页面，采用固定文件白名单，不暴露仓库目录或Git文件。PPT响应使用正确的MIME类型及 `Content-Disposition: attachment`。页面内所有下载/预览链接都是相对URL，不依赖GitHub访问。

```bash
python3 gpe_scientific_questions/serve_ppt_download.py --host 0.0.0.0 --port 8765
```

## 重建与检查

```bash
python3 -m pip install -r gpe_scientific_questions/requirements-design.txt
python3 gpe_scientific_questions/build_traditional_editable.py --font-dir /path/to/fonts
python3 -m unittest discover -s gpe_scientific_questions -p 'test_*.py' -v
```

绘图字体目录要求与最新体系设计页的绘图程序相同。打开现成PPT不需要Python或绘图字体。

结构检查覆盖原生对象类型、无图片/锁定对象、对象唯一命名及边界、内容范围、SVG/PPT场景一致性、预览和压缩包完整性、下载端点与白名单。结构测试不替代在实际PowerPoint中的最终视觉检查，也不验证化学机理。
