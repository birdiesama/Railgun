import os ;
import ast ;
import pymel.core as pm ;

import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'

curvePath = '{0}{1}/{2}'.format(__self_path__.split(__project__)[0], __project__, 'data/curve_data')

def updateCurveList_cmd ( *args ) :

    curveList = os.listdir ( curvePath ) ;
    curveList.sort ( ) ;

    pm.textScrollList ( 'curveList_textScrollList' , e = True , ra = True ) ;

    for each in curveList :
        pm.textScrollList ( 'curveList_textScrollList' , e = True , append = each.split ( '.txt' ) [0] ) ;

def createCurve ( *args ) :

    selectedCurve = pm.textScrollList ( 'curveList_textScrollList' , q = True , selectItem = True ) [0] + '.txt' ;    
    curveTxtPath = curvePath + '/' + selectedCurve ;

    curveTxt = open ( curveTxtPath ) ;
    text = curveTxt.read ( ) ;
    point = ast.literal_eval ( text ) ;
    curveTxt.close ( ) ;

    pm.curve ( d = 1 , p = point ) ;

def textFileDirectory ( *args ) :
    savePath = __self_path__.split ( 'general' ) [0] + 'rig/curveData' ;
    os.startfile ( savePath ) ;

def setColor ( en = True , color = ( 0 , 0 , 0 ) , *args ) :

    selection = pm.ls ( sl = True ) ;
    
    selectionShape = pm.listRelatives ( shapes = True ) [0] ;
    selectionShape = pm.general.PyNode ( selectionShape ) ;
    selectionShape.overrideEnabled.set ( en ) ;
    selectionShape.overrideRGBColors.set ( en ) ;
    selectionShape.overrideColorRGB.set ( color ) ;

def convert_curve_to_type(type='joint', *args):

    selection_list = pm.ls(sl = True)

    if type == 'joint':
    
        for selection in selection_list:

            name = selection.nodeName()
            eachShape = pm.listRelatives ( selection , shapes = True ) [0] ;
           
            jnt = pm.createNode ( 'joint' ) ;
            
            pm.parent ( eachShape , jnt , s = True , r = True ) ;
            
            pm.delete ( selection ) ;
            pm.rename ( jnt , name ) ;
            
            jnt.radius.set ( 0 ) ;
            jnt.radius.lock ( ) ;
            jnt.radius.setKeyable ( False ) ;
            jnt.radius.showInChannelBox ( False ) ;

    if type == 'loc':
        for selection in selection_list:
            name = selection.nodeName()
            selection_shape = selection.getShape()
            loc_shape = pm.createNode('locator')
            loc = loc_shape.listRelatives(parent = True)[0]
            pm.delete(loc_shape)
            pm.parent(selection_shape, loc, s = True, r = True)
            pm.delete(selection)
            loc.rename(name)

def convertToJnt ( *args ) :
    convert_curve_to_type(type = 'joint')
        
# def convert_to_loc(*args):
#     convert_curve_to_type(type = 'loc')

def run ( *args ) :
    
    width = 240.00 ;
    title = 'curve creator' ;

    # check if window exists
    if pm.window ( 'curveCreator_UI' , exists = True ) :
        pm.deleteUI ( 'curveCreator_UI' ) ;
    else : pass ;
   
    window = pm.window ( 'curveCreator_UI', title = title ,
        mnb = True , mxb = False , sizeable = True , rtf = True ) ;
        
    pm.window ( 'curveCreator_UI' , e = True , w = width , h = 10 ) ;
    with window :
    
        mainLayout = pm.rowColumnLayout ( nc = 1 ) ;
        with mainLayout :
            
            utilityLayout = pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , width / 2.0 ) , ( 2 , width / 2.0 ) ] ) ;
            with utilityLayout :

                pm.button ( label = 'go to text file directory' , bgc = ( 1 , 1 , 1 ) , c = textFileDirectory ) ;
                pm.button ( label = 'refresh' , bgc = ( 0.5 , 1 , 0.85 ) , c = updateCurveList_cmd ) ; 

            pm.textScrollList ( 'curveList_textScrollList' , width = width , h = 150 , ams = False ) ;

            pm.button ( label = 'create' , c = createCurve ) ;
            #pm.button ( label = 'create' , bgc = ( 1 , 0.2 , 0.5 ) , c = createCurve ) ;

            pm.separator ( vis = False , h = 5 ) ;

            pm.button ( label = 'convert to joint' , c = convertToJnt , bgc = ( 0 , 0 , 0.5 ) ) ;
            pm.button(label = 'convert to loc', c = convert_to_loc, bgc = (0, 0, 0.5))

            pm.separator ( vis = False , h = 5 ) ;

            colorLayout = pm.rowColumnLayout ( nc = 8 , w = width ,
                cw = [
                ( 1 , width / 8.0 ) , ( 2 , width / 8.0 ) , ( 3 , width / 8.0 ) , ( 4 , width / 8.0 ) , 
                ( 5 , width / 8.0 ) , ( 6 , width / 8.0 ) , ( 7 , width / 8.0 ) , ( 8 , width / 8.0 ) ] ) ;
            with colorLayout :
                
                def n_cmd ( *args ) : setColor ( en = False , color = ( 0 , 0 , 0 ) ) ;
                pm.button ( label = 'n' , w =  width / 8.0 , c = n_cmd ) ;

                def w_cmd ( *args ) : setColor ( en = True , color = ( 1 , 1 , 1 ) ) ;
                pm.button ( label = 'w' , w =  width / 8.0 , bgc = ( 1 , 1 , 1 ) , c = w_cmd ) ;
                
                def r_cmd ( *args ) : setColor ( en = True , color = ( 1 , 0 , 0 ) ) ;
                pm.button ( label = 'r' , w =  width / 8.0 , bgc = ( 1 , 0 , 0 ) , c = r_cmd ) ;

                def b_cmd ( *args ) : setColor ( en = True , color = ( 0 , 0 , 1 ) ) ;
                pm.button ( label = 'b' , w =  width / 8.0 , bgc = ( 0 , 0 , 1 ) , c = b_cmd ) ;

                def g_cmd ( *args ) : setColor ( en = True , color = ( 0 , 1 , 0 ) ) ;
                pm.button ( label = 'g' , w =  width / 8.0 , bgc = ( 0 , 1 , 0 ) , c = g_cmd ) ;
                
                def y_cmd ( *args ) : setColor ( en = True , color = ( 1 , 1 , 0 ) ) ;
                pm.button ( label = 'y' , w =  width / 8.0 , bgc = ( 1 , 1 , 0 ) , c = y_cmd ) ;
                
                def lb_cmd ( *args ) : setColor ( en = True , color = ( 0 , 1 , 1 ) ) ;
                pm.button ( label = 'lb' , w =  width / 8.0 , bgc = ( 0 , 1 , 1 ) , c = lb_cmd ) ;
                
                def br_cmd ( *args ) : setColor ( en = True , color = (  0.3 , 0.1 , 0.1 ) ) ;
                pm.button ( label = 'br' , w =  width / 8.0 , bgc = ( 0.3 , 0.1 , 0.1 ) , c = br_cmd ) ;

    updateCurveList_cmd ( ) ;
                
    window.show ( ) ;
