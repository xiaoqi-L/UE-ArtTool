<p align="center">
  <img src="ArtTool/Resources/Icon128.png" alt="ArtTool icon" width="128" />
</p>

<h1 align="center">ArtTool</h1>

<p align="center">
  面向 Unreal Engine 美术与技术美术工作流的编辑器工具集
</p>

<p align="center">
  <strong>版本</strong> 1.0 &nbsp;|&nbsp; <strong>目标引擎</strong> Unreal Engine 5.7 &nbsp;|&nbsp; <strong>类型</strong> Editor-only Plugin
</p>

---

ArtTool 基于 Editor Utility Widget、Blueprint 和 Python 启动脚本实现，将常用的场景整理、批量替换、调试视图、模型处理、碰撞设置和资产检查整合到一个可停靠的编辑器面板中。

> [!IMPORTANT]
> 本插件仅用于 Unreal Editor。删除空 Actor、移除碰撞、模型减面等操作会修改关卡或资产；执行批量操作前请保存关卡并确认已接入版本控制。

## 目录

- [快速开始](#快速开始)
- [功能概览](#功能概览)
- [打开工具](#打开工具)
- [推荐工作流](#推荐工作流)
- [依赖与配置](#依赖与配置)
- [已知限制](#已知限制)
- [故障排查](#故障排查)
- [目录结构](#目录结构)
- [开发说明](#开发说明)

## 快速开始

### 1. 安装插件

将仓库中的 `ArtTool` 目录复制到目标 Unreal 项目：

```text
<YourProject>/Plugins/ArtTool
```

> 仓库根目录中的 `ArtTool/` 即插件根目录。文档中 `Plugins/ArtTool/` 表示它安装到目标工程后的路径。

### 2. 启用依赖

在目标工程中启用以下插件：

| 插件 | 是否必需 | 用途 |
| --- | :---: | --- |
| Editor Scripting Utilities | 是 | 编辑器 Actor、资产和工具脚本操作 |
| Geometry Scripting | 是 | 静态网格体和几何处理 |
| Dataprep Editor | 是 | 数据准备与导入工作流 |
| Scriptable Tools Editor Mode | 是 | 可脚本化编辑器工具支持 |
| Python Editor Script Plugin | 是 | 注册工具栏入口 |
| Datasmith Importer | 按需 | Datasmith User Data 筛选 |
| Modeling Tools Editor Mode | 按需 | 部分模型编辑工作流 |

### 3. 注册工具栏入口

在目标工程的 Python 插件配置中添加启动脚本：

```ini
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
+StartupScripts=addWidget_plugins.py
```

配置完成后重启 Unreal Editor。启动脚本会在 `LevelEditor.LevelEditorToolBar.User` 注册工具栏按钮。

## 打开工具

优先使用工具栏中提示文本为“美术工具”的按钮。若按钮未出现，可在 Content Browser 中启用 `Show Plugin Content`，然后右键运行：

```text
/ArtTool/Art_Tool
```

## 功能概览

| 模块 | 核心能力 |
| --- | --- |
| 场景 Actor | 材质与模型批量替换及回退、Lightmap Resolution、空 Actor 清理、Datasmith 筛选、距离测量 |
| Debug | 材质 Debug、色彩校准、UV Overlay、饱和度、Lumen Reflections、Specular Range |
| 资产工具 | 材质实例参数复制与粘贴、模型减面、自动 LOD、简单与复杂碰撞、资产检测 |

> [!WARNING]
> Rapid Packer 的贴图合并功能当前不可用。部分资产仍保留旧的 `/Game/Rapid_Packer` 引用，加载时可能报告缺失依赖。请在修复并重新保存相关资产前，不要依赖该功能。

### 工具界面

主入口资产：

```text
/ArtTool/Art_Tool
```

`Art_Tool` 通过 Widget Switcher 承载两个工具页面，两个页面均支持停靠窗口缩放和独立垂直滚动。

| 页签 | Widget | 用途 |
| --- | --- | --- |
| 编辑器工具 | `WBP_nSpaceDevTool` | 场景 Actor、调试视图和通用编辑器操作 |
| 资产工具 | `WBP_nSpaceDevTool_2` | 材质实例、模型、碰撞、贴图和资产检查 |

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

Lightmap Resolution 可选值：

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

调试辅助资产位于：

```text
Plugins/ArtTool/Content/ViewModes
Plugins/ArtTool/Content/UV
Plugins/ArtTool/Content/ColorCorrection
```

当前仅保留基础 ColorCorrection 流程。旧版 LUT 流程使用的 `BP_ColorCorrectionPost_Lut`、LUT 纹理、旧校正材质和参数集合已经移除，不再属于受支持功能。

### 资产工具

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

贴图处理资产位于：

```text
Plugins/ArtTool/Content/Rapid_Packer
```

Rapid Packer 加载时可能报告 `T_Black8x8` 依赖不可用。实际纹理位于 `/ArtTool/Rapid_Packer/Material/Textures/T_Black8x8`，但部分材质与材质函数仍引用 `/Game/Rapid_Packer/Material/Textures/T_Black8x8`。

## 推荐工作流

### 批量替换材质或模型

1. 在关卡中选择需要处理的 Actor。
2. 在 Details View 中设置源材质或源模型，以及目标材质或目标模型。
3. 检查选择范围，避免处理不相关对象。
4. 点击替换按钮。
5. 如需撤销本次映射，使用对应回退按钮或 Unreal Editor Undo。

### 清理空 Actor

1. 在关卡中选择待检查的 Actor。
2. 先运行“检测空 Actor”确认数量。
3. 再运行“删除空 Actor”。
4. 根据确认框决定是否处理包含子组件的空 Actor。
5. 完成后检查关卡并保存。

### Datasmith 元数据筛选

1. 选择需要筛选的 Datasmith Actor 集合。
2. 输入 Datasmith User Data Key 和需要精确匹配的 Value。
3. 点击筛选；不匹配的 Actor 会从当前选择中移除。

### 距离测量

1. 依次选择两个 Actor。
2. 点击“距离测量”。
3. 工具使用选择数组中的最后两个 Actor 作为端点。
4. 测量结果以厘米显示，并生成辅助箭头与端点。
5. 点击“清空”删除测量辅助对象。

## 依赖与配置

### 插件描述文件

`ArtTool.uplugin` 当前声明以下依赖：

| 插件 | 用途 |
| --- | --- |
| EditorScriptingUtilities | 编辑器 Actor、资产和工具脚本操作 |
| GeometryScripting | 静态网格体和几何处理 |
| DataprepEditor | 数据准备与导入工作流 |
| ScriptableToolsEditorMode | 可脚本化编辑器工具支持 |

### 额外要求

- Python Editor Script Plugin 是工具栏入口的实际必需依赖，但尚未写入 `ArtTool.uplugin` 的依赖列表，需要在目标工程中手动启用。
- 目标工程还需要将 `addWidget_plugins.py` 配置为 Startup Script，详见[快速开始](#快速开始)。
- Datasmith 筛选依赖 Datasmith Importer；部分模型编辑流程依赖 Modeling Tools Editor Mode。

## 已知限制

- 工具主要针对 Windows 编辑器工作流设计。
- 当前插件资产基于 Unreal Engine 5.7 制作，较早版本可能无法加载。
- 部分操作仅支持 Static Mesh Actor 或 Static Mesh Component。
- 调试工具会在关卡中生成辅助 Actor；不再使用时应关闭对应模式或执行清理。
- LUT 色彩校正、Custom UV、旧关卡工具和 Asset Replace 已从当前插件中移除。
- Rapid Packer 仍包含旧 `/Game/Rapid_Packer` 引用，贴图合并功能暂不可用。
- Editor Utility Widget 修改不会自动刷新已运行的实例，需关闭并重新打开工具页签。
- 插件当前没有自动化测试套件，发布前需要在测试工程中手动验证关键功能。

## 故障排查

### 工具栏按钮没有出现

- 确认 Python Editor Script Plugin 已启用。
- 确认 `addWidget_plugins.py` 已配置为 Startup Script。
- 检查 Output Log 中的 Python 错误。
- 重启 Unreal Editor。
- 使用 Content Browser 手动运行 `/ArtTool/Art_Tool`。

### 找不到插件内容

- 在 Content Browser Settings 中启用 `Show Plugin Content`。
- 确认插件位于 `<Project>/Plugins/ArtTool`。
- 确认 `ArtTool.uplugin` 已启用并成功加载。

### 工具窗口没有随停靠区域缩放

- 关闭并重新打开 `Art Tool` 页签。
- 确认运行的是 `/ArtTool/Art_Tool`，而不是旧的临时实例。
- 确认 `WidgetSwitcher_137` 和两个子 Widget 的 Slot 保持 Fill。

### Rapid Packer 报告 `T_Black8x8` 缺失

已知警告：

```text
/Game/Rapid_Packer/Material/Textures/T_Black8x8 不可用
```

插件内实际资产路径：

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

## 目录结构

```text
ArtTool/
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

## 开发说明

| 项目 | 路径 |
| --- | --- |
| 主工具入口 | `/ArtTool/Art_Tool` |
| 编辑器工具页面 | `/ArtTool/WBP_nSpaceDevTool` |
| 资产工具页面 | `/ArtTool/WBP_nSpaceDevTool_2` |
| 工具栏注册脚本 | `ArtTool/Content/Python/addWidget_plugins.py` |
| 插件版本信息 | `ArtTool/ArtTool.uplugin` |

核心资产为二进制 `.uasset`。修改后请在 Unreal Editor 中完成以下检查：

1. 编译所有相关 Blueprint，确认没有新增编译错误或警告。
2. 验证全部按钮、复选框和输入控件的事件绑定。
3. 在测试关卡中执行非破坏性冒烟测试。
4. 使用版本控制检查被修改的资产列表。
