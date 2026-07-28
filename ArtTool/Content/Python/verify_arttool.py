# Copyright Epic Games, Inc. All Rights Reserved.
#
# Run inside Unreal Editor after installing the ArtTool plugin:
#   Tools -> Execute Python Script -> verify_arttool.py
# Or from the Python console:
#   import verify_arttool; verify_arttool.run()

import unreal

REQUIRED_ASSETS = (
    "/ArtTool/Art_Tool",
    "/ArtTool/WBP_nSpaceDevTool",
    "/ArtTool/WBP_nSpaceDevTool_2",
)

REQUIRED_PLUGINS = (
    "EditorScriptingUtilities",
    "GeometryScripting",
    "DataprepEditor",
    "ScriptableToolsEditorMode",
    "PythonScriptPlugin",
)


def _log(message, level="info"):
    prefix = "[ArtTool Verify]"
    if level == "error":
        unreal.log_error(f"{prefix} {message}")
    elif level == "warning":
        unreal.log_warning(f"{prefix} {message}")
    else:
        unreal.log(f"{prefix} {message}")


def _check_assets(errors):
    for asset_path in REQUIRED_ASSETS:
        if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
            _log(f"Asset found: {asset_path}")
        else:
            errors.append(f"Missing asset: {asset_path}")


def _check_main_tool(errors):
    asset_path = "/ArtTool/Art_Tool"
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        return

    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if asset is None:
        errors.append(f"Failed to load asset: {asset_path}")
        return

    utility_subsystem = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
    widget = utility_subsystem.find_utility_widget_from_blueprint(asset)
    if widget is None:
        widget = utility_subsystem.spawn_and_register_tab(asset)

    if widget is None:
        errors.append("Failed to open Editor Utility Widget for /ArtTool/Art_Tool")
        return

    _log("Editor Utility Widget opened successfully: /ArtTool/Art_Tool")


def _check_toolbar_entry(errors):
    tool_menus = unreal.ToolMenus.get()
    menu = tool_menus.find_menu("LevelEditor.LevelEditorToolBar.User")
    if menu is None:
        errors.append("Toolbar menu not found: LevelEditor.LevelEditorToolBar.User")
        return

    _log("Toolbar menu found. Confirm the '美术工具' button appears after editor restart.")


def _check_plugins(warnings):
    enabled_plugins = set(unreal.PluginBlueprintLibrary.get_enabled_plugin_names())
    for plugin_name in REQUIRED_PLUGINS:
        if plugin_name in enabled_plugins:
            _log(f"Plugin enabled: {plugin_name}")
        else:
            warnings.append(f"Plugin not enabled: {plugin_name}")


def run():
    errors = []
    warnings = []

    _log("Starting ArtTool installation verification...")
    _check_plugins(warnings)
    _check_assets(errors)
    _check_toolbar_entry(errors)

    if not errors:
        _check_main_tool(errors)

    for warning in warnings:
        _log(warning, "warning")

    if errors:
        for error in errors:
            _log(error, "error")
        _log(f"Verification failed with {len(errors)} error(s).", "error")
        return False

    _log("Verification passed. Open both tabs in Art_Tool and run a non-destructive smoke test.")
    return True


if __name__ == "__main__":
    run()
