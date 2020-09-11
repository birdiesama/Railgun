################################################################################
__Script__	= 'curve_blendshape_cv.general'
__Author__  = 'Weerapot Chaoman'
__Date__    = 20200910
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
################################################################################
import re, random
from random import shuffle
import pymel.core as pm
import maya.cmds as mc
################################################################################

class CleanUp(object):
    def __init__(self):
        super(CleanUp, self).__init__()

    def delete_non_visible_shape(self, target):
        target = pm.PyNode(target)
        target_shape_list = target.getShapes()
        for target_shape in target_shape_list:
            if target_shape.isIntermediate():
                pm.delete(target_shape)
        target_shape = target.getShape()
        target_shape.rename(target.nodeName() + 'Shape')

    def freeze_transform(self, target):
        target = pm.PyNode(target)
        pm.makeIdentity(target, apply = True)

    def delete_history(self, target):
        target = pm.PyNode(target)
        pm.delete(target, ch = True)

    def center_pivot(self, target):
        target = pm.PyNode(target)
        pm.xform(target, cp = True)

    def list_connections(self, target, type):
        # list connections of the transform + it's shapes for specified connection type
        connection_list = []
        target = pm.PyNode(target)
        target_shape_list = target.getShapes()
        connection_list.extend(target.listConnections(type = type))
        for target_shape in target_shape_list:
            connection_list.extend(target_shape.listConnections(type = type))
        return connection_list

    def get_visible_shape(self, mesh):
        mesh = pm.PyNode(mesh)
        try:
            mesh_shape = mesh.getShape()
            if mesh_shape.isIntermediate():  # It's not the shape we see? Lets run through every shape and see
                mesh_shape_list = mesh.getShapes()
                for mesh_shape_prx in mesh_shape_list:
                    if not mesh_shape_prx.isIntermediate():
                        mesh_shape = mesh_shape_prx
            return mesh_shape
        except:
            return None

    ##################
    ''' sets '''
    ##################
    def remove_from_set(self, object_set_list, object_list):
        target_list = []
        for object in object_list:
            target_list.append(object)
            try:
                target_list.extend(object.getShapes())
            except:
                pass
        for object_set in object_set_list:
            pm.sets(object_set, rm = target_list)

    def remove_from_all_set(self, target):
        target = pm.PyNode(target)
        target_shape_list = target.getShapes()

        target_list = [target]
        target_list.extend(target_shape_list)

        set_list = []
        set_list.extend(target.listConnections(type = 'objectSet'))

        for target_shape in target_shape_list:
            set_list.extend(target_shape.listConnections(type = 'objectSet'))
        set_list = list(set(set_list))

        for set_name in set_list:
            pm.sets(set_name, rm = target_list)

    def add_to_set(self, list_object, list_object_set):

        list_target = []

        for object in list_object:
            list_target.append(object)
            # if self.get_visible_shape(object):
            #     list_target.append(self.get_visible_shape(object))

        for set_name in list_object_set:
            pm.sets(set_name, add=list_target)

    ##################
    ''' layer '''
    ##################
    def remove_from_all_layer(self, target):
        target = pm.PyNode(target)
        target_list = []
        target_list.append(target)
        target_list.append(target.getShapes())
        for item in target_list:
            pm.editDisplayLayerMembers('defaultLayer', item)

    ##################
    ''' unlock normal '''
    ##################

    def unlock_normal(self, target, prefix=True, suffix=False):

        if suffix:
            prefix = False

        if prefix:
            prefix = 'unlockNorm_'
            suffix = ''
        elif suffix:
            prefix = ''
            suffix = '_unlockNorm'

        target_list = target
        if not isinstance(target_list, list):
            target_list = [target_list]

        for target in target_list:
            target = pm.PyNode(target)
            target_shape = self.get_visible_shape(target)
            old_unlockNorm_list = pm.listHistory(target_shape, type = 'polyNormalPerVertex')
            pm.polyNormalPerVertex(target, unFreezeNormal = True)
            new_unlockNorm_list = pm.listHistory(target_shape, type = 'polyNormalPerVertex')
            for unlockNorm in new_unlockNorm_list:
                if unlockNorm not in old_unlockNorm_list:
                    unlockNorm.rename(prefix + target.stripNamespace() + suffix)

    def poly_soft_edge(self, target, prefix=True, suffix=False):

        if suffix:
            prefix = False

        if prefix:
            prefix = 'unlockNorm_'
            suffix = ''
        elif suffix:
            prefix = ''
            suffix = '_unlockNorm'

        target_list = target
        if not isinstance(target_list, list):
            target_list = [target_list]

        for target in target_list:
            target = pm.PyNode(target)
            target_shape = self.get_visible_shape(target)
            old_polySoftEdge_list = pm.listHistory(target_shape, type = 'polySoftEdge')
            pm.polySoftEdge(target, angle = 180, constructionHistory = True)
            new_polySoftEdge_list = pm.listHistory(target_shape, type = 'polySoftEdge')
            for polySoftEdge in new_polySoftEdge_list:
                if polySoftEdge not in old_polySoftEdge_list:
                    polySoftEdge.rename(prefix + target.stripNamespace() + suffix)

    def rename_tweak(self):
        tweak_list = pm.ls(type = 'tweak')

        type_list = ['mesh', 'nurbsCurve']

        for tweak in tweak_list:
            tfm_list = []
            for type in type_list:
                tfm_list.extend(tweak.listConnections(type = type))
            try:
                tfm = tfm_list[0]
                tweak.rename(tfm.nodeName() + '_tweak')
            except:
                print('... Cannot rename ' + tweak.nodeName())
    ##################
    ''' reorder  children '''
    ##################
    def reorder_children(self ,target):
        target = pm.PyNode(target)
        children_list = target.getChildren()
        children_list = self.natural_sort(children_list)
        for children in children_list[::-1]:
            pm.reorder(children, front = True)

    ##################
    ''' clean duplicate '''
    ##################

    def clean_duplicate(self, target, suffix='dup'):
        target = pm.PyNode(target)
        dup_target = pm.duplicate(target)[0]
        dup_target.rename(target.stripNamespace() + '_' + suffix)
        pm.parent(dup_target, world = True)
        self.lock_hide_attr(dup_target, en = False)
        self.freeze_transform(dup_target)
        self.center_pivot(dup_target)
        self.delete_history(dup_target)
        self.remove_from_all_set(dup_target)
        self.remove_from_all_layer(dup_target)
        if target.getShapes():
            self.delete_non_visible_shape(dup_target)
            if target.getShape().nodeType() == 'mesh':
                pm.sets('initialShadingGroup', forceElement=dup_target)
        return(dup_target)

    def quick_duplicate(self, target, namespace=None, suffix=None, parent=None, lockHide=False, color_list=None, re_list=None):
        target = pm.PyNode(target)
        dup_target = pm.duplicate(target)[0]
        # rename top node
        if namespace:
            dup_target.rename('{0}:{1}'.format(namespace, target.nodeName()))
            if suffix:
                dup_target.rename('{0}_{1}'.format(dup_target.nodeName(), suffix))
        elif suffix:
            dup_target.rename('{0}_{1}'.format(target.nodeName(), suffix))
        # rename tfm under top node (if any)
        tfm_list = dup_target.listRelatives(ad = True, type = 'transform')
        if tfm_list:
            tfm_list = list(set(tfm_list))            
            for tfm in tfm_list:
                if namespace:
                    tfm.rename('{0}:{1}'.format(namespace, tfm.nodeName()))
                    if suffix:
                        tfm.rename('{0}_{1}'.format(tfm.nodeName(), suffix))
                elif suffix:
                    tfm.rename('{0}_{1}'.format(tfm.nodeName(), suffix))
        # parent
        if parent:
            pm.parent(dup_target, parent)
        # lockHide
        if lockHide:
            self.lock_hide_attr(dup_target)
        # color
        if color_list:

            shuffle(color_list)
            mesh_shape_list = pm.listRelatives(dup_target, ad = True, type = 'mesh')
            mesh_list = pm.listRelatives(mesh_shape_list, parent = True)
            mesh_list = list(set(mesh_list))

            for i in range(0, len(mesh_list)):
                mesh = mesh_list[i]
                color = color_list[i%len(color_list)]
                
                if re_list:
                    for re_data in re_list:
                        re = re_data[0]
                        re_color = re_data[1]
                        re_exception = re_data[2]
                        if re.findall(mesh.nodeName()):
                            if re_exception:
                                if not re_exception.findall(mesh.nodeName()):
                                    color = re_color
                            else:
                                color = re_color

                # if self.body_regex.findall(str(mesh)):
                #     if geo_grp != input_anim:
                #         color = self.skin_color
                #     else:
                #         pass
                # elif self.eye_regex.findall(mesh.nodeName()):
                #     if not self.eye_exception_regex.findall(mesh.nodeName()):
                #         color = self.eye_color
                

                self.assign_poly_shader(target_list = mesh, color_name = color)

        # return top node
        return(dup_target)

