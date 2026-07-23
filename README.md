# ArtTool

ArtTool 是一套面向 Unreal Engine 美术与技术美术工作流的编辑器工具集。插件基于 Editor Utility Widget 和蓝图实现，将常用的场景整理、批量替换、调试视图、模型处理、碰撞设置和资产检查集中到一个可停靠的编辑器面板中。

当前版本：`1.0`

目标引擎：Unreal Engine `5.7`

## 主要特性

- 在一个 `Art Tool` 页签中集中提供编辑器工具和资产工具。
- 对当前选择的 Actor 或资产执行批量操作。
- 支持材质、静态网格体批量替换及回退。
- 支持空 Actor 检测、清理和光照贴图分辨率设置。
- 提供 UV、色彩、Lumen Reflection、Specular Range 等调试视图。
- 提供模型减面、自动 LOD、碰撞配置和未使用资产检测。
- 提供 Datasmith 元数据筛选和场景距离测量。
- 使用 VS Code Dark 风格的响应式编辑器界面。
- Rapid Packer 贴图合并资产仍在插件中，但当前版本因旧路径引用问题暂不可用。

## 界面结构

主界面资产为：

```text
/ArtTool/Art_Tool
```

`Art_Tool` 使用 Widget Switcher 承载两个工具面板：

| 页签 | Widget | 用途 |
| --- | --- | --- |
| 编辑器工具 | `WBP_nSpaceDevTool` | 场景 Actor、调试视图和通用编辑器操作 |
| 资产工具 | `WBP_nSpaceDevTool_2` | 材质实例、模型、碰撞、贴图和资产检查 |

两个页面均支持停靠窗口缩放和独立垂直滚动。

## 编辑器工具

### 场景 Actor

| 功能 | 说明 |
| --- | --- |
| 材质替换 | 批量查找指定材质，并按原材质槽位替换为目标材质 |
| 材质回退 | 将匹配的目标材质恢复为替换前材质 |
| 模型替换 | 批量替换 Static Mesh Actor 使用的静态网格体 |
| 模型回退 | 将匹配的目标网格体恢复为替换前网格体 |
| 光照分辨率 | 为选中的 Static Mesh Actor 设置固定或自适应 Lightmap Resolution |
| 空 Actor 检测 | 统计当前选择中不包含有效静态网格体的 Actor |
| 空 Actor 删除 | 根据确认选项删除当前选择中的空 Actor |
| Datasmith 筛选 | 根据 Datasmith User Data 的键和值过滤当前选择 |
| 距离测量 | 测量最后选择的两个 Actor，并生成端点、箭头和距离文本 |
| 清空测量 | 删除距离测量生成的辅助 Actor |
| 工具实例化 | 注册并打开相关 Editor Utility 工具页签 |

光照分辨率可选值包括：

```text
自适应、32、64、128、256、512、1024、2048、4096
```

### Debug

| 功能 | 说明 |
| --- | --- |
| 材质 Debug | 启用或关闭材质调试辅助视图 |
| 色彩校准 | 生成或移除基础 ColorCorrection Post Process 辅助 Actor |
| UV 查看 | 为场景网格体设置或清除 UV Overlay Material |
| 饱和度调节 | 修改调试 Material Parameter Collection 中的标量参数 |
| Lumen Reflections | 切换 Lumen 反射检查视图 |
| Specular Range | 切换高光范围检查视图 |
| 反射参数 | 调整 Reflections、Reflections Add 和 Reflections Color 参数 |

相关辅助资产位于：

```text
Plugins/ArtTool/Content/ViewModes
Plugins/ArtTool/Content/UV
Plugins/ArtTool/Content/ColorCorrection
```

当前仅保留基础 ColorCorrection 流程。旧版 LUT 流程使用的 `BP_ColorCorrectionPost_Lut`、LUT 纹理、旧校正材质和参数集合已经移除，不再属于受支持功能。

## 资产工具

