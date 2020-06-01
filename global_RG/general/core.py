################################################################################
__Script__      = 'global_RG.general.core'
__Author__      = 'Weerapot Chaoman'
__Version__     = 6.00
__Date__        = 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
module_list = []
module_list.append(['global_RG.general.module', 'alembic', 'alembic'])
module_list.append(['global_RG.general.module', 'attribute', 'attribute'])
module_list.append(['global_RG.general.module', 'average_vertex', 'average_vertex'])
module_list.append(['global_RG.general.module', 'blendshape', 'blendshape'])
module_list.append(['global_RG.general.module', 'camera', 'camera'])
module_list.append(['global_RG.general.module', 'clean_up', 'clean_up'])
module_list.append(['global_RG.general.module', 'color', 'color'])
module_list.append(['global_RG.general.module', 'compose_name', 'compose_name'])
module_list.append(['global_RG.general.module', 'controller', 'controller'])
module_list.append(['global_RG.general.module', 'create', 'create'])
module_list.append(['global_RG.general.module', 'curve', 'crv'])
module_list.append(['global_RG.general.module', 'deformer', 'deformer'])
module_list.append(['global_RG.general.module', 'follicle', 'follicle'])
module_list.append(['global_RG.general.module', 'misc', 'misc'])
module_list.append(['global_RG.general.module', 'natural_sort', 'natural_sort'])
module_list.append(['global_RG.general.module', 'nucleus', 'nucleus'])
module_list.append(['global_RG.general.module', 'outliner', 'outliner'])
module_list.append(['global_RG.general.module', 'playblast', 'playblast'])
module_list.append(['global_RG.general.module', 'preference', 'preference'])
module_list.append(['global_RG.general.module', 'soft_cluster', 'soft_cluster'])
module_list.append(['global_RG.general.module', 'text', 'text'])
module_list.append(['global_RG.general.module', 'uv', 'uv'])
module_list.append(['global_RG.general.module', 'xgen', 'xgen'])
if __project__ in __self_path__:
    local_path = __self_path__.split(__project__)[0]
    if not local_path in sys.path:
        sys.path.insert(0, local_path)
for module_data in module_list:
    parent, module, as_name = module_data
    cmd = 'import '
    if __project__ in __self_path__:
        cmd += __project__ + '.'
    if parent:
        cmd += parent + '.'
    cmd += module + ' as ' + as_name + ';'
    cmd += 'reload(' + as_name + ');'
    exec(cmd)
################################################################################
import random, re
import pymel.core as pm
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
from collections import OrderedDict
################################################################################

class General(
	alembic.Alembic,
    attribute.Attribute,
    average_vertex.AverageVertex,
    blendshape.Blendshape,
    camera.Camera,
    clean_up.CleanUp,
    color.Color,
    compose_name.ComposeName,
    controller.Controller,
    create.Create,
    crv.Curve,
    deformer.Deformer,
    follicle.Follicle,
    misc.Misc,
    natural_sort.NaturalSort,
    nucleus.Nucleus,
    outliner.Outliner,
    playblast.Playblast,
    preference.Preference,
    soft_cluster.SoftCluster,
    text.Text,
    uv.UV,
    # xgen.XGen,
    ):

    def __init__(self, *args, **kwargs):
        super(General, self).__init__(*args, **kwargs)
