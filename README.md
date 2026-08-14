<div align="center">

# ArtTool

**面向 Unreal Engine 美术与技术美术工作流的编辑器工具集**

<br />

[![Version](https://img.shields.io/badge/version-1.0-blue?style=flat-square)](ArtTool/ArtTool.uplugin)
[![Unreal Engine](https://img.shields.io/badge/Unreal%20Engine-UE5-0E1128?style=flat-square&logo=unrealengine)](https://www.unrealengine.com/)
[![Platform](https://img.shields.io/badge/platform-Editor%20Only-555?style=flat-square)](ArtTool/ArtTool.uplugin)
[![License](https://img.shields.io/badge/license-Epic%20Sample-green?style=flat-square)](ArtTool/Content/Python/addWidget_plugins.py)

<br />

将场景整理、批量替换、调试视图、模型处理、碰撞设置和资产检查<br />
整合到一个**可停靠的编辑器面板**中

</div>

---

## 简介

ArtTool 是基于 **Editor Utility Widget**、**Blueprint** 和 **Python 启动脚本** 构建的 Editor-only 插件，不包含 C++ `Source` 模块。主要逻辑由 Widget 蓝图与 Python 入口脚本组成，适合在 Windows 编辑器环境下快速集成到现有 TA 工作流。

> **注意**
>
> 本插件仅用于 Unreal Editor。删除空 Actor、移除碰撞、模型减面等操作会**直接修改关卡或资产**。执行批量操作前，请先保存关卡并确认已接入版本控制。

## 界面预览

<div align="center">
  <img src="docs/images/tool.png" alt="ArtTool 编辑器工具界面" width="48%" />
  &nbsp;
  <img src="docs/images/tool2.png" alt="ArtTool 资产工具界面" width="48%" />
</div>

## 目录

- [快速开始](#快速开始)
- [打开工具](#打开工具)
- [功能概览](#功能概览)
- [推荐工作流](#推荐工作流)
- [依赖与配置](#依赖与配置)
- [目录结构](#目录结构)
- [已知限制](#已知限制)
- [开发说明](#开发说明)

---

## 快速开始

### Step 1 · 安装插件

将仓库中的 `ArtTool/` 目录复制到目标 Unreal 项目：

```text
<YourProject>/Plugins/ArtTool
```

> 仓库根目录中的 `ArtTool/` 即插件根目录。文档里的 `Plugins/ArtTool/` 表示安装到目标工程后的路径。

### Step 2 · 启用依赖

`ArtTool.uplugin` 会自动启用以下核心依赖。首次安装后重启编辑器，并在 **Edit → Plugins** 中确认它们处于启用状态：

| 插件 | 必需 | 用途 |
| :-- | :--: | :-- |
| Editor Scripting Utilities | 是 | Actor、资产与工具脚本操作 |
| Geometry Scripting | 是 | 静态网格体与几何处理 |
| Dataprep Editor | 是 | 数据准备与导入工作流 |
| Scriptable Tools Editor Mode | 是 | 可脚本化编辑器工具 |
| Python Editor Script Plugin | 是 | 工具栏入口（由 `.uplugin` 自动启用） |
| Modeling Tools Editor Mode | 按需 | 部分模型编辑工作流 |

### Step 3 · 注册工具栏入口

在目标工程的 Python 插件配置中添加启动脚本：

```ini
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
+StartupScripts=addWidget_plugins.py
```

保存配置并**重启 Unreal Editor**。启动脚本会在 `LevelEditor.LevelEditorToolBar.User` 注册 **「美术工具」** 按钮。

### Step 4 · 验证安装

在编辑器中运行验证脚本 `ArtTool/Content/Python/verify_arttool.py`：

**Tools → Execute Python Script**，或在 Python 控制台执行：

```python
import verify_arttool; verify_arttool.run()
```

验证通过后，请在 `Art_Tool` 中手动确认两个页签均可正常显示与滚动。

---

## 打开工具

**首选方式：** 点击工具栏中的 **「美术工具」** 按钮。

**备用方式：** 在 Content Browser 中启用 `Show Plugin Content`，右键运行：

```text
/ArtTool/Art_Tool
```

---

## 功能概览

### 工具界面

主入口资产：`/ArtTool/Art_Tool`

`Art_Tool` 通过 **Widget Switcher** 承载两个工具页面，均支持停靠、缩放和独立垂直滚动：

| 页签 | Widget | 用途 |
| :-- | :-- | :-- |
| 编辑器工具 | `WBP_nSpaceDevTool` | 场景 Actor、调试视图、通用编辑器操作 |
| 资产工具 | `WBP_nSpaceDevTool_2` | 材质实例、模型、碰撞、贴图、资产检查 |

<details>
<summary><strong>场景 Actor 功能详情</strong></summary>

| 功能 | 说明 |
| :-- | :-- |
| 材质替换 | 批量查找指定材质，并按原材质槽位替换为目标材质 |
| 材质回退 | 将匹配的目标材质恢复为替换前材质 |
| 模型替换 | 批量替换 Static Mesh Actor 使用的静态网格体 |
| 模型回退 | 将匹配的目标网格体恢复为替换前网格体 |
| 光照分辨率 | 为选中的 Static Mesh Actor 设置固定或自适应光照分辨率 |
| 空 Actor 检测 | 统计当前选择中不包含有效静态网格体的 Actor |
| 空 Actor 删除 | 根据确认选项删除当前选择中的空 Actor |
| Datasmith 筛选 | 根据 Datasmith User Data 的键和值过滤当前选择 |
| 距离测量 | 测量最后选择的两个 Actor，并生成端点、箭头和距离文本 |
| 清空测量 | 删除距离测量生成的辅助 Actor |
| 工具实例化 | 注册并打开相关 Editor Utility 工具页签 |

</details>

<details>
<summary><strong>Debug 功能详情</strong></summary>

| 功能 | 说明 |
| :-- | :-- |
| 材质 Debug | 启用或关闭材质调试辅助视图 |
| UV 查看 | 为场景静态网格体赋予覆层材质，检测 UV 拉伸情况 |
| Lumen Reflections | 切换 Lumen 反射检查视图 |
| Specular Range | 切换高光范围检查视图 |

> 当前仅保留基础 **ColorCorrection** 流程。旧版 LUT 流程（`BP_ColorCorrectionPost_Lut`、LUT 纹理、旧校正材质和参数集合）已移除，不再受支持。

</details>

<details>
<summary><strong>资产工具功能详情</strong></summary>

| 功能 | 说明 |
| :-- | :-- |
| 材质实例参数复制 | 读取并暂存材质实例参数 |
| 材质实例参数粘贴 | 将暂存参数应用到目标材质实例 |
| 模型减面 | 按设置比例简化静态网格体 |
| 自动 LOD | 自动生成或设置静态网格体 LOD |
| 简单碰撞 | 配置并生成指定类型的简单碰撞 |
| 复杂碰撞 | 配置复杂碰撞方式 |
| 添加碰撞 | 对目标静态网格体添加碰撞 |
| 移除碰撞 | 移除目标静态网格体的碰撞数据 |
| 贴图合并 | 合并多张贴图，支持 RGBA 通道 |

</details>

---

## 推荐工作流

### 场景批量替换

1. 在关卡中选中目标 Actor 范围
2. 打开 **编辑器工具** 页签
3. 使用 **材质替换** 或 **模型替换** 执行批量操作
4. 如需撤销，使用对应的 **回退** 功能
5. 保存关卡并提交版本控制

### 资产检查与处理

1. 在 Content Browser 中选中目标 Static Mesh 或 Material Instance
2. 切换到 **资产工具** 页签
3. 按需执行减面、LOD、碰撞或贴图合并
4. 在测试关卡中验证结果后再提交资产

### Debug 视图切换

1. 打开 **编辑器工具** 页签中的 Debug 区域
2. 启用 UV Overlay、Lumen Reflections 等检查视图
3. 检查完成后**关闭对应模式**或执行清理，避免辅助 Actor 残留

---

## 依赖与配置

### 插件描述文件

[`ArtTool.uplugin`](ArtTool/ArtTool.uplugin) 声明的依赖：

| 插件 | 用途 |
| :-- | :-- |
| EditorScriptingUtilities | 编辑器 Actor、资产和工具脚本操作 |
| GeometryScripting | 静态网格体和几何处理 |
| DataprepEditor | 数据准备与导入工作流 |
| ScriptableToolsEditorMode | 可脚本化编辑器工具 |
| PythonScriptPlugin | 工具栏入口与 Python 启动脚本 |

### 额外要求

- 目标工程需将 `addWidget_plugins.py` 配置为 **Startup Script**（见 [快速开始](#快速开始)）
- **Modeling Tools Editor Mode** 为可选依赖，部分模型编辑工作流按需启用

### 安装验证

验证脚本 [`verify_arttool.py`](ArtTool/Content/Python/verify_arttool.py) 会检查：

| 检查项 | 说明 |
| :-- | :-- |
| 插件依赖 | `ArtTool.uplugin` 声明的依赖是否已启用 |
| 核心资产 | `Art_Tool`、`WBP_nSpaceDevTool`、`WBP_nSpaceDevTool_2` 是否存在 |
| 工具栏 | 工具栏菜单是否可访问 |
| 主界面 | Editor Utility Widget 是否能成功打开 |

### 资产版本管理

核心 Blueprint 与 Widget 为二进制 `.uasset` 文件，仓库通过 **Git LFS** 管理：

| 类型 | 路径模式 | 说明 |
| :-- | :-- | :-- |
| UE 资产 | `*.uasset`, `*.umap`, `*.ubulk`, `*.uexp` | 插件 Content 与关卡资产 |
| 文档截图 | `docs/images/**` | README 引用的界面预览图 |

```bash
git lfs install
git lfs pull
```

将本地 `.uasset` 纳入版本库前，确认 Git LFS 已跟踪对应扩展名（见 [`.gitattributes`](.gitattributes)），然后正常 `git add` 与 `git commit` 即可。

---

## 目录结构

```text
UE-ArtTool/
├── README.md
├── .gitignore
├── .gitattributes              # Git LFS 跟踪规则
├── docs/
│   └── images/                 # 界面预览截图
└── ArtTool/                    # 插件根目录 → 复制到 <Project>/Plugins/ArtTool
    ├── ArtTool.uplugin         # 插件描述与依赖声明
    ├── Config/
    │   └── FilterPlugin.ini    # 打包过滤配置
    └── Content/
        ├── Python/
        │   ├── addWidget_plugins.py   # 工具栏入口注册
        │   └── verify_arttool.py      # 安装验证脚本
        └── *.uasset            # Art_Tool, WBP_nSpaceDevTool 等核心资产
```

---

## 已知限制

| 限制 | 说明 |
| :-- | :-- |
| 平台 | 主要面向 **Windows** 编辑器工作流 |
| 对象类型 | 部分操作仅支持 Static Mesh Actor 或 Static Mesh Component |
| 辅助 Actor | Debug 与测量工具会在关卡中生成辅助 Actor，不使用时应关闭或清理 |
| 资产格式 | 核心逻辑为二进制 `.uasset`，需在 UE 编辑器中修改与验证 |

---

---

## 开发说明

### 关键路径

| 项目 | 路径 |
| :-- | :-- |
| 主工具入口 | `/ArtTool/Art_Tool` |
| 编辑器工具页面 | `/ArtTool/WBP_nSpaceDevTool` |
| 资产工具页面 | `/ArtTool/WBP_nSpaceDevTool_2` |
| 工具栏注册脚本 | [`ArtTool/Content/Python/addWidget_plugins.py`](ArtTool/Content/Python/addWidget_plugins.py) |
| 安装验证脚本 | [`ArtTool/Content/Python/verify_arttool.py`](ArtTool/Content/Python/verify_arttool.py) |
| 插件版本信息 | [`ArtTool/ArtTool.uplugin`](ArtTool/ArtTool.uplugin) |

### 修改后检查清单

- [ ] 编译所有相关 Blueprint，确认无新增编译错误或警告
- [ ] 验证全部按钮、复选框和输入控件的事件绑定
- [ ] 在测试关卡中执行非破坏性冒烟测试
- [ ] 使用版本控制检查被修改的资产列表

---

<div align="center">

**ArtTool** · Unreal Engine UE5 · Editor-only Plugin

</div>
