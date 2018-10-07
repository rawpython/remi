#the following list contains all html standard attributes with description and a list of applicable html tags
#source http://www.w3.org/html/wg/drafts/html/master/index.html#attributes-1

#these tags will to be not written into the saved project because created at runtime
import remi.gui as gui

htmlInternallyUsedTags = ('id'\
,'data-parent-widget'\
,'style'\
,'draggable'\
,'tabindex'\
,'onabort'\
,'onautocomplete'\
,'onautocompleteerror'\
,'onafterprint'\
,'onbeforeprint'\
,'onbeforeunload'\
,'onblur'\
,'oncancel'\
,'oncanplay'\
,'oncanplaythrough'\
,'onchange'\
,'onclick'\
,'onclose'\
,'oncontextmenu'\
,'oncuechange'\
,'ondblclick'\
,'ondrag'\
,'ondragend'\
,'ondragenter'\
,'ondragexit'\
,'ondragleave'\
,'ondragover'\
,'ondragstart'\
,'ondrop'\
,'ondurationchange'\
,'onemptied'\
,'onended'\
,'onerror'\
,'onfocus'\
,'onhashchange'\
,'oninput'\
,'oninvalid'\
,'onkeydown'\
,'onkeypress'\
,'onkeyup'\
,'onlanguagechange'\
,'onload'\
,'onloadeddata'\
,'onloadedmetadata'\
,'onloadstart'\
,'onmessage'\
,'onmousedown'\
,'onmouseenter'\
,'onmouseleave'\
,'onmousemove'\
,'onmouseout'\
,'onmouseover'\
,'onmouseup'\
,'onwheel'\
,'onoffline'\
,'ononline'\
,'onpagehide'\
,'onpageshow'\
,'onpause'\
,'onplay'\
,'onplaying'\
,'onpopstate'\
,'onprogress'\
,'onratechange'\
,'onreset'\
,'onresize'\
,'onscroll'\
,'onseeked'\
,'onseeking'\
,'onselect'\
,'onshow'\
,'onsort'\
,'onstalled'\
,'onstorage'\
,'onsubmit'\
,'onsuspend'\
,'ontimeupdate'\
,'ontoggle'\
,'onunload'\
,'onvolumechange'\
,'onwaiting')


editorAttributesGroupOrdering = {
    'Generic':1,
    'Geometry':2,
    'WidgetSpecific':3,
    'Background':4,
    'Border':5,
    'Font':6,
    'Layout':7
}

