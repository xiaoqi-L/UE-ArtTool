# Copyright Epic Games, Inc. All Rights Reserved.

import unreal

menu_owner = "editorUtilities"
tool_menus = unreal.ToolMenus.get()
owning_menu_name = "LevelEditor.LevelEditorToolBar.User"

@unreal.uclass()
class createEntry_Example(unreal.ToolMenuEntryScript):
    
    @unreal.ufunction(override=True)
    def execute(self, context):
        registry = unreal.AssetRegistryHelpers.get_asset_registry()
        asset = unreal.EditorAssetLibrary.load_asset("/ArtTool/Art_Tool")
        bp = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem).find_utility_widget_from_blueprint(asset)
        
        if bp == None:
            bp = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem).spawn_and_register_tab(asset)
        
    def init_as_toolbar_button(self):
        self.data.menu = owning_menu_name
        self.data.advanced.entry_type = unreal.MultiBlockType.TOOL_BAR_BUTTON
        self.data.icon = unreal.ScriptSlateIcon("EditorStyle", "Launcher.EditSettings")

def Run():    
    entry = createEntry_Example()
    entry.init_as_toolbar_button()
    entry.init_entry(menu_owner, "editorUtilitiesExampleEntry", "", "", "Example Button", "美术工具")
    toolbar = tool_menus.extend_menu(owning_menu_name)
    toolbar.add_menu_entry_object(entry)
    tool_menus.refresh_all_widgets()

Run()