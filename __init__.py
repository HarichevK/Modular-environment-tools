# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "ModularEnvironmentTools",
    "author": "KharichevKirill",
    "description": "",
    "blender": (5, 1),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}

from . import auto_load
from .props import ObjectScaleNamingProperties
from .props import AutoUnwrapProperties
import bpy

auto_load.init()


def register():
    auto_load.register()
    
    bpy.types.Scene.object_scale_naming = bpy.props.PointerProperty(
    type=ObjectScaleNamingProperties
    )
    
    bpy.types.Scene.auto_unwrap_props = bpy.props.PointerProperty(
        type=AutoUnwrapProperties 
    )


def unregister():
    
    del bpy.types.Scene.object_scale_naming
    del bpy.types.Scene.auto_unwrap_props
    
    auto_load.unregister()
