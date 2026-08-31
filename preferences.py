import bpy
import rna_keymap_ui

PANEL_ID = "panel.modular_environment_tools"

# The panel has no bl_category, so no sidebar tab ever appears for it. The only
# way in is a popup, and the shortcut below is what opens it.
KEYMAP_NAME = "3D View"
KEYMAP_SPACE_TYPE = "VIEW_3D"

addon_keymaps = []


class ModularEnvironmentToolsPreferences(bpy.types.AddonPreferences):
    # Must match the add-on module name. For a module that sits next to
    # __init__.py, __package__ is exactly the add-on package.
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout

        layout.label(text="The panel opens as a popup: it has no tab in the sidebar.")

        row = layout.row()
        row.operator("wm.call_panel", text="Open panel", icon="WINDOW").name = PANEL_ID

        box = layout.box()
        box.label(text="Setup Keymap")

        kc = context.window_manager.keyconfigs.user
        km = kc.keymaps.get(KEYMAP_NAME)

        if km is None:
            box.label(text="Keymap \"%s\" not found" % KEYMAP_NAME, icon="ERROR")
            return

        col = box.column()
        col.context_pointer_set("keymap", km)
        col.label(text=km.name)

        found = False

        for kmi in km.keymap_items:
            if kmi.idname != "wm.call_panel":
                continue
            if getattr(kmi.properties, "name", "") != PANEL_ID:
                continue
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
            found = True

        if not found:
            col.label(text="Shortcut is missing - switch the add-on off and on", icon="ERROR")


def register():
    kc = bpy.context.window_manager.keyconfigs.addon

    # There is no add-on keyconfig in background mode.
    if kc is None:
        return

    km = kc.keymaps.new(name=KEYMAP_NAME, space_type=KEYMAP_SPACE_TYPE)
    kmi = km.keymap_items.new("wm.call_panel", "C", "PRESS", shift=True)
    kmi.properties.name = PANEL_ID
    addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()