| 功能 | 说明 |
| --- | --- |
| 材质实例参数复制 | 读取并暂存材质实例参数 |
| 材质实例参数粘贴 | 将暂存参数应用到目标材质实例 |
| 模型减面 | 按设置比例简化静态网格体 |
| 自动 LOD | 自动生成或设置静态网格体 LOD |
| 简单碰撞 | 配置并生成指定类型的简单碰撞 |
| 复杂碰撞 | 配置复杂碰撞方式 |
| 添加碰撞 | 对目标静态网格体添加碰撞 |
| 移除碰撞 | 移除目标静态网格体的碰撞数据 |
| 贴图合并 | 暂不可用；Rapid Packer 当前仍包含旧 `/Game/Rapid_Packer` 资源引用 |
| 资产检测 | 检测未使用资产或执行资产整理检查 |

贴图处理相关资产位于：

```text
Plugins/ArtTool/Content/Rapid_Packer
```

> Rapid Packer 当前会在加载时报告 `T_Black8x8` 依赖不可用。实际纹理位于 `/ArtTool/Rapid_Packer/Material/Textures/T_Black8x8`，但部分材质与材质函数仍引用 `/Game/Rapid_Packer/Material/Textures/T_Black8x8`。修复并重新保存这些资产前，不应将贴图合并视为可用功能。

## 当前资产范围

当前插件保留以下主要资产组：

- 主工具入口和两个 Editor Utility Widget 页面
- ViewModes 调试材质、纹理、MPC 和辅助 Blueprint
- 基础 UV Overlay 材质及 MPC
- 基础 ColorCorrection 材质和辅助 Blueprint
- DistanceMeasurement 距离测量辅助 Blueprint
- MaterialParameters 材质参数结构
- MeshToHISM 工具及其参数结构
- Rapid Packer 资产（当前因路径引用问题暂不可用）

以下旧资产已经从插件中移除，不应再作为现有功能或安装内容引用：

- UIBackup、PreVSCode、PreResponsiveRoot 和 ResponsiveProbe 等临时 Widget
- `T_CustomUV`
- LUT 色彩校正纹理、材质、MPC 和 `BP_ColorCorrectionPost_Lut`
- 旧关卡打开/保存工具
- 旧 `Asset_replace` 工具
- `BP_Table_a`、`NewWidgetBlueprint`、`Text` 等测试资产

## 安装

### 使用当前示例工程

1. 使用 Unreal Engine `5.7` 打开 `ArtTool.uproject`。
2. 等待编辑器完成插件加载、资产发现和蓝图编译。
3. 如果编辑器提示缺少插件，请先安装或启用对应依赖。
4. 重启编辑器，使 Python Startup Script 注册工具栏入口。

### 安装到其他工程

将插件目录复制到目标工程：

```text
<YourProject>/Plugins/ArtTool
```

在目标工程中启用以下插件：

- Editor Scripting Utilities
- Geometry Scripting
- Dataprep Editor
- Scriptable Tools Editor Mode
- Python Editor Script Plugin
- Datasmith Importer（使用 Datasmith 筛选时需要）

其中 Python Editor Script Plugin 是工具栏入口的必需依赖，但当前没有写入 `ArtTool.uplugin` 的插件依赖列表，迁移到其他工程时必须手动启用。

当前插件通过 Python 启动脚本注册工具栏按钮。目标工程需要包含以下配置：

```ini
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
+StartupScripts=addWidget_plugins.py
```

修改插件和配置后重启 Unreal Editor。

> 当前示例工程还启用了 nSpace、nSpacePlatform、Datasmith Runtime、Modeling Tools Editor Mode、OSC 和 VibeUE。这些属于示例工程环境，不是 `ArtTool.uplugin` 声明的插件依赖；从工程中单独迁移插件时，应使用 Reference Viewer 检查项目是否还需要它们。

当前版本不能视为完全无警告的独立迁移版本。Rapid Packer 的部分资产仍引用 `/Game/Rapid_Packer`，即使插件目录复制正确，编辑器启动时也会产生缺失依赖警告。该问题不影响主工具入口和大多数编辑器功能，但会影响贴图合并功能。

## 打开工具

### 工具栏入口

启动脚本会向以下菜单扩展点注册按钮：

```text
LevelEditor.LevelEditorToolBar.User
```

当前脚本注册的按钮标签为 `Example Button`，提示文本为“美术工具”。点击后会查找现有工具实例；如果工具尚未打开，则创建并注册 `Art_Tool` 页签。

### Content Browser 入口

如果工具栏按钮没有出现：

