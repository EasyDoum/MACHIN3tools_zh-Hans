import bpy
from bpy.props import IntProperty, StringProperty, CollectionProperty, BoolProperty, EnumProperty
import os
import rna_keymap_ui
from . properties import AppendMatsCollection
from . utils.ui import get_icon
from . utils.registration import activate, get_path, get_name


preferences_tabs = [("GENERAL", "通用设置", ""),
                    ("KEYMAPS", "快捷键设置", ""),
                    ("ABOUT", "关于", "")]


links = [("Documentation", "https://machin3.io/MACHIN3tools/docs/", "INFO"),
         ("MACHINƎ作者官网", "https://machin3.io", "WORLD"),
         ("Youtube教程", "https://www.youtube.com/channel/UC4yaFzFDILd2yAqOWRuLOvA", "NONE"),
         ("Twitter推特", "https://twitter.com/machin3io", "NONE"),
         ("", "", ""),
         ("", "", ""),
         ("DECALmachine插件", "https://machin3.io/DECALmachine", "NONE"),
         ("MESHmachine插件", "https://machin3.io/MESHmachine", "NONE"),
         ("", "", ""),
         ("", "", ""),
         ("MACHINƎ @ Artstation地址", "https://www.artstation.com/artist/machin3", "NONE"),
         ("", "", ""),
         ]


# TODO: check if the append world/materials paths exist and make them abosolute


