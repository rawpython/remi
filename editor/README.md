
# *The WYSIWYG Editor for your Remi gui*

Introduction
===
What is Remi?
**A Platform independent Python GUI library for your applications**

[![Join the chat at https://gitter.im/dddomodossola/remi](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/dddomodossola/remi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

RemI is a GUI library for Python applications which transpiles an application's interface into HTML to be rendered in a web browser. This removes platform-specific dependencies and lets you easily develop cross-platform applications in Python!
[More info at https://github.com/dddomodossola/remi](https://github.com/dddomodossola/remi)

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/preview.png "Editor window")

The **editor_app** allows you to graphically design your gui interface in an easy to use environment.
From a collection of widgets (on the left side of the screen) you can choose the right one you would like to add to your interface.
Choosing a widget, you have to fill some fields required to allocate the widget. Besides the constructor parameters, some additional information are required:
- **Variable name**: an identifier that will be used in order to produce the app code;
- **Overload base class** flag: defines if the variable have to be an instance of a new class that will overload the base class.

On the right side of the screen, the widget's parameters are available. It consists in a set of html and css attributes.
A widget can be selected by clicking on it. Once a widget is selected, it can be customized by the property panel.

Widgets can be added one into another. Currently three types of containers are available:
- **Widget**: a generic container that allows absolute positioning;
- **HBox, VBox**: both layouts automatically inner widgets.

By using Widget container you can be able to resize and drag widgets manually.

HBox and VBox containers **does not allow** the manual drag and resize of widgets. But widgets can be resized by the right property panel.

Once your interface is ready, you can save you app. It will be exported **directly into python code**.
Your app **can be reloaded for editing**.


A step by step example
===
Now, let's create our first *Hello World* application.

First of all we have to select from the left side toolbox the Widget component. It will be our main window.
In the shown dialog we have to write a name for the variable. We will call it *mainContainer*.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/new_container.png "New Widget container")


Then, once the widget is added to the editor, you can drag and resize it.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/drag_resize_container.png "Drag and resize container")


Now, from the left side toolbox we select a Label widget that will contain our *Hello World* message.
Again, we have to type the variable name for this widget.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/new_label.png "Add new label")


Then, we can select the label by clicking on it in order to drag and resize.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/drag_resize_label.png "Drag and resize label")


We need for sure a Button. Since we have to add it to the mainContainer, we have to select the container by clicking on it.
After that, click on the Button widget in the left side toolbox. 
Type the variable name and confirm.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/new_button.png "Add new button")


Select the Button widget by clicking on it and drag and resize.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/drag_resize_button.png "Drag and resize button")


Now, all the required widgets are added. We have to connect the *onclick* event from the button to a listener, in our case the listener will be the main App.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/connect_button.png "Connect button onclick event to App")


All it's done, save the project by the upper menu bar.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/save_menu.png "Save menu")


Select the destination folder. Type the app filename and confirm.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/save_dialog.png "Save dialog")


We can now edit the code to say the *Hello World* message.

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/edit_hello_message.png "Edit the code to say Hello World")


Run the application and... Say Hello!

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/tutorial_images/hello.png "Run the App")


Project configuration
===