Traducción gracias a: Julio Contreras

gui
===

Esta es una version pre-pre-pre-alpha, una gui python basada en HTML y de esta manera, una plataforma independiente.
Esto permite crear una plataforma GUI independiente con python. 
La gui entera será mostrada en el explorador porque esta es representada en HTML. 
Cuando tu aplicación inicia, esta inicia como un servidor web que será accesible en tu red.

Porqué otra librería gui? Ok, Kivy es la mejor, Tk es histórica, pyQt es buena también, 
pero por cada plataforma que aparece tenemos que esperar un puerto. 
Esta librería permite mostrar una interfaz de usuario en donde sea que haya un explorador.

Justo ahora está incompleta. Estos widgets están disponibles:

- widget : como un panel vacío
- buttonWidget
- textareaWidget : para texto editable.
- spinboxWidget
- labelWidget
- inputDialog
- listWidget
- comboWidget
- imageWidget
- tableWidget
- objectWidget : te permite mostrar un objeto embebido como pdf, swf...

Una aplicación básica aparece como:

<pre><code>
import gui
from gui import *

class App( BaseApp ):
	def __init__( self, *args ):
		super( App, self ).__init__( *args )
		
	def main( self ):
		#the arguments are	width - height - layoutOrientationOrizontal
		wid = gui.widget( 100, 60, False )
		self.lbl = gui.labelWidget( 100, 30, "Hello world!" )
		self.bt = gui.buttonWidget( 100, 30, "Press me!" )
			
		#setting the listener for the onclick event of the button
		self.bt.setOnClickListener( self, "onButtonPressed" )
			
		#appending a widget to another, the first argument is a string key
		wid.append( "1", self.lbl )
		wid.append( "2", self.bt )
			
		#setting up the root widget
		self.client.root = wid
	
	#listener function
	def onButtonPressed( self, x, y ):
		self.lbl.setText( "Button pressed!" )
		self.bt.text("Hi!")

#starts the webserver	
start( App )
</code></pre>

De forma que para ver la interfaz de usuario, 
abre tu explorador preferido (Yo uso Chrome) and type : "http://127.0.0.1:8080"
Tu puedes cambiar la dirección url, editando el archivo "configuration.py"

Probado en Android, Linux, Windows con el explorador web Google Chrome.