1. 在 Content Browser 中启用 `Show Plugin Content`。
2. 打开 `ArtTool` 插件内容目录。
3. 找到 `Art_Tool` Editor Utility Widget。
4. 右键选择 `Run Editor Utility Widget`。

## 推荐工作流

### 批量替换材质或模型

1. 在关卡中选择需要处理的 Actor。
2. 在 Details View 中设置源材质或源模型。
3. 设置目标材质或目标模型。
4. 检查选择范围，避免处理不相关对象。
5. 点击替换按钮。
6. 如需撤销本次映射，使用对应回退按钮或 Unreal Editor Undo。

### 清理空 Actor

1. 在关卡中选择待检查的 Actor。
2. 先运行“检测空 Actor”确认数量。
3. 再运行“删除空 Actor”。
4. 根据确认框决定是否处理包含子组件的空 Actor。
5. 完成后检查关卡并保存。

### Datasmith 元数据筛选

1. 选择需要筛选的 Datasmith Actor 集合。
2. 输入 Datasmith User Data Key。
3. 输入需要精确匹配的 Value。
4. 点击筛选。
5. 不匹配的 Actor 会从当前选择中移除。

### 距离测量

1. 依次选择两个 Actor。
2. 点击“距离测量”。
3. 工具使用选择数组中的最后两个 Actor 作为端点。
4. 测量结果以厘米显示，并生成辅助箭头与端点。
5. 点击“清空”删除测量辅助对象。

## 目录结构

```text
Plugins/ArtTool/
├─ ArtTool.uplugin
├─ Config/
│  └─ FilterPlugin.ini
├─ Resources/
│  └─ Icon128.png
└─ Content/
   ├─ Art_Tool.uasset
   ├─ WBP_nSpaceDevTool.uasset
   ├─ WBP_nSpaceDevTool_2.uasset
   ├─ ColorCorrection/
   ├─ DistanceMeasurement/
   ├─ MaterialParameters/
   ├─ MeshToHISM/
   ├─ Python/
   │  └─ addWidget_plugins.py
   ├─ Rapid_Packer/
   │  ├─ Blueprint/
   │  │  └─ BP_Rapid_Packer.uasset
   │  └─ Material/
   │     ├─ M_TexturePacking.uasset
   │     ├─ MaterialFunctions/
   │     └─ Textures/
   ├─ UV/
   └─ ViewModes/
```

插件不包含 C++ Source 模块，主要逻辑由 Editor Utility Widget、Blueprint 和 Python 启动脚本组成。

## 依赖

### 插件描述文件声明的依赖

`ArtTool.uplugin` 当前声明：

| 插件 | 用途 |
| --- | --- |
| EditorScriptingUtilities | 编辑器 Actor、资产和工具脚本操作 |
| GeometryScripting | 静态网格体和几何处理 |
| DataprepEditor | 数据准备与导入工作流 |
| ScriptableToolsEditorMode | 可脚本化编辑器工具支持 |

### 启动必需依赖

| 插件或配置 | 用途 |
| --- | --- |
| Python Editor Script Plugin | 执行 `addWidget_plugins.py` 并注册工具栏入口 |
| `+StartupScripts=addWidget_plugins.py` | 在编辑器启动时加载注册脚本 |

### 功能依赖

| 插件 | 用途 |
| --- | --- |
| Datasmith Importer | Datasmith User Data 筛选 |
| Modeling Tools Editor Mode | 部分模型编辑工作流 |

### 示例工程依赖

当前 `ArtTool.uproject` 还启用了 nSpace、nSpacePlatform、Datasmith Runtime、OSC 和 VibeUE。它们属于当前示例工程环境，不应自动视为插件发布包的强制依赖。

## 安全提示

- 本插件是 Editor-only 工具，不应作为运行时 UI 使用。
- 删除空 Actor、移除碰撞、模型减面等操作会修改资产或关卡。
- 执行批量操作前应保存关卡，并确保工程处于版本控制中。
- 多数场景操作以当前选择为处理范围，执行前应再次确认选择内容。
- 不要随意移动或重命名插件内的 Widget、Material、MPC 和辅助 Blueprint；蓝图中包含对这些资产的直接引用。
- 材质或模型回退用于反向执行对应替换映射，不替代完整的版本控制恢复流程。
- 修改 Editor Utility Widget 后，需要关闭并重新打开正在运行的工具页签，才能加载新实例。

