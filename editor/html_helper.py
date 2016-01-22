#the following list contains all html standard attributes with description and a list of applicable html tags
#source http://www.w3.org/html/wg/drafts/html/master/index.html#attributes-1

#these tags will to be not written into the saved project because created at runtime
import remi.gui as gui

htmlInternallyUsedTags = ('id','parent_widget','children_list')

editorAttributeDictionary = {
    'background-color':{'type':gui.ColorPicker, 'description':'Background color of the widget','additional_data':{'affected_widget_attribute':'style'}},
    'background-image':{'type':gui.FileSelectionDialog, 'description':'An optional background image','additional_data':{'affected_widget_attribute':'style'}},
    'background-position':{'type':str, 'description':'The position of an optional background in the form 0% 0%','additional_data':{'affected_widget_attribute':'style'}},
    'background-repeat':{'type':gui.DropDown, 'description':'The repeat behaviour of an optional background image', 'additional_data':{'affected_widget_attribute':'style', 'possible_values':('repeat','repeat-x','repeat-y','no-repeat','inherit')}},
    'border-color':{'type':gui.ColorPicker, 'description':'Border color', 'additional_data':{'affected_widget_attribute':'style'}},
    'border-width':{'type':str, 'description':'Border thickness', 'additional_data':{'affected_widget_attribute':'style'}},
    'border-style':{'type':gui.DropDown, 'description':'Border thickness', 'additional_data':{'affected_widget_attribute':'style', 'possible_values':('none','solid','dotted','dashed')}},
    'color':{'type':gui.ColorPicker, 'description':'Text color', 'additional_data':{'affected_widget_attribute':'style'}},

    'disabled':{'type':bool, 'description':'Whether the form control is disabled', 'additional_data':{'affected_widget_attribute':'attributes'}},
    'hidden':{'type':bool, 'description':'Whether the element is relevant', 'additional_data':{'affected_widget_attribute':'attributes'}},
    'title':{'type':str, 'description':'Advisory information for the element', 'additional_data':{'affected_widget_attribute':'attributes'}}
}

#future use
htmlCsvEventsData = """Attribute;Element(s);Description;Value
onabort;all;abort event handler;Event handler content attribute
onautocomplete;all;autocomplete event handler;Event handler content attribute
onautocompleteerror;all;autocompleteerror event handler;Event handler content attribute
onafterprint;body;afterprint event handler for Window object;Event handler content attribute
onbeforeprint;body;beforeprint event handler for Window object;Event handler content attribute
onbeforeunload;body;beforeunload event handler for Window object;Event handler content attribute
onblur;all;blur event handler;Event handler content attribute
oncancel;all;cancel event handler;Event handler content attribute
oncanplay;all;canplay event handler;Event handler content attribute
oncanplaythrough;all;canplaythrough event handler;Event handler content attribute
onchange;all;change event handler;Event handler content attribute
onclick;all;click event handler;Event handler content attribute
onclose;all;close event handler;Event handler content attribute
oncontextmenu;all;contextmenu event handler;Event handler content attribute
oncuechange;all;cuechange event handler;Event handler content attribute
ondblclick;all;dblclick event handler;Event handler content attribute
ondrag;all;drag event handler;Event handler content attribute
ondragend;all;dragend event handler;Event handler content attribute
ondragenter;all;dragenter event handler;Event handler content attribute
ondragexit;all;dragexit event handler;Event handler content attribute
ondragleave;all;dragleave event handler;Event handler content attribute
ondragover;all;dragover event handler;Event handler content attribute
ondragstart;all;dragstart event handler;Event handler content attribute
ondrop;all;drop event handler;Event handler content attribute
ondurationchange;all;durationchange event handler;Event handler content attribute
onemptied;all;emptied event handler;Event handler content attribute
onended;all;ended event handler;Event handler content attribute
onerror;all;error event handler;Event handler content attribute
onfocus;all;focus event handler;Event handler content attribute
onhashchange;body;hashchange event handler for Window object;Event handler content attribute
oninput;all;input event handler;Event handler content attribute
oninvalid;all;invalid event handler;Event handler content attribute
onkeydown;all;keydown event handler;Event handler content attribute
onkeypress;all;keypress event handler;Event handler content attribute
onkeyup;all;keyup event handler;Event handler content attribute
onlanguagechange;body;languagechange event handler for Window object;Event handler content attribute
onload;all;load event handler;Event handler content attribute
onloadeddata;all;loadeddata event handler;Event handler content attribute
onloadedmetadata;all;loadedmetadata event handler;Event handler content attribute
onloadstart;all;loadstart event handler;Event handler content attribute
onmessage;body;message event handler for Window object;Event handler content attribute
onmousedown;all;mousedown event handler;Event handler content attribute
onmouseenter;all;mouseenter event handler;Event handler content attribute
onmouseleave;all;mouseleave event handler;Event handler content attribute
onmousemove;all;mousemove event handler;Event handler content attribute
onmouseout;all;mouseout event handler;Event handler content attribute
onmouseover;all;mouseover event handler;Event handler content attribute
onmouseup;all;mouseup event handler;Event handler content attribute
onwheel;all;wheel event handler;Event handler content attribute
onoffline;body;offline event handler for Window object;Event handler content attribute
ononline;body;online event handler for Window object;Event handler content attribute
onpagehide;body;pagehide event handler for Window object;Event handler content attribute
onpageshow;body;pageshow event handler for Window object;Event handler content attribute
onpause;all;pause event handler;Event handler content attribute
onplay;all;play event handler;Event handler content attribute
onplaying;all;playing event handler;Event handler content attribute
onpopstate;body;popstate event handler for Window object;Event handler content attribute
onprogress;all;progress event handler;Event handler content attribute
onratechange;all;ratechange event handler;Event handler content attribute
onreset;all;reset event handler;Event handler content attribute
onresize;all;resize event handler;Event handler content attribute
onscroll;all;scroll event handler;Event handler content attribute
onseeked;all;seeked event handler;Event handler content attribute
onseeking;all;seeking event handler;Event handler content attribute
onselect;all;select event handler;Event handler content attribute
onshow;all;show event handler;Event handler content attribute
onsort;all;sort event handler;Event handler content attribute
onstalled;all;stalled event handler;Event handler content attribute
onstorage;body;storage event handler for Window object;Event handler content attribute
onsubmit;all;submit event handler;Event handler content attribute
onsuspend;all;suspend event handler;Event handler content attribute
ontimeupdate;all;timeupdate event handler;Event handler content attribute
ontoggle;all;toggle event handler;Event handler content attribute
onunload;body;unload event handler for Window object;Event handler content attribute
onvolumechange;all;volumechange event handler;Event handler content attribute
onwaiting;all;waiting event handler;Event handler content attribute"""

