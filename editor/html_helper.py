import csv

#the following list contains all html standard attributes with description and a list of applicable html tags
#source http://www.w3.org/html/wg/drafts/html/master/index.html#attributes-1

htmlAttributeDict = {}

htmlCsvAttributeData = """Attribute;Element(s);Description;Value
abbr;th;Alternative label to use for the header cell when referencing the cell in other contexts;Text
accept;input;Hint for expected file type in file upload controls;Set of comma-separated tokens consisting of valid MIME types with no parameters or audio/, video/, or image/
accept-charset;form;Character encodings to use for form submission;Ordered set of unique space-separated tokens, ASCII case-insensitive, consisting of labels of ASCII-compatible encodings
accesskey;HTML elements;Keyboard shortcut to activate or focus element;Ordered set of unique space-separated tokens, case-sensitive, consisting of one Unicode code point in length
action;form;URL to use for form submission;Valid non-empty URL potentially surrounded by spaces
allowfullscreen;iframe;Whether to allow the iframe's contents to use requestFullscreen();bool
alt;"area; img; input";Replacement text for use when images are not available;Text
async;script;Execute script when available, without blocking;bool
autocomplete;form;Default setting for autofill feature for controls in the form;"on; off"
autocomplete;"input; select; textarea";Hint for form autofill feature;Autofill field name and related tokens
autofocus;"button; input; keygen; select; textarea";Automatically focus the form control when the page is loaded;bool
autoplay;"audio; video";Hint that the media resource can be started automatically when the page is loaded;bool
challenge;keygen;String to package with the generated and signed public key;Text
charset;meta;Character encoding declaration;Encoding label
charset;script;Character encoding of the external script resource;Encoding label
checked;"menuitem; input";Whether the command or control is checked;bool
cite;"blockquote; del; ins; q";Link to the source of the quotation or more information about the edit;Valid URL potentially surrounded by spaces
class;HTML elements;Classes to which the element belongs;Set of space-separated tokens
cols;textarea;Maximum number of characters per line;int greater than zero
colspan;"td; th";Number of columns that the cell is to span;int greater than zero
command;menuitem;Command definition;ID
content;meta;Value of the element;Text
contenteditable;HTML elements;Whether the element is editable;"true; false"
contextmenu;HTML elements;The element's context menu;ID
controls;"audio; video";Show user agent controls;bool
coords;area;Coordinates for the shape to be created in an image map;Valid list of integers
crossorigin;"audio; img; link; script; video";How the element handles crossorigin requests;"anonymous; use-credentials"
data;object;Address of the resource;Valid non-empty URL potentially surrounded by spaces
datetime;"del; ins";Date and (optionally) time of the change;Valid date string with optional time
datetime;time;Machine-readable value;Valid month string, valid date string, valid yearless date string, valid time string, valid local date and time string, valid time-zone offset string, valid global date and time string, valid week string, int, or valid duration string
default;menuitem;Mark the command as being a default command;bool
default;track;Enable the track if no other text track is more suitable;bool
defer;script;Defer script execution;bool
dir;HTML elements;The text directionality of the element;"ltr; rtl; auto"
dir;bdo;The text directionality of the element;"ltr; rtl"
dirname;"input; textarea";Name of form field to use for sending the element's directionality in form submission;Text
disabled;"button; menuitem; fieldset; input; keygen; optgroup; option; select;textarea";Whether the form control is disabled;bool
download;"a; area";Whether to download the resource instead of navigating to it, and its file name if so;Text
draggable;HTML elements;Whether the element is draggable;"true; false"
dropzone;HTML elements;Accepted item types for drag-and-drop;Unordered set of unique space-separated tokens, ASCII case-insensitive, consisting of accepted types and drag feedback
enctype;form;Form data set encoding type to use for form submission;"application/x-www-form-urlencoded; multipart/form-data; text/plain"
for;label;Associate the label with form control;ID
for;output;Specifies controls from which the output was calculated;Unordered set of unique space-separated tokens, case-sensitive, consisting of IDs
form;button; "fieldset; input; keygen; label; object; output; select; textarea";Associates the control with a form element;ID
formaction;"button; input";URL to use for form submission;Valid non-empty URL potentially surrounded by spaces
formenctype;"button; input";Form data set encoding type to use for form submission;"application/x-www-form-urlencoded; multipart/form-data; text/plain"
formmethod;"button; input";HTTP method to use for form submission;"GET; POST"
formnovalidate;"button; input";Bypass form control validation for form submission;bool
formtarget;"button; input";Browsing context for form submission;Valid browsing context name or keyword
headers;"td; th";The header cells for this cell;Unordered set of unique space-separated tokens, case-sensitive, consisting of IDs
height;"canvas; embed; iframe; img; input; object; video";Vertical dimension;int
hidden;HTML elements;Whether the element is relevant;bool
high;meter;Low limit of high range;float
href;"a; area";Address of the hyperlink;Valid URL potentially surrounded by spaces
href;link;Address of the hyperlink;Valid non-empty URL potentially surrounded by spaces
href;base;Document base URL;Valid URL potentially surrounded by spaces
hreflang;"a; area; link";Language of the linked resource;Valid BCP 47 language tag
http-equiv;meta;Pragma directive;Text
icon;menuitem;Icon for the command;Valid non-empty URL potentially surrounded by spaces
id;HTML elements;The element's ID;Text
inputmode;"input; textarea";Hint for selecting an input modality;"verbatim; latin; latin-name; latin-prose; full-width-latin; kana; kana-name; katakana; numeric; tel; email; url"
ismap;img;Whether the image is a server-side image map;bool
itemid;HTML elements;Global identifier for a microdata item;Valid URL potentially surrounded by spaces
itemprop;HTML elements;Property names of a microdata item;Unordered set of unique space-separated tokens, case-sensitive, consisting of valid absolute URLs, defined property names, or text
itemref;HTML elements;Referenced elements;Unordered set of unique space-separated tokens, case-sensitive, consisting of IDs
itemscope;HTML elements;Introduces a microdata item;bool
itemtype;HTML elements;Item types of a microdata item;Unordered set of unique space-separated tokens, case-sensitive, consisting of valid absolute URL
keytype;keygen;The type of cryptographic key to generate;Text
kind;track;The type of text track;"subtitles; captions; descriptions; chapters; metadata"
label;"menuitem; menu; optgroup; option; track";User-visible label;Text
lang;HTML elements;Language of the element;Valid BCP 47 language tag or the empty string
list;input;List of autocomplete options;ID
loop;"audio; video";Whether to loop the media resource;bool
low;meter;High limit of low range;float
manifest;html;Application cache manifest;Valid non-empty URL potentially surrounded by spaces
max;input;Maximum value;Varies
max;"meter; progress";Upper bound of range;float
maxlength;"input; textarea";Maximum length of value;int
media;"link; style";Applicable media;Valid media query list
mediagroup;"audio; video";Groups media elements together with an implicit MediaController;Text
menu;button;Specifies the element's designated pop-up menu;ID
method;form;HTTP method to use for form submission;"GET; POST; dialog"
min;input;Minimum value;Varies
min;meter;Lower bound of range;float
minlength;"input; textarea";Minimum length of value;int
multiple;"input; select";Whether to allow multiple values;bool
muted;"audio; video";Whether to mute the media resource by default;bool
name;"button; fieldset; input; keygen; output; select; textarea";Name of form control to use for form submission and in the form.elements API;Text
name;form;Name of form to use in the document.forms API;Text
name;"iframe; object";Name of nested browsing context;Valid browsing context name or keyword
name;map;Name of image map to reference from the usemap attribute;Text
name;meta;Metadata name;Text
name;param;Name of parameter;Text
nonce;"script; style";Cryptographic nonce used in Content Security Policy checks [CSP];Text
novalidate;form;Bypass form control validation for form submission;bool
open;details;Whether the details are visible;bool
open;dialog;Whether the dialog box is showing;bool
optimum;meter;Optimum value in gauge;float
pattern;input;Pattern to be matched by the form control's value;Regular expression matching the JavaScript Pattern production
placeholder;"input; textarea";User-visible label to be placed within the form control;Text
poster;video;Poster frame to show prior to video playback;Valid non-empty URL potentially surrounded by spaces
preload;"audio; video";Hints how much buffering the media resource will likely need;"none; metadata; auto"
radiogroup;menuitem;Name of group of commands to treat as a radio button group;Text
readonly;"input; textarea";Whether to allow the value to be edited by the user;bool
rel;"a; area; link";Relationship between the document containing the hyperlink and the destination resource;Set of space-separated tokens
required;"input; select; textarea";Whether the control is required for form submission;bool
reversed;ol;Number the list backwards;bool
rows;textarea;Number of lines to show;int greater than zero
rowspan;"td; th";Number of rows that the cell is to span;int
sandbox;iframe;Security rules for nested content;Unordered set of unique space-separated tokens, ASCII case-insensitive, consisting of allow-forms, allow-modals, allow-pointer-lock, allow-popups, allow-popups-to-escape-sandbox, allow-same-origin, allow-scripts and allow-top-navigation"
spellcheck;HTML elements;Whether the element is to have its spelling and grammar checked;"true; false"
scope;th;Specifies which cells the header cell applies to;"row; col; rowgroup; colgroup"
scoped;style;Whether the styles apply to the entire document or just the parent subtree;bool
seamless;iframe;Whether to apply the document's styles to the nested content;bool
selected;option;Whether the option is selected by default;bool
shape;area;The kind of shape to be created in an image map;"circle; default; poly; rect"
size;"input; select";Size of the control;int greater than zero
sizes;link;Sizes of the icons (for rel=icon);Unordered set of unique space-separated tokens, ASCII case-insensitive, consisting of sizes
sortable;table;Enables a sorting interface for the table;bool
sorted;th;Column sort direction and ordinality;Set of space-separated tokens, ASCII case-insensitive, consisting of neither, one, or both of reversed and a int greater than zero
span;"col; colgroup";Number of columns spanned by the element;int greater than zero
src;"audio; embed; iframe; img; input; script; source; track; video";Address of the resource;Valid non-empty URL potentially surrounded by spaces
srcdoc;iframe;A document to render in the iframe;The source of an iframe srcdoc document
srclang;track;Language of the text track;Valid BCP 47 language tag
srcset;img;Images to use in different situations (e.g. high-resolution displays, small monitors, etc);Comma-separated list of image candidate strings
start;ol;Ordinal value of the first item;Valid integer
step;input;Granularity to be matched by the form control's value;"float greater than zero, or any"
style;HTML elements;Presentational and formatting instructions;CSS declarations
tabindex;HTML elements;Whether the element is focusable, and the relative order of the element for the purposes of sequential focus navigation;Valid integer
target;"a; area";Browsing context for hyperlink navigation;Valid browsing context name or keyword
target;base;Default browsing context for hyperlink navigation and form submission;Valid browsing context name or keyword
target;form;Browsing context for form submission;Valid browsing context name or keyword
title;HTML elements;Advisory information for the element;Text
title;"abbr; dfn";Full term or expansion of abbreviation;Text
title;input;Description of pattern (when used with pattern attribute);Text
title;menuitem;Hint describing the command;Text
title;link;Title of the link;Text
title;link; style;Alternative style sheet set name;Text
translate;HTML elements;Whether the element is to be translated when the page is localized;"yes; no"
type;"a; area; link";Hint for the type of the referenced resource;Valid MIME type
type;button;Type of button;"submit; reset; button; menu"
type;"embed; object; script; source; style";Type of embedded resource;Valid MIME type
type;input;Type of form control;input type keyword
type;menu;Type of menu;"popup; toolbar"
type;menuitem;Type of command;"command; checkbox; radio"
type;ol;Kind of list marker;"1; a; A; i; I"
typemustmatch;object;Whether the type attribute and the Content-Type value need to match for the resource to be used;bool
usemap;"img; object";Name of image map to use;Valid hash-name reference
value;"button; option";Value to be used for form submission;Text
value;data;Machine-readable value;Text
value;input;Value of the form control;Varies
value;li;Ordinal value of the list item;Valid integer
value;"meter; progress";Current value of the element;float
value;param;Value of parameter;Text
width;"canvas; embed; iframe; img; input; object; video";Horizontal dimension;int
wrap;textarea;How the value of the form control is to be wrapped for form submission;"soft; hard"
"""