class MACHIN3toolsPreferences(bpy.types.AddonPreferences):
    path = get_path()
    bl_idname = get_name()


    # APPENDMATS

    def update_appendmatsname(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        else:
            if self.appendmatsname and self.appendmatsname not in self.appendmats:
                am = self.appendmats.add()
                am.name = self.appendmatsname

                self.appendmatsIDX = len(self.appendmats) - 1

            self.avoid_update = True
            self.appendmatsname = ""


    # CHECKS

    def update_switchmatcap1(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [mc.name for mc in context.preferences.studio_lights if os.path.basename(os.path.dirname(mc.path)) == "matcap"]
        if self.switchmatcap1 not in matcaps:
            self.avoid_update = True
            self.switchmatcap1 = "没有找到"

    def update_switchmatcap2(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [mc.name for mc in context.preferences.studio_lights if os.path.basename(os.path.dirname(mc.path)) == "matcap"]
        if self.switchmatcap2 not in matcaps:
            self.avoid_update = True
            self.switchmatcap2 = "没有找到"

    def update_custom_preferences_keymap(self, context):
        if self.custom_preferences_keymap:
            kc = context.window_manager.keyconfigs.user

            for km in kc.keymaps:
                if km.is_user_modified:
                    self.custom_preferences_keymap = False
                    self.dirty_keymaps = True
                    return

            self.dirty_keymaps = False


    # RUNTIME TOOL ACTIVATION

    def update_activate_smart_vert(self, context):
        activate(self, register=self.activate_smart_vert, tool="smart_vert")

    def update_activate_smart_edge(self, context):
        activate(self, register=self.activate_smart_edge, tool="smart_edge")

    def update_activate_smart_face(self, context):
        activate(self, register=self.activate_smart_face, tool="smart_face")

    def update_activate_clean_up(self, context):
        activate(self, register=self.activate_clean_up, tool="clean_up")

    def update_activate_clipping_toggle(self, context):
        activate(self, register=self.activate_clipping_toggle, tool="clipping_toggle")

    def update_activate_focus(self, context):
        activate(self, register=self.activate_focus, tool="focus")

    def update_activate_mirror(self, context):
        activate(self, register=self.activate_mirror, tool="mirror")

    def update_activate_align(self, context):
        activate(self, register=self.activate_align, tool="align")

    def update_activate_apply(self, context):
        activate(self, register=self.activate_apply, tool="apply")

    def update_activate_select(self, context):
        activate(self, register=self.activate_select, tool="select")

    def update_activate_mesh_cut(self, context):
        activate(self, register=self.activate_mesh_cut, tool="mesh_cut")

    def update_activate_customize(self, context):
        activate(self, register=self.activate_customize, tool="customize")

    def update_activate_filebrowser_tools(self, context):
        activate(self, register=self.activate_filebrowser_tools, tool="filebrowser")


    # RUNTIME PIE ACTIVATION

    def update_activate_modes_pie(self, context):
        activate(self, register=self.activate_modes_pie, tool="modes_pie")

    def update_activate_save_pie(self, context):
        activate(self, register=self.activate_save_pie, tool="save_pie")

    def update_activate_shading_pie(self, context):
        activate(self, register=self.activate_shading_pie, tool="shading_pie")

    def update_activate_views_pie(self, context):
        activate(self, register=self.activate_views_pie, tool="views_pie")

    def update_activate_align_pie(self, context):
        activate(self, register=self.activate_align_pie, tool="align_pie")

    def update_activate_cursor_pie(self, context):
        activate(self, register=self.activate_cursor_pie, tool="cursor_pie")

    def update_activate_transform_pie(self, context):
        activate(self, register=self.activate_transform_pie, tool="transform_pie")

    def update_activate_collections_pie(self, context):
        activate(self, register=self.activate_collections_pie, tool="collections_pie")

    def update_activate_workspace_pie(self, context):
        activate(self, register=self.activate_workspace_pie, tool="workspace_pie")


    # RUNTIME MENU ACTIVATION

    def update_activate_object_context_menu(self, context):
        activate(self, register=self.activate_object_context_menu, tool="object_context_menu")


    # PROPERTIES

    appendworldpath: StringProperty(name="世界环境的来源 (.blend格式)", subtype='FILE_PATH')
    appendworldname: StringProperty(name="世界环境的名称")

    appendmatspath: StringProperty(name="材质的来源 .blend", subtype='FILE_PATH')
    appendmats: CollectionProperty(type=AppendMatsCollection)
    appendmatsIDX: IntProperty()
    appendmatsname: StringProperty(name="追加材质的名称", update=update_appendmatsname)

    switchmatcap1: StringProperty(name="Matcap着色 1", update=update_switchmatcap1)
    switchmatcap2: StringProperty(name="Matcap着色 2", update=update_switchmatcap2)

    obj_mode_rotate_around_active: BoolProperty(name="围绕选择的对象旋转,但仅在对象模式使用", default=False)
    toggle_cavity: BoolProperty(name="在编辑模式下来回切换Cavity材质/Curvature材质,在对象模式下打开", default=True)

    focus_view_transition: BoolProperty(name="视图过渡运动", default=True)

    custom_startup: BoolProperty(name="起始场景", default=True)
    custom_workspaces: BoolProperty(name="工作空间", default=False)
    custom_theme: BoolProperty(name="主题", default=True)
    custom_matcaps: BoolProperty(name="材质捕获 (Matcaps) 着色和默认着色", default=True)
    custom_overlays: BoolProperty(name="叠加", default=True)
    custom_preferences_interface: BoolProperty(name="通用设置: 界面", default=True)
    custom_preferences_viewport: BoolProperty(name="通用设置: 视图", default=True)
    custom_preferences_navigation: BoolProperty(name="通用设置: 导航", default=True)
    custom_preferences_keymap: BoolProperty(name="通用设置: 快捷键", default=False, update=update_custom_preferences_keymap)
    custom_preferences_system: BoolProperty(name="通用设置: 系统", default=False)
    custom_preferences_save: BoolProperty(name="通用设置: 保存 & 载入", default=True)


    # MACHIN3tools

    activate_smart_vert: BoolProperty(name="智能工具-顶点", default=True, update=update_activate_smart_vert)
    activate_smart_edge: BoolProperty(name="智能工具-边", default=True, update=update_activate_smart_edge)
    activate_smart_face: BoolProperty(name="智能工具-面", default=True, update=update_activate_smart_face)
    activate_clean_up: BoolProperty(name="清理工具", default=True, update=update_activate_clean_up)
    activate_clipping_toggle: BoolProperty(name="视图裁切切换", default=True, update=update_activate_clipping_toggle)
    activate_focus: BoolProperty(name="对焦工具", default=True, update=update_activate_focus)
    activate_mirror: BoolProperty(name="镜像工具", default=True, update=update_activate_mirror)
    activate_align: BoolProperty(name="对齐工具", default=True, update=update_activate_align)
    activate_apply: BoolProperty(name="应用变换", default=True, update=update_activate_apply)
    activate_select: BoolProperty(name="选择助手", default=True, update=update_activate_select)
    activate_mesh_cut: BoolProperty(name="网格切割", default=True, update=update_activate_mesh_cut)
    activate_filebrowser_tools: BoolProperty(name="文件浏览器工具", default=True, update=update_activate_filebrowser_tools)
    activate_customize: BoolProperty(name="自定义", default=False, update=update_activate_customize)


    # MACHIN3pies

    activate_modes_pie: BoolProperty(name="Pie菜单-模式", default=True, update=update_activate_modes_pie)
    activate_save_pie: BoolProperty(name="保存Pie菜单", default=True, update=update_activate_save_pie)
    activate_shading_pie: BoolProperty(name="Pie菜单-着色", default=True, update=update_activate_shading_pie)
    activate_views_pie: BoolProperty(name="Pie菜单-视图", default=True, update=update_activate_views_pie)
    activate_align_pie: BoolProperty(name="Pie菜单-对齐", default=True, update=update_activate_align_pie)
    activate_cursor_pie: BoolProperty(name="Pie菜单-游标", default=True, update=update_activate_cursor_pie)
    activate_transform_pie: BoolProperty(name="Pie菜单-变换", default=True, update=update_activate_transform_pie)
    activate_collections_pie: BoolProperty(name="Pie菜单-集合", default=True, update=update_activate_collections_pie)
    activate_workspace_pie: BoolProperty(name="Pie菜单-工作空间", default=False, update=update_activate_workspace_pie)


    # MACHIN3menus
    activate_object_context_menu: BoolProperty(name="对象的索引菜单", default=True, update=update_activate_object_context_menu)




    # hidden

    tabs: EnumProperty(name="标签", items=preferences_tabs, default="GENERAL")
    avoid_update: BoolProperty(default=False)
    dirty_keymaps: BoolProperty(default=False)


    def draw(self, context):
        layout=self.layout


        # TAB BAR

        column = layout.column(align=True)
        row = column.row()
        row.prop(self, "tabs", expand=True)

        box = column.box()

        if self.tabs == "GENERAL":
            self.draw_general(box)

        elif self.tabs == "KEYMAPS":
            self.draw_keymaps(box)

        elif self.tabs == "ABOUT":
            self.draw_about(box)

    def draw_general(self, box):
        split = box.split()

        # LEFT

        b = split.box()
        b.label(text="激活")


        # MACHIN3tools

        bb = b.box()
        bb.label(text="工具")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_vert", toggle=True)
        row.label(text="智能顶点操控.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_edge", toggle=True)
        row.label(text="智能边的创建,操控和选择转换.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_smart_face", toggle=True)
        row.label(text="智能面的创建和从面创建对象.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_clean_up", toggle=True)
        row.label(text="几何体的快速清理.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_clipping_toggle", toggle=True)
        row.label(text="切换视图裁切平面.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_focus", toggle=True)
        row.label(text="对象与历史隔离.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_mirror", toggle=True)
        row.label(text="镜像对象+取消镜像")

        row = column.split(factor=0.25)
        row.prop(self, "activate_align", toggle=True)
        row.label(text="对象每个轴向的位置,旋转和缩放对齐.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_apply", toggle=True)
        row.label(text="应用变化时,同时保持倒角宽度和子变化不变")

        row = column.split(factor=0.25)
        row.prop(self, "activate_select", toggle=True)
        row.label(text="选择的助手.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_mesh_cut", toggle=True)
        row.label(text="切刀与网格相交,使用另一个对象.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_filebrowser_tools", toggle=True)
        row.label(text="文件浏览器的其余工具.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_customize", toggle=True)
        row.label(text="自定义各种Blender的首选项，设置和快捷键映射.")


        # MACHIN3pies

        bb = b.box()
        bb.label(text="Pie菜单")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_modes_pie", toggle=True)
        row.label(text="快速进行模式切换.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_save_pie", toggle=True)
        row.label(text="保存、打开、追加。载入“最近文件”、“上一个”和“下一个”。追加世界环境和材质.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_shading_pie", toggle=True)
        row.label(text="控制着色,覆盖,eevee和一些对象的属性.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_views_pie", toggle=True)
        row.label(text="控制视图,创建和控制摄像机.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_align_pie", toggle=True)
        row.label(text="使网格对齐.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_cursor_pie", toggle=True)
        row.label(text="操控游标和原点.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_transform_pie", toggle=True)
        row.label(text="变换方向和轴.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_collections_pie", toggle=True)
        row.label(text="集合管理.")

        row = column.split(factor=0.25)
        row.prop(self, "activate_workspace_pie", toggle=True)
        r = row.split(factor=0.4)
        r.label(text="切换工作空间.")
        r.label(text="如果启用，请在ui/pies.py中对其进行自定义", icon="INFO")


        # MACHIN3menus

        bb = b.box()
        bb.label(text="菜单")

        column = bb.column()

        row = column.split(factor=0.25)
        row.prop(self, "activate_object_context_menu", toggle=True)
        row.label(text="对象的索引菜单,访问类型的工具,没有快捷键映射.")


        # RIGHT

        b = split.box()
        b.label(text="设置")

        # FOCUS

        if getattr(bpy.types, "MACHIN3_OT_focus", False):
            bb = b.box()
            bb.label(text="对焦")

            column = bb.column()
            column.prop(self, "focus_view_transition")


        # CUSTOMIZE

        if getattr(bpy.types, "MACHIN3_OT_customize", False):
            bb = b.box()
            bb.label(text="自定义")

            bbb = bb.box()
            column = bbb.column()

            row = column.row()
            row.prop(self, "custom_startup")
            row.prop(self, "custom_workspaces")
            row.prop(self, "custom_theme")
            row.prop(self, "custom_matcaps")
            row.prop(self, "custom_overlays")

            bbb = bb.box()
            column = bbb.column()

            row = column.row()

            col = row.column()
            col.prop(self, "custom_preferences_interface")
            col.prop(self, "custom_preferences_viewport")

            col = row.column()
            col.prop(self, "custom_preferences_navigation")
            col.prop(self, "custom_preferences_keymap")

            col = row.column()
            col.prop(self, "custom_preferences_system")
            col.prop(self, "custom_preferences_save")

            if self.dirty_keymaps:
                row = column.row()
                row.label(text="已修改了快捷键，请先还原它们.", icon="ERROR")
                row.operator("machin3.restore_keymaps", text="立刻恢复")
                row.label()

            column = bb.column()
            row = column.row()

            row.label()
            row.operator("machin3.customize", text="Customize")
            row.label()


        # MODES PIE

        if getattr(bpy.types, "MACHIN3_MT_modes_pie", False):
            bb = b.box()
            bb.label(text="Pie菜单-模式")

            column = bb.column()

            column.prop(self, "toggle_cavity")


        # SAVE PIE

        if getattr(bpy.types, "MACHIN3_MT_save_pie", False):
            bb = b.box()
            bb.label(text="保存Pie菜单: 追加世界环境和材质")

            column = bb.column()

            column.prop(self, "appendworldpath")
            column.prop(self, "appendworldname")
            column.separator()

            column.prop(self, "appendmatspath")


            column = bb.column()

            row = column.row()
            rows = len(self.appendmats) if len(self.appendmats) > 6 else 6
            row.template_list("MACHIN3_UL_append_mats", "", self, "appendmats", self, "appendmatsIDX", rows=rows)

            c = row.column(align=True)
            c.operator("machin3.move_appendmat", text="", icon='TRIA_UP').direction = "UP"
            c.operator("machin3.move_appendmat", text="", icon='TRIA_DOWN').direction = "DOWN"

            c.separator()
            c.operator("machin3.clear_appendmats", text="", icon='LOOP_BACK')
            c.operator("machin3.remove_appendmat", text="", icon_value=get_icon('cancel'))
            c.separator()
            c.operator("machin3.populate_appendmats", text="", icon='MATERIAL')
            c.operator("machin3.rename_appendmat", text="", icon='OUTLINER_DATA_FONT')


            row = column.row()
            row.prop(self, "appendmatsname")
            row.operator("machin3.add_separator", text="", icon_value=get_icon('separator'))


        # SHADING PIE

        if getattr(bpy.types, "MACHIN3_MT_shading_pie", False):
            bb = b.box()
            bb.label(text="Pie菜单-着色: 切换Matcap着色")

            column = bb.column()

            row = column.row()

            row.prop(self, "switchmatcap1")
            row.prop(self, "switchmatcap2")


        # NO SETTINGS

        if not any([getattr(bpy.types, "MACHIN3_" + name, False) for name in ["MT_modes_pie", "MT_save_pie", "MT_shading_pie"]]):
            b.label(text="工具或Pie菜单未激活.")

    def draw_keymaps(self, box):
        wm = bpy.context.window_manager
        # kc = wm.keyconfigs.addon
        kc = wm.keyconfigs.user

        from . registration import keys

        split = box.split()

        b = split.box()
        b.label(text="工具")

        if not self.draw_tool_keymaps(kc, keys, b):
            b.label(text="没有可用的键盘映射，因为没有激活任何工具。")


        b = split.box()
        b.label(text="Pie菜单")

        if not self.draw_pie_keymaps(kc, keys, b):
            b.label(text="快捷键创建失败,因为没有激活任何Pie菜单.")

    def draw_about(self, box):
        column = box.column()

        for idx, (text, url, icon) in enumerate(links):
            if idx % 2 == 0:
                row = column.row()
                if text == "":
                    row.separator()
                else:
                    row.operator("wm.url_open", text=text, icon=icon).url = url
            else:
                if text == "":
                    row.separator()
                else:
                    row.operator("wm.url_open", text=text, icon=icon).url = url

    def draw_tool_keymaps(self, kc, keysdict, layout):
        drawn = False

        for name in keysdict:
            if "PIE" not in name:
                keylist = keysdict.get(name)

                if self.draw_keymap_items(kc, name, keylist, layout):
                    drawn = True

        return drawn

    def draw_pie_keymaps(self, kc, keysdict, layout):
        drawn = False

        for name in keysdict:
            if "PIE" in name:
                keylist = keysdict.get(name)

                if self.draw_keymap_items(kc, name, keylist, layout):
                    drawn = True

        return drawn

    def draw_keymap_items(self, kc, name, keylist, layout):
        drawn = False

        for idx, item in enumerate(keylist):
            keymap = item.get("keymap")

            if keymap:
                km = kc.keymaps.get(keymap)

                kmi = None
                if km:
                    idname = item.get("idname")

                    for kmitem in km.keymap_items:
                        if kmitem.idname == idname:
                            properties = item.get("properties")

                            if properties:
                                if all([getattr(kmitem.properties, name, None) == value for name, value in properties]):
                                    kmi = kmitem
                                    break

                            else:
                                kmi = kmitem
                                break

                # draw keymap item

                if kmi:
                    # multi kmi tools, will only have a single box, created for the first kmi
                    if idx == 0:
                        box = layout.box()

                    # single kmi tools, get their label from the title
                    if len(keylist) == 1:
                        label = name.title().replace("_", " ")

                    # multi kmi tools, get it from the label tag, while the title is printed once, before the first item
                    else:
                        if idx == 0:
                            box.label(text=name.title().replace("_", " "))

                        label = item.get("label")

                    row = box.split(factor=0.15)
                    row.label(text=label)

                    # layout.context_pointer_set("keymap", km)
                    rna_keymap_ui.draw_kmi(["ADDON", "USER", "DEFAULT"], kc, km, kmi, row, 0)

                    drawn = True
        return drawn
