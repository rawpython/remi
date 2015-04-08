"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import gui
from gui import *

class App( BaseApp ):
	def __init__( self, *args ):
		super( App, self ).__init__( *args )

	def main( self ):
		mainContainer = gui.widget( 600, 410, True, 10 )
		
		subContainerLeft = gui.widget( 300, 370, False, 10 )
		self.img = gui.imageWidget( 100, 100, "logo.png" )
	
		self.table = gui.tableWidget( 300, 200 )
		self.tableTitle = gui.labelWidget( 300, 20, "This is a table" )
		row = gui.rowTable()
		item = gui.titleTable()
		item.append( str(id(item)), "ID" )
		row.append( str(id(item)), item )
		item = gui.titleTable()
		item.append( str(id(item)), "First Name" )
		row.append( str(id(item)), item )
		item = gui.titleTable()
		item.append( str(id(item)), "Last Name" )
		row.append( str(id(item)), item )
		self.table.append( str(id(row)), row )
		self.addTableRow( self.table, "101", "Danny", "Young" )
		self.addTableRow( self.table, "102", "Christine", "Holand" )
		self.addTableRow( self.table, "103", "Lars", "Gordon" )
		self.addTableRow( self.table, "104", "Roberto", "Robitaille" )
		self.addTableRow( self.table, "105", "Maria", "Papadopoulos" )
		
		#the arguments are	width - height - layoutOrientationOrizontal
		subContainerRight = gui.widget( 240, 370, False,10 )
		
		self.lbl = gui.labelWidget( 200, 30, "This is a LABEL!" )
		self.lbl.setUpdateTimer( self, 500 )
		
		self.bt = gui.buttonWidget( 200, 30, "Press me!" )
		#setting the listener for the onclick event of the button
		self.bt.setOnClickListener( self, "onButtonPressed" )
		
		self.txt = gui.textareaWidget( 200, 30 )
		self.txt.text( "This is a TEXTAREA" )
		self.txt.setOnChangeListener( self, "onTextAreaChange" )
		
		self.spin = gui.spinboxWidget( 200, 30 )
		self.spin.setOnChangeListener( self, "onSpinChange" )
		
		self.btInputDiag = gui.buttonWidget( 200, 30, "Open InputDialog" )
		self.btInputDiag.setOnClickListener( self, "openInputDialog" )
		
		self.listWidget = gui.listWidget( 220,60 )
		li0 = gui.listItem( 200,20, "Item 0")
		li0.setOnClickListener( self, "listItem0_selected" )
		li1 = gui.listItem( 200,20, "Item 1")
		li1.setOnClickListener( self, "listItem1_selected" )
		li2 = gui.listItem( 200,20, "Item 2")
		li2.setOnClickListener( self, "listItem2_selected" )
		self.listWidget.append( "0", li0 )
		self.listWidget.append( "1", li1 )
		self.listWidget.append( "2", li2 )

		self.combo = gui.comboWidget( 200, 20 )
		c0 = gui.comboItem( 200, 20, "Combo 0" )
		c1 = gui.comboItem( 200, 20, "Combo 1" )
		self.combo.append( "0", c0 )
		self.combo.append( "1", c1 )
		self.combo.setOnChangeListener( self, "comboChanged" )
		
		#appending a widget to another, the first argument is a string key
		subContainerRight.append( "1", self.lbl )
		subContainerRight.append( "2", self.bt )
		subContainerRight.append( "3", self.txt )
		subContainerRight.append( "4", self.spin )
		subContainerRight.append( "5", self.btInputDiag )
		subContainerRight.append( "6", self.listWidget )
		subContainerRight.append( "7", self.combo )
		
		subContainerLeft.append( "0", self.img )
		subContainerLeft.append( "1", self.tableTitle )
		subContainerLeft.append( "2", self.table )
		
		
		mainContainer.append( "0", subContainerLeft )
		mainContainer.append( "1", subContainerRight )
		#returning the root widget
		return mainContainer
	
	def addTableRow( self, table, field1, field2, field3 ):
		row = gui.rowTable()
		item = gui.itemTable()
		item.append( str(id(item)), field1 )
		row.append( str(id(item)), item )
		item = gui.itemTable()
		item.append( str(id(item)), field2 )
		row.append( str(id(item)), item )
		item = gui.itemTable()
		item.append( str(id(item)), field3 )
		row.append( str(id(item)), item )
		table.append( str(id(row)), row )
		
	#listener function
	def onButtonPressed( self, x, y ):
		self.lbl.setText( "Button pressed!" )
		self.bt.text("Hi!")

	def onTextAreaChange( self, newValue ):
		self.lbl.setText( "Text Area value changed!" )
	
	def onSpinChange( self, newValue ):
		self.lbl.setText( "SpinBox changed, new value: " + newValue )
	
	def openInputDialog( self, x, y ):
		self.inputDialog = gui.inputDialog( "Input Dialog", "Your name?" )
		self.inputDialog.setOnConfirmValueListener( self, "onInputDialogConfirm" )
		
		#here is returned the Input Dialog widget, and it will be shown
		return self.inputDialog
		
	def onInputDialogConfirm( self, value ):
		self.lbl.setText( "Hello " + value )
		
	def listItem0_selected( self, x, y ):
		self.lbl.setText( "List Item 0 selected" )
	def listItem1_selected( self, x, y ):
		self.lbl.setText( "List Item 1 selected" )
	def listItem2_selected( self, x, y ):
		self.lbl.setText( "List Item 2 selected" )
		
	def comboChanged( self, value ):
		self.lbl.setText( "New Combo value: " + value )
		
#starts the webserver	
start( App )
