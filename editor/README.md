
## *The WYSIWYG Editor for your Remi gui*

Introduction
===

![Alt text](https://raw.githubusercontent.com/dddomodossola/remi/master/editor/res/preview.png "Editor window")

The editor_app allows you to graphically design your gui interface in an easy to use environment.
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

Project configuration
===