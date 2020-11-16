import os, sys
import pymel.core as pm
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'

def convert(*args):

    mel = pm.scrollField ( 'inputText_field' , q = True , text = True ) ;

    pointListTxtSuffix = mel.split ( '-p' ) [0] ;

    pointListTxt = mel.split ( '-k' ) [0] ;
    pointListTxt = pointListTxt.split ( pointListTxtSuffix ) [1] ;
    
    pointList = '[ ' ;

    pointListTxtList = pointListTxt.split ( '-p' ) ;

    for i in range ( 0 , len ( pointListTxtList ) ) :

        if ( pointListTxtList[i] == '' ) or ( pointListTxtList[i] == ' ' ) :
            pass ;
        else :

            pList = pointListTxtList[i].split ( ' ' ) ;
            point = [] ;

            for p in pList :
                if ( p == '' ) or ( p == ' ' ) :
                    pass ;
                else :
                    point.append ( p ) ;

            pointList += '( ' ;

            for j in range ( 0 , 3 ) :

                if j != 2 :
                    pointList += point[j] + ' , ' ;        
                else :
                    pointList += point[j] + ' ) ' ;

            if i == len ( pointListTxtList ) -1 :
                pass ;
            else :
                pointList += ', ' ;

    pointList += ']' ;

    pm.scrollField ( 'outputText_field' , e = True , text = pointList ) ;

    # [(0, 0, 0), (3, 5, 6), (10, 12, 14), (9, 9, 9)] )

def save_path_init(*args):
    save_path = '{0}{1}/{2}'.format(__self_path__.split(__project__)[0], __project__, 'data/curve_data')
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    return(save_path)

def save ( *args ) :

    fileNm = pm.textField ( '__self_name___textField' , q = True , text = True ) ;

    savePath = save_path_init()
    # savePath = __self_path__.split ( 'general' ) [0] + 'rig/curveData' ;

    if os.path.isfile ( savePath + '/' + fileNm + '.txt' ) == True :
    
        userInput = pm.confirmDialog (
            title = 'replace' ,
            message = '%s.txt exists, would you like to replace the file?' % fileNm ,
            button = [ 'Yes' , 'No' ] ,
            defaultButton = 'Yes' ,
            cancelButton = 'No' ,
            dismissString = 'No' ) ;

        if userInput == 'No' :
            pass ;
        else :
            textFile = open ( savePath + '/' + fileNm + '.txt' , 'w+' ) ;
        
            curvePointList = pm.scrollField ( 'outputText_field' , q = True , text = True ) ;

            textFile.write ( curvePointList ) ;
            textFile.close ( ) ;

    else :
        
        textFile = open ( savePath + '/' + fileNm + '.txt' , 'w+' ) ;
        
        curvePointList = pm.scrollField ( 'outputText_field' , q = True , text = True ) ;

        textFile.write ( curvePointList ) ;
        textFile.close ( ) ;

def collapseCmd ( *args ) :
    pm.window ( 'curveEP_melToPython_UI' , e = True , h = 10 ) ;

def textFileDirectory ( *args ) :
    savePath = save_path_init()
    os.startfile(savePath)

####################
####################


helpText = '''
this script convert "curve mel script" to python "point list"

1. draw curve using maya's EP curve tool, curve degree should be '1 linear'

2. copy echoed maya curve command from script editor

3. paste the command to the input scroll field

4. press convert button, point list should be printed to the output scroll field
'''

####################
####################

def run ( *args ) :
    
    width = 500 ;

    # check if window exists
    if pm.window ( 'curveEP_melToPython_UI' , exists = True ) :
        pm.deleteUI ( 'curveEP_melToPython_UI' ) ;
    else : pass ;
   
    window = pm.window ( 'curveEP_melToPython_UI', title = "MEL curve -> Python Point List" ,
        mnb = True , mxb = False , sizeable = True , rtf = True ) ;
        
    pm.window ( 'curveEP_melToPython_UI' , e = True , w = width , h = 10 ) ;
    with window :
    
        mainLayout = pm.rowColumnLayout ( nc = 1 ) ;
        with mainLayout :

            helpFrameLayout = pm.frameLayout ( label = 'help' , bgc = ( 0.5 , 0 , 0 ) , w  = width ,
                collapsable = True , collapse = True , cc = collapseCmd ) ;
            with helpFrameLayout :
                
                pm.scrollField ( editable = False , ww = True , w = width , h = 100 , text = helpText ) ;

            pm.separator ( vis = False , h = 5 ) ;

            inputFrameLayout = pm.frameLayout ( label = 'input' , bgc = ( 0 , 0.5 , 0 ) , w  = width ,
                collapsable = True , collapse = False , cc = collapseCmd ) ;
            with inputFrameLayout :

                inputLayout = pm.rowColumnLayout ( nc = 1 ) ;
                with inputLayout :

                    pm.scrollField ( 'inputText_field' , editable = True , ww = True , w = width , h = 150 ) ;
                    pm.button ( 'convert' , c = convert , bgc = ( 0 , 1 , 0 ) ) ;

            pm.separator ( vis = False , h = 5 ) ;

            outputFrameLayout = pm.frameLayout ( label = 'output' , bgc = ( 0 , 0 , 0.5 ) , w  = width ,
                collapsable = True , collapse = False , cc = collapseCmd ) ;
            with outputFrameLayout :            

                outputLayout = pm.rowColumnLayout ( nc = 1 ) ;
                with outputLayout :

                    pm.scrollField ( 'outputText_field' , editable = True , ww = True ,
                        w = width , h = 150 ) ;

                    saveLayout = pm.rowColumnLayout ( nc = 4 ,
                        cw = [ ( 1 , width / 10.0 * 3.5 ) , ( 2 , width / 10.0 * 3.5 ) , ( 3 , width / 10.0 * 1 ) , ( 4 , width / 10.0 * 2 ) ] ) ;
                    with saveLayout :

                        pm.text(label = '.../{0}/data/curve_data'.format(__project__))
                        pm.textField ( '__self_name___textField' ) ;
                        pm.text ( label = '.text' ) ;
                        pm.button ( label = 'save' , bgc = ( 0 , 0.7 , 1 ) , c = save ) ;

            pm.separator ( vis = False , h = 5 ) ;

            pm.button ( label = 'go to text file directory' , c = textFileDirectory , bgc = ( 1 , 1 , 1 ) ) ;

    window.show () ;