## 故障排查

### 工具栏按钮没有出现

- 确认 Python Editor Script Plugin 已启用。
- 确认 `addWidget_plugins.py` 已配置为 Startup Script。
- 检查 Output Log 中的 Python 错误。
- 重启 Unreal Editor。
- 使用 Content Browser 手动运行 `Art_Tool`。

### 找不到插件内容

- 在 Content Browser Settings 中启用 `Show Plugin Content`。
- 确认插件位于 `<Project>/Plugins/ArtTool`。
- 确认 `ArtTool.uplugin` 已启用并成功加载。

### 工具窗口没有随停靠区域缩放

- 关闭并重新打开 `Art Tool` 页签。
- 确认运行的是 `/ArtTool/Art_Tool`，而不是旧的临时实例。
- 确认 `WidgetSwitcher_137` 和两个子 Widget 的 Slot 保持 Fill。

### Rapid Packer 报告 T_Black8x8 缺失

当前已知警告：

```text
/Game/Rapid_Packer/Material/Textures/T_Black8x8 不可用
```

插件内实际资产路径为：

```text
/ArtTool/Rapid_Packer/Material/Textures/T_Black8x8
```

需要在 Unreal Editor 中修复 `M_TexturePacking`、`MF_CustomNormalFromHeightmap`、`MF_HeightmapUVOffset` 等资产的旧引用并重新保存。修复前请勿依赖贴图合并功能。

### 启动时恢复 Unknown 页签失败

- 该信息通常来自编辑器保存的旧布局，而不是当前 `Art_Tool` 资产缺失。
- 关闭失效页签并重新运行 `/ArtTool/Art_Tool`。
- 必要时恢复默认编辑器布局，再重新固定 Art Tool 页签。

### Datasmith 筛选没有结果

- 确认 Datasmith Importer 已启用。
- 确认 Actor 确实包含 Datasmith User Data。
- Key 和 Value 使用精确匹配，注意空格、大小写和语言字符。

### 调试视图没有变化

- 确认 ViewModes、UV 和 ColorCorrection 目录中的辅助资产没有丢失。
- 检查关卡中是否存在旧的调试辅助 Actor。
- 先关闭对应开关，再重新启用。
- 当前不再包含 LUT 色彩校正链；不要尝试加载 `BP_ColorCorrectionPost_Lut` 或旧 LUT 材质。

## 开发说明

- 主工具入口：`/ArtTool/Art_Tool`
- 编辑器工具页面：`/ArtTool/WBP_nSpaceDevTool`
- 资产工具页面：`/ArtTool/WBP_nSpaceDevTool_2`
- 工具栏注册脚本：`Plugins/ArtTool/Content/Python/addWidget_plugins.py`
- 插件版本信息：`Plugins/ArtTool/ArtTool.uplugin`

由于核心资产为二进制 `.uasset`，修改前后应在 Unreal Editor 中完成以下检查：

1. 编译所有相关 Blueprint。
2. 确认没有新增编译错误或警告。
3. 验证全部按钮、复选框和输入控件的事件绑定。
4. 在测试关卡中执行非破坏性冒烟测试。
5. 使用版本控制检查被修改的资产列表。

## 已知限制

- 工具主要针对 Windows 编辑器工作流设计。
- 当前工程与插件资产基于 Unreal Engine 5.7 制作，较早版本可能无法加载。
- 部分操作仅支持 Static Mesh Actor 或 Static Mesh Component。
- 调试工具会在关卡中生成辅助 Actor；不再使用时应关闭对应模式或执行清理。
- LUT 色彩校正、Custom UV、旧关卡工具和 Asset Replace 已从当前插件中移除。
- Rapid Packer 仍包含旧 `/Game/Rapid_Packer` 引用，贴图合并功能暂不可用。
- Python Editor Script Plugin 是工具栏入口的实际必需依赖，但尚未写入 `ArtTool.uplugin`。
- 当前示例工程依赖 nSpace 环境；直接复制整个工程与仅迁移 ArtTool 插件的依赖范围不同。
- Editor Utility Widget 修改不会自动刷新已经运行的实例。
- 插件当前没有自动化测试套件，发布前需要在测试工程中手动验证关键功能。
