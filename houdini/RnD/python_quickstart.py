### Create a new tool shelf
### Create a Python tool on the shelf and start developing a snippet

import hou

def return_type(sel=None):
    if sel:
        # print('We are awesome')
        for each in sel:
            print(each.type())

return_type(sel = hou.selectedNodes())


### Connecting / Disconnection nodes using Python

obj = hou.node('/obj')
geo = obj.createNode('geo', 'awesome_geo')

# adding parameter to a selected node
# ref: https://gfxhacks.com/create-parameters-in-houdini-with-python/

def add_parm_demo():

    node = hou.selectedNodes()[0]

    # creating parameters template
    float2_parm = hou.FloatParmTemplate(name = "float2", label = "Float 2", num_components = 2, default_value = [1, 0.5])
    float3_parm = hou.FloatParmTemplate(name = "float3", label = "Float 3", num_components = 3, default_value = [0, 1, 2])
    string1_parm = hou.StringParmTemplate(name = "string1", label = "String1", num_components = 1, default_value = ["Birdie is Awesome"])
    string2_parm = hou.StringParmTemplate(name = "string2", label = "String 2", num_components = 2, default_value = ["test", "tset"])

    # how to create folder?
    # https://www.sidefx.com/docs/houdini/hom/hou/FolderParmTemplate.html
    
    folderDefault = hou.FolderParmTemplate(name = "folderDefault", label = "Folder Default")

    # __init__(name, label, parm_templates=(), folder_type=hou.folderType.Tabs, is_hidden=False, ends_tab_group=False, tags={}, conditionals={}, tab_conditionals={})
    
    
    # way 1
    ori_parmTemplateGrp = node.parmTemplateGroup()
    
    ori_parmTemplateGrp.append(float2_parm)
    ori_parmTemplateGrp.append(float3_parm)
    ori_parmTemplateGrp.append(string1_parm)
    ori_parmTemplateGrp.append(string2_parm)
        
    # way 2
    new_parmTemplateGrp = hou.ParmTemplateGroup()

    new_parmTemplateGrp.append(folderDefault)
    
    # # this way doesn't have control which folder the parameter will be put in
    # new_parmTemplateGrp.append(float2_parm)
    # new_parmTemplateGrp.append(float3_parm)
    # new_parmTemplateGrp.append(string1_parm)
    # new_parmTemplateGrp.append(string2_parm)
    
    # new_parmTemplateGrp.appendToFolder(0, float2_parm)
    # new_parmTemplateGrp.appendToFolder(0, float3_parm)
    # new_parmTemplateGrp.appendToFolder(0, string1_parm)
    # new_parmTemplateGrp.appendToFolder(0, string2_parm)
    
    #appendToFolder(label_or_labels_or_parm_template_or_indices, parm_template)

    node.setParmTemplateGroup(new_parmTemplateGrp)

add_parm_demo()


# __init__(name, label, num_components, default_value=(), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, file_type=hou.fileType.Any, menu_items=(), menu_labels=(), icon_names=(), item_generator_script=None, item_generator_script_language=None, menu_type=hou.menuType.Normal, disable_when=None, is_hidden=False, is_label_hidden=False, join_with_next=False, help=None, script_callback=None, script_callback_language=hou.scriptLanguage.Hscript, tags={}, default_expression=(), default_expression_language=())