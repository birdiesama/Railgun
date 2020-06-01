################################################################################
__Script__  = 'utils_RG.simulation_setup.core'
__Author__	= 'Weerapot Chaoman'
__Version__	= 2.00
__Date__	= 20200510
################################################################################
import os, re, sys
import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMayaUI as mui
from random import shuffle
################################################################################
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
module_list = []
module_list.append(['global_RG.general', 'core', 'general'])
module_list.append(['global_RG.ui', 'core', 'ui'])
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
try:
    from global_RG.Qt import Qt, QtCore, QtGui, QtWidgets, QtCompat
except:
    cmd = 'from '
    if __project__ in __self_path__:
        cmd += __project__ + '.'
    cmd += 'global_RG.Qt'
    cmd += ' import Qt, QtCore, QtGui, QtWidgets, QtCompat'
    exec(cmd)
################################################################################

class SimulationSetup(general.General):

    def __init__(self):
        super(SimulationSetup, self).__init__()

        self.info_topNode   = ['cfx', None]

        self.info_input         = ['INPUT', 'orange'] # 'INPUT_ANIM_GRP'
        self.info_input_attr    = ['INPUT', 'orange']
        # self.info_input_layer   = ['_INPUT_', 'orange'] # '_input_anim_'

        self.info_sim           = ['SIM', 'light_blue'] # 'SIMULATION_GRP'
        self.info_sim_attr      = ['SIM', 'light_blue']
        # self.info_sim_layer     = ['_SIM_', 'light_blue'] # '_simulation_'

        self.info_output        = ['OUTPUT', 'green'] # 'OUTPUT_SIM_GRP'
        self.info_output_attr   = ['OUTPUT', 'green']
        # self.info_output_layer  = ['_OUTPUT_', 'green'] # '_output_sim_'

        # namespace
        self.namespace_input = 'input'
        self.namespace_output = 'output'

        # INPUT
        self.name_cache_in      = 'input_anim'
        self.info_sim_input         = ['sim_input', None]
        self.info_collider_input    = ['collider_input', None]
        self.info_collider_input_wrap = ['collider_input_wrap', None]
        self.info_cloth_input       = ['cloth_input', None]
        self.info_cloth_input_wrap  = ['cloth_input_wrap', None]
        self.info_nHair_input       = ['nHair_input', None]

        # SIM
        self.info_solver    = ['solver', None]

        self.name_cache_in_loc = 'input_anim_loc'
        self.name_solver_mm_ref = 'solver_mm_loc'

        self.info_ref = ['ref_loc_grp', None]
        self.name_ref_fol = 'ref_fol'
        self.name_ref_loc = 'ref_loc'

        self.info_collider  = ['collider', None]
        self.info_nRigid    = ['nRigid', None]
        self.info_cloth     = ['cloth', None]
        self.info_nCloth    = ['nCloth', None]
        self.info_utils     = ['utils', None]
        self.info_wrap      = ['wrap', None]
        self.info_nConstraint = ['nConstraint', None]

        # SUFFIX
        self.suffix_cache_in    = 'iAnim'
        self.suffix_cloth       = 'cloth'
        self.suffix_input_cloth = 'iCloth'
        self.suffix_col         = 'col'
        self.suffix_input_col   = 'iCol'
        self.suffix_techAnim_lowRes = 'lowRes'
        self.suffix_techAnim_highRes = 'highRes'
        self.suffix_folDriver = 'folDriver'

        # OUTPUT
        self.info_techAnim          = ['tech_anim', None]
        self.info_techAnim_lowRes   = ['low_res', None]
        self.info_techAnim_highRes  = ['high_res', None]
        self.info_techAnim_highRes_wrap = ['high_res_wrap', None]
        self.info_publish           = ['publish', 'green']
        self.info_publish_wrap      = ['publish_wrap', None]

        self.name_publish_set   = 'publish_set'

        # RegEx
        self.skin_color = 'skin'
        self.eye_color = 'white'
        self.body_regex = re.compile(r'body|skin', re.IGNORECASE)
        self.eye_regex = re.compile(r'eye|pupil|len', re.IGNORECASE)
        self.eye_exception_regex = re.compile(r'eyelash|eyebrow', re.IGNORECASE)

        # Color
        self.color_list = ['light_sea_green', 'light_green', 'light_yellow', 'light_orange', 'light_red', 'light_brown', 'light_purple', 'light_pink']
        self.mono_color_list = ['black', 'dark_grey', 'grey', 'light_grey']

    def init_hierarchy(self):

        top_node = self.create_group(name = self.info_topNode[0], color = self.info_topNode[1])
        self.lock_hide_attr(top_node)
        
        ### MAIN groups ###
        input   = self.create_group(name = self.info_input[0], color = self.info_input[1], parent = top_node)
        sim     = self.create_group(name = self.info_sim[0], color = self.info_sim[1], parent = top_node)
        output  = self.create_group(name = self.info_output[0], color = self.info_output[1], parent = top_node)
        self.lock_hide_attr([input, sim, output])

        # sim
        solver_grp  = self.create_group(name = self.info_solver[0], parent = sim)
        utils_grp   = self.create_group(name = self.info_utils[0], parent = sim)
        wrap_grp    = self.create_group(name = self.info_wrap[0], parent = utils_grp)
        self.lock_hide_attr([utils_grp, wrap_grp])

        # output
        techAnim            = self.create_group(name = self.info_techAnim[0], color = self.info_techAnim[1], parent = output)
        techAnim_lowRes     = self.create_group(name = self.info_techAnim_lowRes[0], color = self.info_techAnim_lowRes[1], parent = techAnim)
        techAnim_highRes    = self.create_group(name = self.info_techAnim_highRes[0], color = self.info_techAnim_highRes[1], parent = techAnim)
        publish             = self.create_group(name = self.info_publish[0], color = self.info_publish[1], parent = output)
        self.lock_hide_attr([techAnim, techAnim_lowRes, techAnim_highRes, publish])

        # set
        publish_set = self.create_set(name = self.name_publish_set)
        pm.sets(publish_set, add = publish)

        ### add main attributes on top_node ###

        # __solver__
        top_node.addAttr('__solver__', keyable = True, attributeType = 'enum', enumName = '======:')
        top_node.__solver__.lock()

        top_node.addAttr('enable', keyable = True, attributeType = 'bool', dv = 0)
        top_node.addAttr('start_frame', keyable = True, attributeType = 'float', dv = 0)

        if pm.getAttr(top_node.start_frame, settable = True):
            expression = 'start_frame = `playbackOptions -q -min`;'
            pm.expression(object = top_node, string = expression)

        top_node.addAttr('preroll_amount', keyable = True, attributeType = 'float', dv = 10, min = 0)
        top_node.addAttr('tPose_en', keyable = True, attributeType = 'float', max = 1, min = 0, dv = 1)
        top_node.addAttr('tPose_val', keyable = True, attributeType = 'float', max = 1, min = 0, dv = 1)

        # create node network for tPose_val
        preroll_en_1_indiv_val_mdv = self.create_mdv(name = 'preroll_en_1_indiv_val_mdv', mode = 'divide')
        preroll_en_1_indiv_val_pma = self.create_pma(name = 'preroll_en_1_indiv_val_pma', mode = 'minus')
        preroll_en_2_sum_val_mdv = self.create_mdv(name = 'preroll_en_2_sum_val_mdv', mode = 'multiply')
        preroll_en_3_raw_val_pma = self.create_pma(name = 'preroll_en_3_raw_val_pma', mode = 'minus')
        preroll_en_4_final_val_clamp = self.create_clamp(name = 'preroll_en_4_final_val_clamp', max = 1, min = 0)
        
        time_node = pm.ls(type = 'time')[0]

        preroll_en_3_raw_val_pma.input2D[0].input2Dx.set(1)
        preroll_en_2_sum_val_mdv.ox >> preroll_en_3_raw_val_pma.input2D[1].input2Dx
        preroll_en_3_raw_val_pma.output2D.output2Dx >> preroll_en_4_final_val_clamp.ipr
        preroll_en_4_final_val_clamp.opr >> top_node.tPose_val
        top_node.tPose_val.lock()

        preroll_en_1_indiv_val_mdv.i1x.set(1)
        top_node.preroll_amount >> preroll_en_1_indiv_val_mdv.i2x

        time_node.outTime >> preroll_en_1_indiv_val_pma.input2D[0].input2Dx
        top_node.start_frame >> preroll_en_1_indiv_val_pma.input2D[1].input2Dx

        preroll_en_1_indiv_val_mdv.ox >> preroll_en_2_sum_val_mdv.i1x
        preroll_en_1_indiv_val_pma.output2D.output2Dx >> preroll_en_2_sum_val_mdv.i2x

        if pm.getAttr(top_node.tPose_val, settable = True):
            expression = 'tPose_val = (1/`playbackOptions -q -min`;'
            pm.expression(object = top_node, string = expression)

        # __visibility__
        top_node.addAttr('__visibility__', keyable = True, attributeType = 'enum', enumName = '======:')
        top_node.__visibility__.lock()
        top_node.addAttr(self.info_input_attr[0], keyable = True, attributeType = 'bool', dv = 0)
        top_node.addAttr(self.info_sim_attr[0], keyable = True, attributeType = 'bool', dv = 1)
        top_node.addAttr(self.info_output_attr[0], keyable = True, attributeType = 'bool', dv = 0)

        top_node_attr_input = pm.PyNode('{0}.{1}'.format(top_node.nodeName(), self.info_input_attr[0]))
        top_node_attr_sim = pm.PyNode('{0}.{1}'.format(top_node.nodeName(), self.info_sim_attr[0]))
        top_node_attr_output = pm.PyNode('{0}.{1}'.format(top_node.nodeName(), self.info_output_attr[0]))

        pm.connectAttr(top_node_attr_input, input.v)
        pm.connectAttr(top_node_attr_sim, sim.v)
        pm.connectAttr(top_node_attr_output, output.v)

        # __solver_motion_mult__
        top_node.addAttr('__solver_motion_mult__', keyable = True, attributeType = 'enum', enumName = '======:')
        top_node.__solver_motion_mult__.lock()
        top_node.addAttr('smm_translate', keyable = True, attributeType = 'float', dv = 1)
        top_node.addAttr('smm_tx', keyable = True, attributeType = 'float', dv = 1)
        top_node.addAttr('smm_ty', keyable = True, attributeType = 'float', dv = 1)
        top_node.addAttr('smm_tz', keyable = True, attributeType = 'float', dv = 1)
        top_node.addAttr('smm_rotate', keyable = True, attributeType = 'float', dv = 1)
        top_node.addAttr('smm_rx', keyable = True, attributeType = 'float', dv = 1)
        top_node.addAttr('smm_ry', keyable = True, attributeType = 'float', dv = 1)
        top_node.addAttr('smm_rz', keyable = True, attributeType = 'float', dv = 1)

        # create solver motion mult network, with locator as a reference point

        solver_mm_ref = self.create_locator(name = self.name_solver_mm_ref, parent = utils_grp)

        smm_t_1_indiv_amp_mdv = self.create_mdv(name = 'smm_t_1_indiv_amp_mdv', mode = 'multiply')
        smm_t_2_glob_amp_mdv = self.create_mdv(name = 'smm_t_2_glob_amp_mdv', mode = 'multiply')
        smm_t_3_final_val_pma = self.create_pma(name = 'smm_t_3_final_val_pma', mode = 'minus')

        smm_r_1_indiv_amp_mdv = self.create_mdv(name = 'smm_r_1_indiv_amp_mdv', mode = 'multiply')
        smm_r_2_glob_amp_mdv = self.create_mdv(name = 'smm_r_2_glob_amp_mdv', mode = 'multiply')
        smm_r_3_final_val_pma = self.create_pma(name = 'smm_r_3_final_val_pma', mode = 'minus')

        for axis in ['x', 'y', 'z']:
            for attr, attribute in zip(['t', 'r'], ['translate', 'rotate']):
                exec('solver_mm_ref.{0}{1} >> smm_{0}_1_indiv_amp_mdv.i1{1}'.format(attr, axis))
                exec('top_node.smm_{0}{1} >> smm_{0}_1_indiv_amp_mdv.i2{1}'.format(attr, axis))

                exec('smm_{0}_1_indiv_amp_mdv.o{1} >> smm_{0}_2_glob_amp_mdv.i1{1}'.format(attr, axis))
                exec('top_node.smm_{2} >> smm_{0}_2_glob_amp_mdv.i2{1}'.format(attr, axis, attribute))               

                exec('solver_mm_ref.{0}{1} >> smm_{0}_3_final_val_pma.input3D[0].input3D{1}'.format(attr, axis))
                exec('smm_{0}_2_glob_amp_mdv.o{1} >> smm_{0}_3_final_val_pma.input3D[1].input3D{1}'.format(attr, axis))

                exec('smm_{0}_3_final_val_pma.output3D.output3D{1} >> solver_grp.{0}{1}'.format(attr, axis))

        pm.select(clear = True)

    def init_geo_grp(self, geo_grp_list=None):

        # initiate groups
        input = self.create_group(name = self.info_input[0])
        publish = self.create_group(name = self.info_publish[0])
        utils_grp = self.create_group(name = self.info_utils[0])
        solver_grp = self.create_group(name = self.info_solver[0])

        # add name space
        namespace_input = self.create_namespace(self.namespace_input)
        namespace_output = self.create_namespace(self.namespace_output)

        self.skin_color = 'skin'
        self.eye_color = 'white'
        self.body_regex = re.compile(r'body|skin|head', re.IGNORECASE)
        self.eye_regex = re.compile(r'eye|pupil|len', re.IGNORECASE)
        self.eye_exception_regex = re.compile(r'eyelash|eyebrow', re.IGNORECASE)

        # create publish_set
        publish_set = self.create_set(name = self.name_publish_set)

        cache_in_grp = self.create_group(name = self.name_cache_in, parent = input)
        self.lock_hide_attr(cache_in_grp)

        # duplicate selected geo group, for input and output
        for geo_grp in geo_grp_list:

            geo_grp = pm.PyNode(geo_grp)
            geo_grp_name = geo_grp.nodeName()
            
            input_geo_grp = pm.duplicate(geo_grp)[0]
            output_geo_grp = pm.duplicate(geo_grp)[0]

            for dup_geo_grp, namespace in zip([input_geo_grp, output_geo_grp], [namespace_input, namespace_output]):
                dup_geo_grp.rename('{0}:{1}'.format(namespace, geo_grp_name))
                tfm_list = dup_geo_grp.listRelatives(ad = True, type = 'transform')
                tfm_list = list(set(tfm_list))        
                for tfm in tfm_list:
                    tfm.rename('{0}:{1}'.format(namespace, tfm.nodeName()))

            pm.parent(input_geo_grp, cache_in_grp)
            pm.parent(output_geo_grp, publish)
            self.lock_hide_attr([input_geo_grp, output_geo_grp])

        # coloring geo_grp
        for geo_grp, color_list in zip([cache_in_grp, publish], [self.mono_color_list, self.color_list]):

            shuffle(color_list)
            mesh_shape_list = pm.listRelatives(geo_grp, ad = True, type = 'mesh')
            mesh_list = pm.listRelatives(mesh_shape_list, parent = True)
            mesh_list = list(set(mesh_list))

            for i in range(0, len(mesh_list)):
                mesh = mesh_list[i]
                color = color_list[i%len(color_list)]
                if self.body_regex.findall(str(mesh)):
                    if geo_grp != cache_in_grp:
                        color = self.skin_color
                    else:
                        pass
                elif self.eye_regex.findall(mesh.nodeName()):
                    if not self.eye_exception_regex.findall(mesh.nodeName()):
                        color = self.eye_color
                self.assign_poly_shader(target_list = mesh, color_name = color)

        # create cache_in_rivet -- for default nucleus motion mult
        cache_in_loc = self.create_locator(name = self.name_cache_in_loc)

        for axis in ['x', 'y', 'z']:
            exec("cache_in_grp.boundingBoxCenter{0} >> cache_in_loc.t{1}".format(axis.upper(), axis))
        pm.parent(cache_in_loc, utils_grp)

        # create blend color and attributes
        # addAttr('from_collider_deformer', keyable = True, attributeType = 'float', max = 1, min = 0, dv = 1)


    def ssu_create_nRigid(self):
        # temporary done, but need to select something from hierarchy or else it will not work
        # must select something from sim rig hierarchy (input, publish)

        # check if nucleus existsnucleus 1/2
        parent_nucleus_stat = None
        nucleus_list = pm.ls(type = 'nucleus')
        if not nucleus_list:
            parent_nucleus_stat = True

        # start operation based on selecion
        selection_list = pm.ls(sl = True)

        # set variables
        input   = self.create_group(name = self.info_input[0])
        sim     = self.create_group(name = self.info_sim[0])
        publish = self.create_group(name = self.info_publish[0])
        utils_grp       = self.create_group(name = self.info_utils[0])
        wrap_grp    = self.create_group(name = self.info_wrap[0])

        if not pm.attributeQuery('from_collider_deformer', node = publish, exists = True):
            publish.addAttr('from_collider_deformer', keyable = True, attributeType = 'float', max = 1, min = 0, dv = 1)

        sim_input_grp   = self.create_group(name = self.info_sim_input[0], parent = input)
        collider_grp    = self.create_group(name = self.info_collider[0], parent = sim)
        nRigid_grp      = self.create_group(name = self.info_nRigid[0], parent = collider_grp)
        iCol_grp        = self.create_group(name = self.info_collider_input[0], parent = sim_input_grp)
        nConstraint_grp = self.create_group(name = self.info_nConstraint[0], parent = sim)

        for selection in selection_list:

            name_input_mesh = selection.nodeName()
            if self.suffix_cache_in in name_input_mesh:
                name_input_mesh = name_input_mesh.split('_' + self.suffix_cache_in)[0]

            input_mesh = pm.PyNode(name_input_mesh + '_' + self.suffix_cache_in)

            col_mesh = self.clean_duplicate(selection)
            self.assign_poly_shader(col_mesh, color_name = 'orange')
            col_mesh.rename(name_input_mesh + '_' + self.suffix_col)
            pm.parent(col_mesh, collider_grp)

            nRigid = self.create_nRigid(col_mesh, parent = nRigid_grp)
            pm.reorder(nRigid_grp, back = True)

            iCol_mesh = self.clean_duplicate(selection)
            self.assign_poly_shader(iCol_mesh, color_name = 'orange')
            iCol_mesh.rename('{0}_{1}'.format(name_input_mesh, self.suffix_input_col))
            pm.parent(iCol_mesh, iCol_grp)

            self.quick_blendshape(driver = input_mesh, driven = iCol_mesh)

            self.quick_blendshape(driver = iCol_mesh, driven = col_mesh)

        # nucleus 2/2
        if parent_nucleus_stat:
            nucleus_list = pm.ls(type = 'nucleus')
            pm.parent(nucleus_list, sim)
            pm.reorder(nucleus_list, front = True)

        pm.reorder(nConstraint_grp, back = True)
        pm.reorder(utils_grp, back = True)

    # def init_output_mesh_cache(self):

    #     if not pm.objExists(self.name_mesh_cache_set):

    #         publish = self.create_group(name = self.info_publish[0])

    #         publish_set = self.create_set(name = self.name_publish_set)
    #         mesh_cache_set = self.create_set(name = self.name_mesh_cache_set)
    #         pm.sets(publish_set, edit = True, fe = mesh_cache_set)

    #         # get existing object set to see which one was created during the extract
    #         existing_object_set_list = pm.ls(type = 'objectSet')

    #         # assuming there's only 1 mesh cache in the scene
    #         mesh_cache_proxy = pm.ls(type = 'csMeshProxy')[0]
    #         output_extract  = self.extract_geo_from_mesh_cache(mesh_cache_proxy = mesh_cache_proxy, parent = publish)

    #         pm.sets(mesh_cache_set, edit = True, fe = output_extract)

    #         # deleting the excess object set
    #         new_object_set_list = pm.ls(type = 'objectSet')
    #         for object_set in new_object_set_list:
    #             if object_set not in existing_object_set_list:
    #                 pm.delete(object_set)

    #         # coloring output extract
    #         color_list = self.color_list
    #         shuffle(color_list)
    #         mesh_shape_list = pm.listRelatives(output_extract, ad = True, type = 'mesh')
    #         mesh_list = pm.listRelatives(mesh_shape_list, parent = True)
    #         mesh_list = list(set(mesh_list))

    #         for i in range(0, len(mesh_list)):
    #             mesh = mesh_list[i]
    #             color = color_list[i%len(color_list)]
    #             if self.body_regex.findall(str(mesh)):
    #                 color = self.skin_color
    #             elif self.eye_regex.findall(str(mesh)):
    #                 if not self.eye_exception_regex.findall(str(mesh)):
    #                     color = self.eye_color
    #             self.assign_poly_shader(target_list = mesh, color_name = color)

    def init_nucleus(self):

        input = self.create_group(name = self.info_input[0])
        mesh_shape_list = pm.listRelatives(input, ad = True, type = 'mesh')
        mesh_list = pm.listRelatives(mesh_shape_list, parent = True)
        mesh_list = list(set(mesh_list))
        space_scale = self.get_space_scale(mesh_list)

        nucleus_list = pm.ls(sl = True, type = 'nucleus')
        if not nucleus_list:
            nucleus_list = pm.ls(type = 'nucleus')

        for nucleus in nucleus_list:
            nucleus.spaceScale.set(space_scale)
            nucleus.subSteps.set(10)
            nucleus.maxCollisionIterations.set(15)

            if pm.getAttr(nucleus.startFrame, settable = True):
                expression = 'startFrame = `playbackOptions -q -min`;'
                pm.expression(object = nucleus, string = expression)

    def ssu_create_nCloth(self):

        selection_list = pm.ls(sl = True)

        # nucleus 1/2
        parent_nucleus_stat = None
        nucleus_list = pm.ls(type = 'nucleus')
        if not nucleus_list:
            parent_nucleus_stat = True

        # self.init_output_mesh_cache()
        # duplicate the whole output instead.

        input           = self.create_group(name = self.info_input[0])
        sim             = self.create_group(name = self.info_sim[0])
        sim_input_grp   = self.create_group(name = self.info_sim_input[0], parent = input)
        cloth_grp       = self.create_group(name = self.info_cloth[0], parent = sim)
        nCloth_grp      = self.create_group(name = self.info_nCloth[0], parent = cloth_grp)
        cloth_input_grp = self.create_group(name = self.info_cloth_input[0], parent = sim_input_grp)
        techAnim_lowRes_grp     = self.create_group(name = self.info_techAnim_lowRes[0])
        techAnim_highRes_grp    = self.create_group(name = self.info_techAnim_highRes[0])
        publish_grp             = self.create_group(name = self.info_publish[0])
        OUTPUT_layer    = self.create_display_layer(name = self.info_output_layer[0])

        nConstraint_grp = self.create_group(name = self.info_nConstraint[0], parent = sim)
        utils_grp   = self.create_group(name = self.info_utils[0])
        wrap_grp    = self.create_group(name = self.info_wrap[0])

        cloth_input_wrap_grp        = self.create_group(name = self.info_cloth_input_wrap[0], parent = wrap_grp)
        techAnim_highRes_wrap_grp   = self.create_group(name = self.info_techAnim_highRes_wrap[0], parent = wrap_grp)
        for selection in selection_list:

            cloth_name = selection.nodeName()

            cloth_custom_wrap_grp = None
            for suffix in ['wrap', 'highRes']:
                cloth_custom_wrap_grp_name = cloth_name + '_' + suffix
                if pm.objExists(cloth_custom_wrap_grp_name):
                    cloth_custom_wrap_grp = pm.PyNode(cloth_custom_wrap_grp_name)
                    for tfm in cloth_custom_wrap_grp.listRelatives(type = 'transform'):
                        if tfm.nodeName()[-(len(suffix)):] != suffix:
                            tfm.rename(tfm + '_' + suffix)
                    pm.parent(cloth_custom_wrap_grp, techAnim_highRes_grp)

            input_cloth_mesh = self.clean_duplicate(selection) # for wrap
            input_cloth_mesh.rename(cloth_name + '_' + self.suffix_input_cloth)

            cloth_mesh = selection
            cloth_mesh.rename(cloth_name + '_' + self.suffix_cloth)

            nCloth, nCloth_shape, cloth_shape = self.create_nCloth(cloth_mesh)
            cloth_input_shape, cloth_current_shape = cloth_shape

            pm.select(cloth_mesh)
            pm.mel.eval('displayNClothMesh "input";')
            self.quick_blendshape(driver = input_cloth_mesh, driven = cloth_mesh, name = input_cloth_mesh.nodeName() + '_bsn')
            pm.select(cloth_mesh)
            pm.mel.eval('displayNClothMesh "current";')

            pm.parent(input_cloth_mesh, cloth_input_grp)
            pm.reorder(cloth_input_wrap_grp, back = True)
            pm.parent(cloth_mesh, cloth_grp)
            pm.parent(nCloth, nCloth_grp)
            pm.reorder(nCloth_grp, back = True)

            techAnim_lowRes_mesh = self.clean_duplicate(cloth_mesh) # duplicate cloth_mesh and blendshape for techAnim_lowRes
            techAnim_lowRes_mesh.rename(cloth_name + '_' + self.suffix_techAnim_lowRes)
            techAnim_lowRes_mesh_bsn = self.quick_blendshape(cloth_mesh, techAnim_lowRes_mesh)
            if not pm.isConnected(OUTPUT_layer + '.v', techAnim_lowRes_mesh_bsn.nodeName() + '.en'):
                pm.connectAttr(OUTPUT_layer + '.v', techAnim_lowRes_mesh_bsn.nodeName() + '.en')
            OUTPUT_layer.v > techAnim_lowRes_mesh_bsn.en # connect layer visbility to deformer enable, optimizing
            pm.parent(techAnim_lowRes_mesh, techAnim_lowRes_grp)

            if cloth_custom_wrap_grp: # if you have custom wrap group, with suffix (_wrap, _highRes)
                wrap_list, wrap_base_list = self.create_wrap(driver = techAnim_lowRes_mesh, driven = cloth_custom_wrap_grp)
                for wrap in wrap_list:
                    if not pm.isConnected(OUTPUT_layer + '.v', wrap.nodeName() + '.envelope'):
                        pm.connectAttr(OUTPUT_layer + '.v', wrap.nodeName() + '.envelope')
                pm.parent(wrap_base_list, techAnim_highRes_wrap_grp)

                for suffix in ['wrap', 'highRes']:
                    if cloth_custom_wrap_grp.nodeName()[-(len(suffix)):] == suffix:
                        tfm_list = cloth_custom_wrap_grp.listRelatives(ad = True, type = 'transform')
                        for tfm in tfm_list:
                            publish_mesh_name = tfm.nodeName().split('_' + suffix)[0]
                            if pm.objExists(publish_mesh_name):
                                publish_mesh = pm.PyNode(publish_mesh_name)
                                self.quick_blendshape(tfm, publish_mesh)
                                # if self.SHOW == 'LAK':
                                #     publish_wrap = self.create_group(name = self.info_publish_wrap[0], parent = wrap_grp)
                                #     wrap, wrap_base = self.create_wrap(driver = tfm, driven = publish_mesh)
                                #     pm.parent(wrap_base, publish_wrap)
                                # else:
                                #     self.quick_blendshape(tfm, publish_mesh)
                                publish_mesh.v.disconnect()
                                publish_mesh.v.set(True)

            else: # if you don't have custom wrap group
                publish_mesh = None
                publish_mesh_name = cloth_name
                if pm.objExists(publish_mesh_name):
                    publish_mesh = pm.PyNode(publish_mesh_name)

                highRes_mesh = self.clean_duplicate(publish_mesh)
                highRes_mesh.v.set(True)
                highRes_mesh.rename(cloth_name + self.suffix_techAnim_highRes)
                pm.parent(highRes_mesh, techAnim_highRes_grp)
                wrap_list, wrap_base_list = self.create_wrap(driver = techAnim_lowRes_mesh, driven = highRes_mesh)
                for wrap in wrap_list:
                    if not pm.isConnected(OUTPUT_layer + '.v', wrap.nodeName() + '.envelope'):
                        pm.connectAttr(OUTPUT_layer + '.v', wrap.nodeName() + '.envelope')
                pm.parent(wrap_base_list, techAnim_highRes_wrap_grp)

                if publish_mesh:
                    self.quick_blendshape(highRes_mesh, publish_mesh)
                    publish_mesh.v.disconnect()
                    publish_mesh.v.set(True)

            cache_in_mesh_name = cloth_name + '_' + self.suffix_cache_in # Wrap to the highres from anim_input_extract
            if pm.objExists(cache_in_mesh_name):
                cache_in_mesh = pm.PyNode(cache_in_mesh_name)
                wrap_list, wrap_base_list = self.create_wrap(driver = cache_in_mesh, driven = input_cloth_mesh)
                pm.parent(wrap_base_list, cloth_input_wrap_grp)
                pm.reorder(cloth_input_wrap_grp, back = True)

        color_list = self.color_list
        shuffle(color_list)
        for i in range(0, len(selection_list)):
            mesh = selection_list[i]
            color = color_list[i%len(color_list)]
            self.assign_poly_shader(target_list = mesh, color_name = color)

        # nucleus 2/2
        if parent_nucleus_stat:
            nucleus_list = pm.ls(type = 'nucleus')
            pm.parent(nucleus_list, sim)
            pm.reorder(nucleus_list, front = True)

        pm.reorder(nConstraint_grp, back = True)
        pm.reorder(utils_grp, back = True)

    def ssu_create_follicle_driver(self, target):

        target = pm.PyNode(target)

        fol_driver_name = target.nodeName()
        if self.suffix_col in fol_driver_name:
            fol_driver_name = fol_driver_name.split(self.suffix_col)[0]
        fol_driver_name += self.suffix_folDriver

        if not pm.objExists(fol_driver_name):

            fol_driver = self.clean_duplicate(target)
            fol_driver.rename(fol_driver_name)
            fol_driver_shape = self.get_visible_shape(fol_driver)
            self.create_cfx_hair_uv(fol_driver)
            self.quick_blendshape(target, fol_driver)

            # smooth
            old_smooth_list = pm.listHistory(fol_driver_shape, type = 'polySmoothFace')
            pm.polySmooth(fol_driver)
            new_smooth_list = pm.listHistory(fol_driver_shape, type = 'polySmoothFace')
            for smooth in new_smooth_list:
                if smooth not in old_smooth_list:
                    smooth.rename(fol_driver.nodeName() + '_smooth')

            # unlock normal
            old_unlockNorm_list = pm.listHistory(fol_driver_shape, type = 'polyNormalPerVertex')
            pm.polyNormalPerVertex(fol_driver, unFreezeNormal = True)
            new_unlockNorm_list = pm.listHistory(fol_driver_shape, type = 'polyNormalPerVertex')
            for unlockNorm in new_unlockNorm_list:
                if unlockNorm not in old_unlockNorm_list:
                    unlockNorm.rename(fol_driver.nodeName() + '_unlockNorm')

            # soften edge
            old_polySoftEdge_list = pm.listHistory(fol_driver_shape, type = 'polySoftEdge')
            pm.polySoftEdge(fol_driver, angle = 180, constructionHistory = True)
            new_polySoftEdge_list = pm.listHistory(fol_driver_shape, type = 'polySoftEdge')
            for polySoftEdge in new_polySoftEdge_list:
                if polySoftEdge not in old_polySoftEdge_list:
                    polySoftEdge.rename(fol_driver.nodeName() + '_softEdge')

        else:
            fol_driver = pm.PyNode(fol_driver_name)

        return(fol_driver)

    def ssu_create_nHair(self):

        selection_list = pm.ls(sl = True)
        pm.select(clear = True)

        input           = self.create_group(name = self.info_input[0])
        sim             = self.create_group(name = self.info_sim[0])
        sim_input_grp   = self.create_group(name = self.info_sim_input[0], parent = input)
        nHair_input_grp = self.create_group(name = self.info_nHair_input[0], parent = sim_input_grp)
        publish         = self.create_group(name = self.info_publish[0])
        nConstraint_grp = self.create_group(name = self.info_nConstraint[0], parent = sim)

        xgGroom = self.create_group(name = 'xgGroom', parent = publish)
        if not pm.attributeQuery('XGen_outputHair', node = xgGroom, exists = True):
            xgGroom.addAttr('XGen_outputHair', keyable = True, attributeType = 'bool', dv = 1)

        # nucleus 1/2
        parent_nucleus_stat = None
        nucleus_list = pm.ls(type = 'nucleus')
        if not nucleus_list:
            parent_nucleus_stat = True

        if selection_list:
            if len(selection_list) < 2:
                pass
            else:
                crv_grp_list = selection_list[:-1]
                mesh = selection_list[-1]
                fol_driver = self.ssu_create_follicle_driver(mesh)
                fol_driver_shape = self.get_visible_shape(fol_driver)
                pm.parent(fol_driver, nHair_input_grp)

                for crv_grp in crv_grp_list:
                    # duplicate for input crv group
                    input_crv_grp = self.clean_duplicate(crv_grp)
                    input_crv_grp.rename(input_crv_grp.nodeName().split('_dup')[0] + '_input')
                    tfm_list = []
                    tfm_list.extend(pm.listRelatives(input_crv_grp, ad = True, type = 'transform'))
                    tfm_list = list(set(tfm_list))
                    for tfm in tfm_list:
                        tfm.rename(tfm.nodeName() + '_input')

                    ### When making selected curve dynamic, select mesh shape instead of mesh or sometimes the follicle will be attached to the mesh shape orig
                    ### reconnect follicle to the correct shape will not work
                    hair_system, nRigid, sim_crv_grp = self.make_curves_dynamic([fol_driver_shape, input_crv_grp])

                    # rename follicle in input_crv_grp
                    input_fol_shape_list = pm.listRelatives(input_crv_grp, ad = True, type = 'follicle')
                    input_fol_list = pm.listRelatives(input_fol_shape_list, parent = True)
                    input_fol_list = list(set(input_fol_list))
                    for fol in input_fol_list:
                        crv_shape = pm.listRelatives(fol, ad = True, type = 'nurbsCurve')
                        crv = pm.listRelatives(crv_shape, parent = True)[0]
                        fol.rename(crv.nodeName() + '_fol')

                    # rename sim_crv_grp and its children
                    sim_crv_grp.rename(crv_grp.nodeName() + '_sim')
                        # sim_crv_grp
                    sim_crv_shape_list = pm.listRelatives(sim_crv_grp, ad = True, type = 'nurbsCurve')
                    sim_crv_list = pm.listRelatives(sim_crv_shape_list, parent = True)
                    sim_crv_list = list(set(sim_crv_list))
                        # crv_grp
                    crv_shape_list = pm.listRelatives(crv_grp, ad = True, type = 'nurbsCurve')
                    crv_list = pm.listRelatives(crv_shape_list, parent = True)
                    crv_list = list(set(crv_list))
                        # rename
                    sim_crv_list = self.natural_sort(sim_crv_list)
                    crv_list = self.natural_sort(crv_list)
                    for crv, sim_crv in zip(crv_list, sim_crv_list):
                        sim_crv.rename(crv.nodeName() + '_sim')

                    # rename hair system
                    hair_system.rename(crv_grp.nodeName().split('_')[0] + '_hairSystem')

                    # blendshape sim >> output crv_grp
                    self.quick_blendshape(sim_crv_grp, crv_grp)

                    # organization
                    if nRigid:
                        pm.parent(nRigid, nHair_input_grp)
                    pm.parent(input_crv_grp, nHair_input_grp)
                    pm.parent(sim_crv_grp, sim)
                    pm.reorder(sim_crv_grp, front = True)
                    pm.parent(hair_system, sim)
                    pm.reorder(hair_system, front = True)
                    pm.reorder(nucleus_list, front = True)
                    pm.parent(crv_grp, xgGroom)
                    self.random_curve_color(sim_crv_grp)

                    # root collider exclude collide pair constraint
                    root_cv = self.get_curve_first_cv(input_crv_grp)
                    pm.select(root_cv, mesh)
                    cmd = 'createNConstraint collisionExclusion 0;'
                    nCon = pm.PyNode(pm.mel.eval(cmd)[0])
                    nCon = nCon.getParent()
                    nCon.rename(self.compose_camel_case(crv_grp.nodeName()) + 'Root_' + self.compose_camel_case(mesh.nodeName()) + '_ECP_nCon')
                    pm.parent(nCon, nConstraint_grp)

        # nucleus 2/2
        if parent_nucleus_stat:
            nucleus_list = pm.ls(type = 'nucleus')
            pm.parent(nucleus_list, sim)
            pm.reorder(nucleus_list, front = True)