editorAttributeList = [
    ('title',{'type':str, 'description':'Advisory information for the element', 'affected_widget_attribute':'attributes', 'group':'Generic', 'additional_data':{}}),
    ('editor_varname',{'type':str, 'description':'Variable name', 'affected_widget_attribute':'attributes', 'group':'Generic', 'additional_data':{}}),
    ('visibility',{'type':gui.DropDown, 'description':'Specifies whether or not an element is visible.', 'affected_widget_attribute':'style', 'group':'Generic', 'additional_data':{'possible_values':('visible','hidden')}}),

    ('width',{'type':'css_size', 'description':'Widget width.', 'affected_widget_attribute':'style', 'group':'Geometry', 'additional_data':{}}),
    ('height',{'type':'css_size', 'description':'Widget height.', 'affected_widget_attribute':'style', 'group':'Geometry', 'additional_data':{}}),
    ('left',{'type':'css_size', 'description':'Widget left.', 'affected_widget_attribute':'style', 'group':'Geometry', 'additional_data':{}}),
    ('top',{'type':'css_size', 'description':'Widget top.', 'affected_widget_attribute':'style', 'group':'Geometry', 'additional_data':{}}),
    ('right',{'type':'css_size', 'description':'Widget right.', 'affected_widget_attribute':'style', 'group':'Geometry', 'additional_data':{}}),
    ('bottom',{'type':'css_size', 'description':'Widget bottom.', 'affected_widget_attribute':'style', 'group':'Geometry', 'additional_data':{}}),
    ('overflow',{'type':gui.DropDown, 'description':'Visibility behavior in case of content does not fit in size.', 'affected_widget_attribute':'style', 'group':'Geometry', 'additional_data':{'possible_values':('visible','hidden','scroll','auto')}}),


    ('grid-template-columns',{'type':'str', 'description':'Column sizes (i.e. 50% 30% 20%).', 'affected_widget_attribute':'style', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.GridBox]}}),
    ('grid-template-rows',{'type':'str', 'description':'Row sizes (i.e. 50% 30% 20%).', 'affected_widget_attribute':'style', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.GridBox]}}),
    ('grid-template-areas',{'type':'str', 'description':"Grid matrix (i.e. 'widget1 widget1 widget2' 'widget1 widget1 widget2').", 'affected_widget_attribute':'style', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.GridBox]}}),
    ('grid-gap',{'type':'css_size', 'description':"Defines the size of the gap between the rows and columns.", 'affected_widget_attribute':'style', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.GridBox]}}),

    ('value',{'type':int, 'description':"Defines the actual value for the progress bar.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.Progress], 'possible_values':'', 'min':0, 'max':10000, 'default':0, 'step':1}}),
    ('max',{'type':int, 'description':"Defines the maximum value for the progress bar.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.Progress], 'possible_values':'', 'min':0, 'max':10000, 'default':0, 'step':1}}),

    ('stroke',{'type':gui.ColorPicker, 'description':"Color for svg elements.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgLine, gui.SvgCircle, gui.SvgGroup, gui.SvgPolyline, gui.SvgRectangle, gui.SvgText, gui.SvgPath]}}),
    ('stroke-width',{'type':int, 'description':"Stroke width for svg elements.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgLine, gui.SvgCircle, gui.SvgGroup, gui.SvgPolyline, gui.SvgRectangle, gui.SvgText, gui.SvgPath], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('fill',{'type':gui.ColorPicker, 'description':"Fill color for svg elements.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgCircle, gui.SvgGroup, gui.SvgRectangle, gui.SvgText, gui.SvgPath]}}),
    ('fill-opacity',{'type':int, 'description':"Fill opacity for svg elements.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgCircle, gui.SvgGroup, gui.SvgRectangle, gui.SvgText, gui.SvgPath], 'possible_values':'', 'min':0.0, 'max':1.0, 'default':1.0, 'step':0.1}}),
    ('textLength',{'type':int, 'description':"Width for svg elements.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgText], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('rotate',{'type':int, 'description':"Rotation angle for svg elements.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgText], 'possible_values':'', 'min':0.0, 'max':360.0, 'default':1.0, 'step':0.1}}),
    ('d',{'type':str, 'description':"Instructions for SvgPath.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgPath]}}),
    ('x',{'type':int, 'description':"Coordinate for SvgShape.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgRectangle], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('y',{'type':int, 'description':"Coordinate for SvgShape.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgRectangle], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('width',{'type':int, 'description':"Width for SvgShape.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgRectangle], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('height',{'type':int, 'description':"Height for SvgShape.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgRectangle], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('cx',{'type':int, 'description':"Center coordinate for SvgCircle.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgCircle], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('cy',{'type':int, 'description':"Center coordinate for SvgCircle.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgCircle], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('r',{'type':int, 'description':"Radius of SvgCircle.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgCircle], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('x1',{'type':int, 'description':"P1 coordinate for SvgLine.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgLine], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('y1',{'type':int, 'description':"P1 coordinate for SvgLine.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgLine], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('x2',{'type':int, 'description':"P2 coordinate for SvgLine.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgLine], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),
    ('y2',{'type':int, 'description':"P2 coordinate for SvgLine.", 'affected_widget_attribute':'attributes', 'group':'WidgetSpecific', 'additional_data':{'applies_to':[gui.SvgLine], 'possible_values':'', 'min':0.0, 'max':10000.0, 'default':1.0, 'step':0.1}}),

    ('background-color',{'type':gui.ColorPicker, 'description':'Background color of the widget', 'affected_widget_attribute':'style', 'group':'Background', 'additional_data':{}}),
    ('background-image',{'type':'url_editor', 'description':'An optional background image', 'affected_widget_attribute':'style', 'group':'Background', 'additional_data':{}}),
    ('background-position',{'type':str, 'description':'The position of an optional background in the form 0% 0%', 'affected_widget_attribute':'style', 'group':'Background', 'additional_data':{}}),
    ('background-repeat',{'type':gui.DropDown, 'description':'The repeat behaviour of an optional background image', 'affected_widget_attribute':'style', 'group':'Background', 'additional_data':{'possible_values':('repeat','repeat-x','repeat-y','no-repeat','round','inherit')}}),
    ('opacity',{'type':float, 'description':"The opacity property sets the opacity level for an element.\nThe opacity-level describes the transparency-level, where 1 is not transparent at all, 0.5 is 50% see-through, and 0 is completely transparent."
                           , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':'', 'min':0.0, 'max':1.0, 'default':1.0, 'step':0.1}}),
    
    ('border-color',{'type':gui.ColorPicker, 'description':'Border color', 'affected_widget_attribute':'style', 'group':'Border', 'additional_data':{}}),
    ('border-width',{'type':'css_size', 'description':'Border thickness', 'affected_widget_attribute':'style', 'group':'Border', 'additional_data':{}}),
    ('border-style',{'type':gui.DropDown, 'description':'Border thickness', 'affected_widget_attribute':'style', 'group':'Border', 'additional_data':{'possible_values':('none','solid','dotted','dashed')}}),
    ('color',{'type':gui.ColorPicker, 'description':'Text color', 'affected_widget_attribute':'style', 'group':'Font', 'additional_data':{}}),
    ('font-family',{'type':str, 'description':'Font family name', 'affected_widget_attribute':'style', 'group':'Font', 'additional_data':{}}),
    ('font-size',{'type':'css_size', 'description':'Font size', 'affected_widget_attribute':'style', 'group':'Font', 'additional_data':{}}),
    ('font-style',{'type':gui.DropDown, 'description':'Style', 'affected_widget_attribute':'style', 'group':'Font', 'additional_data':{'possible_values':('normal','italic','oblique','inherit')}}),
    ('font-weight',{'type':gui.DropDown, 'description':'Style', 'affected_widget_attribute':'style', 'group':'Font', 'additional_data':{'possible_values':('normal','bold','bolder','lighter','100','200','300','400','500','600','700','800','900','inherit')}}),
    ('white-space',{'type':gui.DropDown, 'description':'Specifies how white-space inside an element is handled', 'affected_widget_attribute':'style', 'group':'Font', 'additional_data':{'possible_values':('normal','nowrap','pre','pre-line','pre-wrap','initial','inherit')}}),
    ('letter-spacing',{'type':'css_size', 'description':"Increases or decreases the space between characters in a text."
                        , 'affected_widget_attribute':'style', 'group':'Font', 'additional_data':{}}),
    
    ('flex-direction',{'type':gui.DropDown, 'description':'The flex-direction property specifies the direction of the flexible items. Note: If the element is not a flexible item, the flex-direction property has no effect.'
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':('row','row-reverse','column','column-reverse','initial','inherit')}}),
    ('display',{'type':gui.DropDown, 'description':'The display property specifies the type of box used for an HTML element'
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':('inline','block','contents','flex','grid','inline-block','inline-flex','inline-grid','inline-table','list-item','run-in','table','none','inherit')}}),
    ('justify-content',{'type':gui.DropDown, 'description':"The justify-content property aligns the flexible container's items when the items do not use all available space on the main-axis (horizontally)"
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':('flex-start','flex-end','center','space-between','space-around','initial','inherit')}}),
    ('align-items',{'type':gui.DropDown, 'description':'The align-items property specifies the default alignment for items inside the flexible container'
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':('stretch','center','flex-start','flex-end','baseline','initial','inherit')}}),
    ('flex-wrap',{'type':gui.DropDown, 'description':"The flex-wrap property specifies whether the flexible items should wrap or not. Note: If the elements are not flexible items, the flex-wrap property has no effect"
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':('nowrap','wrap','wrap-reverse','initial','inherit')}}),
    ('align-content',{'type':gui.DropDown, 'description':"The align-content property modifies the behavior of the flex-wrap property.\nIt is similar to align-items, but instead of aligning flex items, it aligns flex lines. Tip: Use the justify-content property to align the items on the main-axis (horizontally).Note: There must be multiple lines of items for this property to have any effect."
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':('stretch','center','flex-start','flex-end','space-between','space-around','initial','inherit')}}),
    ('flex-flow',{'type':gui.DropDown, 'description':"The flex-flow property is a shorthand property for the flex-direction and the flex-wrap properties. The flex-direction property specifies the direction of the flexible items."
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':('flex-direction','flex-wrap','initial','inherit')}}),
    ('order',{'type':int, 'description':"The order property specifies the order of a flexible item relative to the rest of the flexible items inside the same container. Note: If the element is not a flexible item, the order property has no effect."
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':'', 'min':-10000, 'max':10000, 'default':1, 'step':1}}),
    ('align-self',{'type':gui.DropDown, 'description':"The align-self property specifies the alignment for the selected item inside the flexible container. Note: The align-self property overrides the flexible container's align-items property"
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':('auto','stretch','center','flex-start','flex-end','baseline','initial','inherit')}}),
    ('flex',{'type':int, 'description':"The flex property specifies the length of the item, relative to the rest of the flexible items inside the same container. The flex property is a shorthand for the flex-grow, flex-shrink, and the flex-basis properties. Note: If the element is not a flexible item, the flex property has no effect."
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':'', 'min':-10000, 'max':10000, 'default':1, 'step':1}}),
    ('position',{'type':gui.DropDown, 'description':'The position property specifies the type of positioning method used for an element.'
                        , 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':('static','absolute','fixed','relative','initial','inherit')}})

    #:{'type':, 'description':'', 'affected_widget_attribute':'style', 'group':'Layout', 'additional_data':{'possible_values':''}},
    
    #'disabled' causes interaction confusion
    #('disabled',{'type':bool, 'description':'Whether the form control is disabled', 'affected_widget_attribute':'attributes', 'group':'Generic', 'additional_data':{}}),

    #'hidden':{'type':bool, 'description':'Whether the element is relevant', 'affected_widget_attribute':'attributes', 'group':'', 'additional_data':{}},
]

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