class Curve(object):

    def __init__(self, *args, **kwargs):
        super(Curve, self).__init__(*args, **kwargs)

    def get_curve_cv(self, target):
        target = pm.PyNode(target)
        target_shape = self.get_visible_shape(target) # general.clean_up
        spans = target_shape.spans.get()
        degree = target_shape.getAttr('degree')
        cv = spans + degree
        return cv

    def get_curve_first_cv_1(self, target_list): # obsolete
        target_list = self.is_list(target_list) # general.misc
        to_select_list = []
        for target in target_list:
            to_select_list.append(target.cv[0])
        return to_select_list

    def get_curve_last_cv_1(self, target_list): # obsolete
        target_list = self.is_list(target_list) # general.misc
        to_select_list =[]
        for target in target_list:
            last_cv = self.get_curve_cv(target) - 1
            to_select_list.append(target.cv[last_cv])
        return to_select_list

    def get_curve_first_cv(self, target):
        crv_shape_list = pm.listRelatives(target, ad = True, type = 'nurbsCurve')
        crv_list = pm.listRelatives(crv_shape_list, parent = True)
        crv_list = list(set(crv_list))
        return_list = []
        for crv in crv_list:
            return_list.append(crv.cv[0])
        return return_list

    def get_curve_last_cv(self, target):
        crv_shape_list = pm.listRelatives(target, ad = True, type = 'nurbsCurve')
        crv_list = pm.listRelatives(crv_shape_list, parent = True)
        crv_list = list(set(crv_list))
        return_list = []
        for crv in crv_list:
            last_cv = self.get_curve_cv(crv) -1
            return_list.append(crv.cv[last_cv])
        return return_list

    def attach_curve_to_polygon(self):
        selection_list = pm.ls(sl = True)
        curve_grp_list = selection_list[:-1]
        mesh = selection_list[-1]

        if not isinstance(curve_grp_list, list):
            curve_grp_list = [curve_grp_list]

        for curve_grp in curve_grp_list:
            curve_list = pm.listRelatives(curve_grp, ad = True, type = 'nurbsCurve')
            curve_tfm_list = pm.listRelatives(curve_list, parent = True)
            curve_tfm_list = list(set(curve_tfm_list))

            for curve in curve_tfm_list:
                pm.select(curve.nodeName() + '.cv[0]')
                cluster = pm.cluster()
                cluster_pos = pm.xform(cluster, q = True, ws = True, rp = True)
                pm.delete(cluster)
                # uv = self.closest_point_on_mesh(pos = cluster_pos, mesh = mesh)
                fol = self.attach_fol_mesh(name = curve.nodeName() + '_fol', mesh = mesh, pos = cluster_pos)
                pm.parent(curve, fol)
                pm.parent(fol, curve_grp)

    def set_curve_shape_color(self, target_list, rgb=(0, 0, 0)):
        target_list = self.is_list(target_list) # general.misc
        for target in target_list:
            target = pm.PyNode(target)
            target_shape = self.get_visible_shape(target) # general.cleanup
            if rgb:
                r, g, b = rgb
                target_shape.overrideRGBColors.set(True)
                target_shape.overrideEnabled.set(True)
                target_shape.overrideColorRGB.set(r, g, b)
            else:
                target_shape.overrideEnabled.set(False)

    def random_curve_color_1(self, target_list, enable=True): # obsolete

        system_random = random.SystemRandom()
        random_color_list = []
        random_color_list.append('white')
        random_color_list.append('light_yellow')
        random_color_list.append('light_blue')
        random_color_list.append('light_pink')
        random_color_list.append('light_brown')
        random_color_list.append('light_green')
        random_color_list.append('light_purple')

        target_list = self.is_list(target_list) # general.misc

        if enable:
            for target in target_list:
                self.set_curve_shape_color(target, rgb = self.color_rgb_dict[str(system_random.choice(random_color_list))])
        else:
            self.set_curve_shape_color(target_list, rgb = None)

    def random_curve_color(self, target, enable=True):
        system_random = random.SystemRandom()
        random_color_list = []
        random_color_list.append('white')
        random_color_list.append('light_yellow')
        random_color_list.append('light_blue')
        random_color_list.append('light_pink')
        random_color_list.append('light_brown')
        random_color_list.append('light_green')
        random_color_list.append('light_purple')

        crv_shape_list = pm.listRelatives(target, ad = True, type = 'nurbsCurve')
        crv_list = pm.listRelatives(crv_shape_list, parent = True)
        crv_list = list(set(crv_list))

        if enable:
            for crv in crv_list:
                self.set_curve_shape_color(crv, rgb = self.color_rgb_dict[str(system_random.choice(random_color_list))])
        else:
            self.set_curve_shape_color(crv_list, rgb = None)

    def cv_blendshape(self, driver, driven, lower_val, upper_val, direction):

        driver = pm.PyNode(driver)
        driven = pm.PyNode(driven)

        driver_cv = self.get_curve_cv(driver)
        driven_cv = self.get_curve_cv(driven)

        if driver_cv != driven_cv:
            pm.warning('... {0} and {1} cv is not matching, no operation was initiated'.format(driver, driven))

        else:
            cv = driver_cv

            blendshape_name = driver.stripNamespace() + '_cv_bsn'
            if not pm.objExists(blendshape_name):
                blendshape = self.quick_blendshape(driver, driven, name = blendshape_name) # general.blendshape
            else:
                blendshape = pm.PyNode(blendshape_name)

            cv_start = int(cv / 100.00 * lower_val)
            cv_end = int(cv / 100.00 * upper_val)

            print cv_start
            print cv_end

            if cv_start <= 1:
                cv_start += 1
            elif cv_start > cv:
                cv_start -= 1

            if cv_end <= 1:
                cv_end += 1
            elif cv_end > cv:
                cv_end -= 1

            if cv_start == cv_end:
                if cv_start >= 2:
                    cv_start -= 1
                else:
                    if cv_end <= cv - 1:
                        cv_end += 1

            blend_val = 1 / float(((cv_start - cv_end) ** 2) ** 0.5)

            if direction == 1:

                # set weight on all cv to 0
                for i in range(0, cv):
                    pm.setAttr(blendshape.nodeName() + '.inputTarget[0].inputTargetGroup[0].targetWeights[{i}]'.format(i = i), 0)

                val = 0.0
                for i in range(cv_start, cv_end):
                    pm.setAttr(blendshape.nodeName() + '.inputTarget[0].inputTargetGroup[0].targetWeights[{i}]'.format(i = i), val)
                    val += blend_val

                for i in range(cv_end, cv):
                    pm.setAttr(blendshape.nodeName() + '.inputTarget[0].inputTargetGroup[0].targetWeights[{i}]'.format(i = i), 1)

            elif direction == -1:

                # set weight on all cv to 1
                for i in range(0, cv):
                    pm.setAttr(blendshape.nodeName() + '.inputTarget[0].inputTargetGroup[0].targetWeights[{i}]'.format(i = i), 1)

                val = 0.0
                for i in range(cv_start, cv_end):
                    pm.setAttr(blendshape.nodeName() + '.inputTarget[0].inputTargetGroup[0].targetWeights[{i}]'.format(i = i), val)
                    val += blend_val

                for i in range(cv_end, cv):
                    pm.setAttr(blendshape.nodeName() + '.inputTarget[0].inputTargetGroup[0].targetWeights[{i}]'.format(i = i), 0)

            elif direction == 0:
                # set weight on all cv to 1
                for i in range(0, cv):
                    pm.setAttr(blendshape.nodeName() + '.inputTarget[0].inputTargetGroup[0].targetWeights[{i}]'.format(i = i), 1)

        return blendshape

    def reorder_crv_list_closest_root(self, crv_list_A, crv_list_B):

        for crv in crv_list_A:
            crv_shape = self.get_visible_shape(crv)
            # need to create cluster first, then xform
            pm.select(crv_shape.cv[0])
            cluster = pm.cluster()
            crv_root_pos = pm.xform(cluster, q = True, ws = True, rp = True)
            pm.delete(cluster)

    def rebuild_curve(self, target, degree, cv, replace=False):

        target = pm.PyNode(target)
        spans = cv - degree

        rebuild = pm.rebuildCurve(
            target,
            ch = 1,
            replaceOriginal     = replace,
            rebuildType = 0,
            endKnots    = 1,
            keepRange   = 1,
            keepControlPoints   = 0,
            keepEndPoints       = 1,
            keepTangents        = 1,
            spans       = spans,
            degree      = degree,
            tolerance   = 0.01,
            )

        return(rebuild[0])

    def get_closest_crv_pair_list(self, driver_tfm, driven_tfm):

        driver_crv_list = list(set(pm.listRelatives(pm.listRelatives(driver_tfm, ad = True, type = 'nurbsCurve'), parent = True)))
        driven_crv_list = list(set(pm.listRelatives(pm.listRelatives(driven_tfm, ad = True, type = 'nurbsCurve'), parent = True)))

        driver_pos_info = []

        for driver in driver_crv_list:
            pos = pm.pointOnCurve(driver, pr = 0)
            driver_pos_info.append([pos, driver])

        print driver_pos_info

        pair_list = []
        for driven in driven_crv_list:
            pos = pm.pointOnCurve(driven, pr = 0)
            proximity_list = []
            for driver_pos in driver_pos_info:
                distance = self.get_distance(pos, driver_pos[0])
                proximity_list.append([distance, driver_pos[1]])
            proximity_list.sort()
            pair_list.append([proximity_list[0][1], driven])

        return pair_list