htmlEventsDict = {}

htmlCsvEventsData = """Attribute;Element(s);Description;Value
onabort;HTML elements;abort event handler;Event handler content attribute
onautocomplete;HTML elements;autocomplete event handler;Event handler content attribute
onautocompleteerror;HTML elements;autocompleteerror event handler;Event handler content attribute
onafterprint;body;afterprint event handler for Window object;Event handler content attribute
onbeforeprint;body;beforeprint event handler for Window object;Event handler content attribute
onbeforeunload;body;beforeunload event handler for Window object;Event handler content attribute
onblur;HTML elements;blur event handler;Event handler content attribute
oncancel;HTML elements;cancel event handler;Event handler content attribute
oncanplay;HTML elements;canplay event handler;Event handler content attribute
oncanplaythrough;HTML elements;canplaythrough event handler;Event handler content attribute
onchange;HTML elements;change event handler;Event handler content attribute
onclick;HTML elements;click event handler;Event handler content attribute
onclose;HTML elements;close event handler;Event handler content attribute
oncontextmenu;HTML elements;contextmenu event handler;Event handler content attribute
oncuechange;HTML elements;cuechange event handler;Event handler content attribute
ondblclick;HTML elements;dblclick event handler;Event handler content attribute
ondrag;HTML elements;drag event handler;Event handler content attribute
ondragend;HTML elements;dragend event handler;Event handler content attribute
ondragenter;HTML elements;dragenter event handler;Event handler content attribute
ondragexit;HTML elements;dragexit event handler;Event handler content attribute
ondragleave;HTML elements;dragleave event handler;Event handler content attribute
ondragover;HTML elements;dragover event handler;Event handler content attribute
ondragstart;HTML elements;dragstart event handler;Event handler content attribute
ondrop;HTML elements;drop event handler;Event handler content attribute
ondurationchange;HTML elements;durationchange event handler;Event handler content attribute
onemptied;HTML elements;emptied event handler;Event handler content attribute
onended;HTML elements;ended event handler;Event handler content attribute
onerror;HTML elements;error event handler;Event handler content attribute
onfocus;HTML elements;focus event handler;Event handler content attribute
onhashchange;body;hashchange event handler for Window object;Event handler content attribute
oninput;HTML elements;input event handler;Event handler content attribute
oninvalid;HTML elements;invalid event handler;Event handler content attribute
onkeydown;HTML elements;keydown event handler;Event handler content attribute
onkeypress;HTML elements;keypress event handler;Event handler content attribute
onkeyup;HTML elements;keyup event handler;Event handler content attribute
onlanguagechange;body;languagechange event handler for Window object;Event handler content attribute
onload;HTML elements;load event handler;Event handler content attribute
onloadeddata;HTML elements;loadeddata event handler;Event handler content attribute
onloadedmetadata;HTML elements;loadedmetadata event handler;Event handler content attribute
onloadstart;HTML elements;loadstart event handler;Event handler content attribute
onmessage;body;message event handler for Window object;Event handler content attribute
onmousedown;HTML elements;mousedown event handler;Event handler content attribute
onmouseenter;HTML elements;mouseenter event handler;Event handler content attribute
onmouseleave;HTML elements;mouseleave event handler;Event handler content attribute
onmousemove;HTML elements;mousemove event handler;Event handler content attribute
onmouseout;HTML elements;mouseout event handler;Event handler content attribute
onmouseover;HTML elements;mouseover event handler;Event handler content attribute
onmouseup;HTML elements;mouseup event handler;Event handler content attribute
onwheel;HTML elements;wheel event handler;Event handler content attribute
onoffline;body;offline event handler for Window object;Event handler content attribute
ononline;body;online event handler for Window object;Event handler content attribute
onpagehide;body;pagehide event handler for Window object;Event handler content attribute
onpageshow;body;pageshow event handler for Window object;Event handler content attribute
onpause;HTML elements;pause event handler;Event handler content attribute
onplay;HTML elements;play event handler;Event handler content attribute
onplaying;HTML elements;playing event handler;Event handler content attribute
onpopstate;body;popstate event handler for Window object;Event handler content attribute
onprogress;HTML elements;progress event handler;Event handler content attribute
onratechange;HTML elements;ratechange event handler;Event handler content attribute
onreset;HTML elements;reset event handler;Event handler content attribute
onresize;HTML elements;resize event handler;Event handler content attribute
onscroll;HTML elements;scroll event handler;Event handler content attribute
onseeked;HTML elements;seeked event handler;Event handler content attribute
onseeking;HTML elements;seeking event handler;Event handler content attribute
onselect;HTML elements;select event handler;Event handler content attribute
onshow;HTML elements;show event handler;Event handler content attribute
onsort;HTML elements;sort event handler;Event handler content attribute
onstalled;HTML elements;stalled event handler;Event handler content attribute
onstorage;body;storage event handler for Window object;Event handler content attribute
onsubmit;HTML elements;submit event handler;Event handler content attribute
onsuspend;HTML elements;suspend event handler;Event handler content attribute
ontimeupdate;HTML elements;timeupdate event handler;Event handler content attribute
ontoggle;HTML elements;toggle event handler;Event handler content attribute
onunload;body;unload event handler for Window object;Event handler content attribute
onvolumechange;HTML elements;volumechange event handler;Event handler content attribute
onwaiting;HTML elements;waiting event handler;Event handler content attribute"""

reader = csv.reader(htmlCsvAttributeData.split("\n"), delimiter=";", quotechar='"')
for row in reader:
    print "\t".join(row)