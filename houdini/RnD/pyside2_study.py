'''
### Nook's example

from PySide2.QtWidgets import QApplication, QLabel, QMainWindow
from PySide2.QtCore import Qt
import sys

class MainWindow(QMainWindow):
	def __init__(self):
		super(self.__class__,self).__init__()
		self.setWindowTitle("My App")
		
		widget = QLabel("Hello")
		font = widget.font()
		font.setPointSize(30)
		widget.setFont(font)
		align_top_left = Qt.AlignLeft | Qt.AlignTop
		#Qt.AlignLeft , Qt.AlignRight , Qt.AlignHCenter , Qt.AlignJustify , Qt.AlignTop , Qt.AlignBottom , Qt.AlignVCenter 
		widget.setAlignment(align_top_left)
		self.setCentralWidget(widget)


window = MainWindow()
window.show()
'''

### resource: https://www.pythonguis.com/tutorials/pyside-creating-your-first-window/

from PySide2.QtWidgets import (
	QMainWindow, 
	QPushButton,
	QVBoxLayout,
	QWidget,
	)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Test")
        self.resize(250, 100)

        print_button = QPushButton("Press Me!")
        print_button.clicked.connect(self.test)

        node_type_button = QPushButton("Node Type Name")
        node_type_button.clicked.connect(self.node_type)
        
        layout = QVBoxLayout()
        layout.addWidget(print_button)
        layout.addWidget(node_type_button)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def test(self):
    	print('We are awesome!')

    def node_type(self):
    	print('Node Type: None')
        
window = MainWindow() # object instance
window.show() # windows are hidden by default


# C:\Users\birdi\Documents\houdini19.5\houdini.env
# C:\Program Files\Sublime Text 3
# EDITOR = "C:/Program Files/Sublime Text 3/sublime_text.exe"

import hou

def return_type(sel=None):
    if sel:
        # print('We are awesome')
        for each in sel:
            node_type = each.type().name()
            print(node_type)
            
# type() → hou.NodeType
# Return the hou.NodeType object for this node.

return_type(sel = hou.selectedNodes())