ssu = SimulationSetup()
gen = general.General()

def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return QtCompat.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class Gui(QtWidgets.QWidget, ui.UI):

    def __init__(self, parent = maya_main_window(), *args, **kwargs):

        super(Gui, self).__init__(parent, *args, **kwargs)

        self._ui            = 'ui_simulation_set_up_util'
        self._width         = 400.00
        self._height        = 10.00
        self._title_name    = 'Simulation Setup Util'
        self._title         = '{title_name} v{version}'.format(title_name = self._title_name, version = __Version__)

        self.delete_UI(self._ui)

        self.setObjectName(self._ui)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True) # destroy this widget when close
        self.resize(self._width, self._height)
        self.setWindowTitle(self._title)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.NonModal)

        self.gui_init()

    def gui_init(self):

        self.main_layout = self.create_QVBoxLayout(parent = self)
        
        ########## BASE RIG ##########

        self.base_rig_label = self.create_QLabel(text = 'Select geometry group(s)', parent = self.main_layout, alignment = QtCore.Qt.AlignLeft, word_wrap = True)
        
        self.base_rig_info_layout = self.create_QGridLayout(w = self._width, nc = 2, cwp = (80, 20), parent = self.main_layout)
        self.base_rig_info_list = self.create_QListWidget(parent = self.base_rig_info_layout, min_h = 10, ams = True, co = (0, 0))

        self.base_rig_info_btn_layout = self.create_QVBoxLayout(parent = self.base_rig_info_layout, co = (0, 1))
        self.base_rig_info_add_btn = self.create_QPushButton(parent = self.base_rig_info_btn_layout, expanding = True, text = 'Add', c = self.base_rig_info_add_btnCmd)
        self.base_rig_info_remove_btn = self.create_QPushButton(parent = self.base_rig_info_btn_layout, expanding = True, text = 'Remove', c = self.base_rig_info_remove_btnCmd)
        self.base_rig_info_clear_btn = self.create_QPushButton(parent = self.base_rig_info_btn_layout, expanding = True, text = 'Clear', c = self.base_rig_info_clear_btnCmd)

        self.base_rig_create_btn = self.create_QPushButton(text = 'Create base rig', parent = self.main_layout, c = self.base_rig_create_btnCmd)

        self.create_separator(parent = self.main_layout)

        ########## REFERENCE ##########

        text = 'Select 2 edges on the geometry from cfx|INPUT|input_anim that you want motion_mult, t_pose to reference to'
        self.reference_label = self.create_QLabel(text = text, parent = self.main_layout, alignment = QtCore.Qt.AlignLeft, word_wrap = True)

        self.create_QLabel(text = ' ', parent = self.main_layout, alignment = QtCore.Qt.AlignLeft, word_wrap = True)

        self.reference_lineEdit_layout = self.create_QGridLayout(w = self._width, nc = 3, cwp = (60, 20, 20), parent = self.main_layout)

        self.reference_tfm_label = self.create_QLabel(text = 'Transform', parent = self.reference_lineEdit_layout, alignment = QtCore.Qt.AlignCenter, word_wrap = True, co = (0, 0))
        self.reference_edge1_label = self.create_QLabel(text = 'Edge 1', parent = self.reference_lineEdit_layout, alignment = QtCore.Qt.AlignCenter, word_wrap = True, co = (0, 1))
        self.reference_edge2_label = self.create_QLabel(text = 'Edge 2', parent = self.reference_lineEdit_layout, alignment = QtCore.Qt.AlignCenter, word_wrap = True, co = (0, 2))

        self.reference_tfm_lineEdit = self.create_QLineEdit(read_only = True, parent = self.reference_lineEdit_layout, co = (1, 0))
        self.reference_edge1_lineEdit = self.create_QLineEdit(read_only = True, parent = self.reference_lineEdit_layout, co = (1, 1))
        self.reference_edge2_lineEdit = self.create_QLineEdit(read_only = True, parent = self.reference_lineEdit_layout, co = (1, 2))

        self.reference_getInfo_btn_layout = self.create_QGridLayout(w = self._width, nc = 2, cwp = (60, 40), parent = self.main_layout)
        self.reference_getInfo_btn = self.create_QPushButton(parent = self.reference_getInfo_btn_layout, text = 'Get edges', c = self.reference_getInfo_btnCmd, co = (0, 1))

        self.reference_create_btn = self.create_QPushButton(parent = self.main_layout, text = 'Create reference loc', c = self.reference_create_btnCmd)

        self.create_separator(parent = self.main_layout)

        ########## SAVE / LOAD ##########

        self.save_load_layout = self.create_QGridLayout(w = self._width, nc = 3, parent = self.main_layout)
        self.save_btn = self.create_QPushButton(text = 'Save', parent = self.save_load_layout, co = (0, 0))
        self.load_btn = self.create_QPushButton(text = 'Load', parent = self.save_load_layout, co = (0, 1))
        self.clear_btn = self.create_QPushButton(text = 'Clear', parent = self.save_load_layout, co = (0, 2))

        self.main_layout.setAlignment(QtCore.Qt.AlignTop)

        # self.create_separator(parent = self.main_layout)

        # self.create_ref_loc_btn = self.create_QPushButton(text = 'Create Ref Loc', parent = self.main_layout)

        # self.attach_ref_loc_label = self.create_QLabel(
        #     text = 'Select input:geometry that you want to attach ref loc to',
        #     parent = self.main_layout, alignment = QtCore.Qt.AlignLeft, word_wrap = True)
        # self.attach_ref_loc_btn = self.create_QPushButton(text = 'Attach Ref Loc', parent = self.main_layout)

        # self.nDynamic_label = self.create_QLabel(text = 'nDynamic', parent = self.main_layout, alignment = QtCore.Qt.AlignCenter)
        # font = self.nDynamic_label.font()
        # font.setPointSize(15)
        # font.setBold(True)
        # self.nDynamic_label.setFont(font)

        # self.create_separator(parent = self.main_layout)
        # self.nDynamic_label = self.create_QLabel(text = 'Passive Collider', parent = self.main_layout, alignment = QtCore.Qt.AlignCenter)
        # font = self.nDynamic_label.font()
        # font.setPointSize(10)
        # font.setBold(True)
        # self.nDynamic_label.setFont(font)

        # self.create_nRigid_label = self.create_QLabel(text = 'Select mesh(es) from "anim_input_extract" or "publish" group.', parent = self.main_layout, alignment = QtCore.Qt.AlignLeft)
        # self.create_nRigid_btn = self.create_QPushButton(text = 'Create Passive Collider', parent = self.main_layout, c = self.create_nRigid_btnCmd)

        # self.create_separator(parent = self.main_layout)
        # self.nDynamic_label = self.create_QLabel(text = 'nCloth', parent = self.main_layout, alignment = QtCore.Qt.AlignCenter)
        # font = self.nDynamic_label.font()
        # font.setPointSize(10)
        # font.setBold(True)
        # self.nDynamic_label.setFont(font)

        # self.create_QLabel(text = 'skirt_geo            ', parent = self.main_layout, alignment = QtCore.Qt.AlignLeft)
        # self.create_QLabel(text = 'skirt_geo_highRes', parent = self.main_layout, alignment = QtCore.Qt.AlignLeft)
        # self.create_QLabel(text = '    L skirt_geo', parent = self.main_layout, alignment = QtCore.Qt.AlignLeft)
        # self.create_QLabel(text = '    L skirt_button_geo', parent = self.main_layout, alignment = QtCore.Qt.AlignLeft)
        # self.create_nCloth_btn = self.create_QPushButton(text = 'Create nCloth', parent = self.main_layout, c = self.create_nCloth_btnCmd)

        # self.create_separator(parent = self.main_layout)
        # self.nDynamic_label = self.create_QLabel(text = 'nHair', parent = self.main_layout, alignment = QtCore.Qt.AlignCenter)
        # font = self.nDynamic_label.font()
        # font.setPointSize(10)
        # font.setBold(True)
        # self.nDynamic_label.setFont(font)

        # self.create_QLabel(text = 'Select XGen Description(s)', parent = self.main_layout)
        # self.create_curve_from_guide_btn = self.create_QPushButton(text = 'Create Curve from Guide (XGen)', parent = self.main_layout, c = self.create_curve_from_guide_btnCmd)

        # self.create_QLabel(text = 'Select curve group(s), then collider', parent = self.main_layout)
        # self.create_nHair_btn = self.create_QPushButton(text = 'Create nHair', parent = self.main_layout, c = self.create_nHair_btnCmd)

        # self.create_separator(parent = self.main_layout)
        # self.nDynamic_label = self.create_QLabel(text = 'Nucleus', parent = self.main_layout, alignment = QtCore.Qt.AlignCenter)
        # font = self.nDynamic_label.font()
        # font.setPointSize(10)
        # font.setBold(True)
        # self.nDynamic_label.setFont(font)

        # self.set_nucleus_label = self.create_QLabel(text = "Select nucleus/nuclei (or it will set every nucleus in the scene).", parent = self.main_layout, alignment = QtCore.Qt.AlignLeft)
        # self.set_nucleus_btn = self.create_QPushButton(text = 'Set Nucleus', parent = self.main_layout, c = self.set_nucleus_btnCmd)

        # nConstraint

        

    ####################################################################################
    ####################################################################################
    ####################################################################################

    ########## BASE RIG FUNCTION ##########

    def base_rig_info_add_btnCmd(self):
        selection_list = pm.ls(sl = True)
        selection_list.sort()

        item_list = self.get_QListWidget_items(self.base_rig_info_list)
        for selection in selection_list:
            if selection.fullPath() not in item_list:
                self.base_rig_info_list.addItem(selection.fullPath())

        self.base_rig_info_list.sortItems()

    def base_rig_info_remove_btnCmd(self):

        selection_list = self.get_QListWidget_selectedItem(self.base_rig_info_list, raw = True)
        for selection in selection_list:
            (self.base_rig_info_list.takeItem(self.base_rig_info_list.row(selection)))

    def base_rig_info_clear_btnCmd(self):
        self.base_rig_info_list.clear()

    def base_rig_create_btnCmd(self):
        pm.undoInfo(openChunk = True)
        geo_grp_list = pm.ls(sl = True)
        ssu.init_hierarchy()
        ssu.init_geo_grp(geo_grp_list = self.get_QListWidget_items(self.base_rig_info_list))  
        pm.undoInfo(closeChunk = True)

    ####################################################################################
    ####################################################################################
    ####################################################################################

    def reference_getInfo_btnCmd(self):
        pm.undoInfo(openChunk = True)
        # get edge
        raw_edge_list = pm.filterExpand(sm = 32)
        edge_list = []
        if raw_edge_list:
            for edge in raw_edge_list:
                edge_list.append(edge.split('.')[-1])
            self.reference_edge1_lineEdit.setText(edge_list[0])
            self.reference_edge2_lineEdit.setText(edge_list[1])
        else:
            pm.error('Please select 2 edges before proceeding')
        # get object
        object_shape = pm.ls(sl = True, o = True)[0]
        object = pm.listRelatives(object_shape, parent = True)[0]
        self.reference_tfm_lineEdit.setText(object.fullPath())
        pm.undoInfo(closeChunk = True)

    def reference_create_btnCmd(self):
        pm.undoInfo(openChunk = True)

        # initiate
        utils_grp = gen.create_group(name = ssu.info_utils[0])
        # get info from the gui
        object = self.reference_tfm_lineEdit.text()
        object = pm.PyNode(object)
        edge1 = self.reference_edge1_lineEdit.text()
        edge2 = self.reference_edge2_lineEdit.text()
        edge1 = pm.PyNode('{0}.{1}'.format(object.fullPath(), edge1))
        edge2 = pm.PyNode('{0}.{1}'.format(object.fullPath(), edge2))
        # get ref pos
        pm.select(edge1, edge2)
        cluster = pm.cluster()
        ref_pos = pm.xform(cluster, q = True, ws = True, rp = True)
        pm.delete(cluster)
        # create ref_loc        
        obj_ref = pm.duplicate(object)[0]
        obj_ref.rename('{0}_ref'.format(object.nodeName()))
        gen.unlock_normal(target = obj_ref)
        gen.poly_soft_edge(target = obj_ref)
        gen.quick_blendshape(object, obj_ref, name = 'BSH_src_{0}'.format(object.stripNamespace()))
        ref_fol = gen.attach_fol_mesh(ssu.name_ref_fol, obj_ref, ref_pos)
        ref_loc = gen.create_locator(name = ssu.name_ref_loc)
        point_con = pm.pointConstraint(ref_fol, ref_loc, mo = False, skip = 'none')
        pm.delete(point_con)
        par_con = pm.parentConstraint(ref_fol, ref_loc, mo = True, skipRotate = 'none', skipTranslate = 'none')
        # organize
        ref_grp = gen.create_group(ssu.info_ref[0])
        ref_grp.v.set(0)
        pm.parent(ref_loc, ref_grp, utils_grp)
        pm.parent(obj_ref, ref_fol, ref_grp)
        gen.lock_hide_attr(target = ref_grp)
        gen.lock_hide_attr(target = ref_loc, attr_list = ['s'])
        # connect ref >> motion mult
        solver_mm_ref = gen.create_locator(name = ssu.name_solver_mm_ref)
        ref_loc.t >> solver_mm_ref.t
        ref_loc.r >> solver_mm_ref.r
        pm.undoInfo(closeChunk = True)        

    ####################################################################################
    ####################################################################################
    ####################################################################################

    def create_nRigid_btnCmd(self):
        pm.undoInfo(openChunk = True)
        ssu.ssu_create_nRigid()
        pm.undoInfo(closeChunk = True)

    def create_nCloth_btnCmd(self):
        pm.undoInfo(openChunk = True)
        # ssu.ssu_create_nCloth()
        pm.undoInfo(closeChunk = True)

    ####################################################################################
    ####################################################################################
    ####################################################################################

    def create_curve_from_guide_btnCmd(self):
        pm.undoInfo(openChunk = True)
        # ssu.guide_to_curve()
        pm.undoInfo(closeChunk = True)

    def create_nHair_btnCmd(self):
        pm.undoInfo(openChunk = True)
        # ssu.ssu_create_nHair()
        pm.undoInfo(closeChunk = True)

    def set_nucleus_btnCmd(self):
        pm.undoInfo(openChunk = True)
        # ssu.init_nucleus()
        pm.undoInfo(closeChunk = True)

def run():
    gui = Gui()
    gui.show()
