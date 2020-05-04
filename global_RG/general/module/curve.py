################################################################################
__Script__		= 'global_RG.general.module.curve'
__Author__		= 'Weerapot Chaoman'
__Version__		= 2.00
__Date__		= 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################
import pymel.core as pm
import random
################################################################################

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