class Misc(object):

    def __init__(self, *args, **kwargs):
        super(Misc, self).__init__(*args, **kwargs)

    def is_list(self, target_list):
        if not isinstance(target_list, list):
            target_list = [target_list]
        return target_list

    def get_distance(self, point1, point2):
        distance = ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2) ** 0.5
        return distance

class NaturalSort(object):
    def __init__(self, *args, **kwargs):
        super(NaturalSort, self).__init__(*args, **kwargs)

    def convert_key_elem(self, input):
        if input.isdigit(): return int(input)
        else: return input.lower()

    def split_key(self, key):
        return_list = []
        key = str(key)
        for elem in re.split('([0-9]+)', key):
            return_list.append(self.convert_key_elem(elem))
        return return_list

    def natural_sort(self, list):
        return sorted(list, key = self.split_key)

class Utils(object):

    def __init__(self):
        super(Utils, self).__init__()

    ######### BLENDSHAPE #########

    def quick_blendshape(self, driver, driven, name=None, prefix=False, suffix=True):

        if prefix:
            suffix = False

        driver = pm.PyNode(driver)
        driven = pm.PyNode(driven)
        # driven_shape = driven.getShape()

        target_shape_list = []
        type_list = ['mesh', 'nurbsCurve']
        for type in type_list:
            shape_list = driven.listRelatives(ad=True, type=type)
            target_shape_list.extend(shape_list)
        target_shape_list = list(set(target_shape_list))
        for target_shape in target_shape_list:
            if target_shape.isIntermediate():
                target_shape_list.remove(target_shape)

        # tweak node
        old_tweak_list = []
        if target_shape_list:
            for target_shape in target_shape_list:
                tweak_list = target_shape.listConnections(type='tweak')
                tweak_list = list(set(tweak_list))
                old_tweak_list.extend(tweak_list)

        # blend shape history
        blendshape_history_list = []

        for target_shape in target_shape_list:
            blendshape_history = target_shape.listHistory(type='blendShape', lv=1)
            if blendshape_history:
                blendshape_history_list.append([target_shape, blendshape_history[0]])

        blendshape = pm.blendShape(driver, driven, origin='world', automatic=True, weight=[0, 1], envelope=1)[0]

        # tweak node
        new_tweak_list = []
        if target_shape_list:
            for target_shape in target_shape_list:
                tweak_list = target_shape.listConnections(type='tweak')
                tweak_list = list(set(tweak_list))
                new_tweak_list.extend(tweak_list)
            if new_tweak_list:
                for new_tweak in new_tweak_list:
                    if new_tweak not in old_tweak_list:
                        pm.delete(new_tweak)

        # blend shape history
        if blendshape_history_list:
            for blendshape_history in blendshape_history_list:
                pm.reorderDeformers(blendshape, blendshape_history[1], blendshape_history[0])

        if name:
            blendshape.rename(name)
        else:
            name = self.compose_camel_case(driver.nodeName())
            if suffix:
                blendshape.rename(name + '_src_bsn')
            if prefix:
                blendshape.rename('BSH_src_{0}'.format(name))

        return blendshape

    def get_blendshape_member(self, blendshape_list, type = None):
        if not isinstance(blendshape_list, list):
            blendshape_list = [blendshape_list]
        return_list = []
        for blendshape in blendshape_list:
            blendshape = pm.PyNode(blendshape)
            set = blendshape.listConnections(type = 'objectSet')
            set_member_list = pm.sets(set, q = True)
            if type:
                set_member_list = pm.ls(set_member_list, o = True, type = type)
            else:
                set_member_list = pm.ls(set_member_list, o = True)
            return_list.extend(set_member_list)
        return return_list

    def blendshape_get_weight(self, mesh_shape, blendshape):
        mesh_shape = pm.PyNode(mesh_shape)
        blendshape = pm.PyNode(blendshape)
        vertex_no = pm.polyEvaluate(mesh_shape, vertex = True)
        # bsn_base_weight = list(blendshape.inputTarget[0].baseWeights.get())
        bsn_base_weight = mc.getAttr('{0}.inputTarget[0].baseWeights[0:{1}]'.format(blendshape, vertex_no))
        # bsn_iTarget_weight = list(blendshape.inputTarget[0].inputTargetGroup[0].targetWeights.get())
        bsn_iTarget_weight = mc.getAttr('{0}.inputTarget[0].inputTargetGroup[0].targetWeights[0:{1}]'.format(blendshape, vertex_no))
        return(bsn_base_weight, bsn_iTarget_weight, vertex_no)

    def blendshape_set_weight(self, mesh_shape, blendshape, bsn_base_weight, bsn_iTarget_weight, src_vertex_no):
        mesh_shape = pm.PyNode(mesh_shape)
        blendshape = pm.PyNode(blendshape)
        vertex_no = pm.polyEvaluate(mesh_shape, vertex = True)
        if src_vertex_no != vertex_no:
            pm.warning('... Source total vertices and target total vertices not match, you might get unexpected result')
        if bsn_base_weight:
            pm.setAttr('{0}.inputTarget[0].baseWeights[0:{1}]'.format(blendshape, vertex_no), *bsn_base_weight, size = len(bsn_base_weight))
        if bsn_iTarget_weight:
            pm.setAttr('{0}.inputTarget[0].inputTargetGroup[0].targetWeights[0:{1}]'.format(blendshape, vertex_no, *bsn_iTarget_weight, size = len(bsn_iTarget_weight)))

    ######### Contraint #########

    def quick_par_con(self, driver, driven, mo=False, name=None):
        par_con = pm.parentConstraint(driver, driven, mo = mo, skipRotate = 'none', skipTranslate = 'none')
        if name:
            par_con.rename(name)
        else:
            par_con.rename(driven.stripNamespace() + '_parCon')
        return par_con

    def quick_point_con(self, driver, driven, mo=False, name=None):
        point_con = pm.pointConstraint(driver, driven, mo = mo, skip = 'none')
        if name:
            point_con.rename(name)
        else:
            point_con.rename(driven.stripNamespace() + '_pointCon')
        return point_con

class General(
	CleanUp,
	Curve,
	Misc,
	NaturalSort,
	Utils,
    ):

    def __init__(self, *args, **kwargs):
        super(General, self).__init__(*args, **kwargs)