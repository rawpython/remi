#the following list contains all html standard attributes with description and a list of applicable html tags
#source http://www.w3.org/html/wg/drafts/html/master/index.html#attributes-1

"""<tr><th> <code>abbr</code>
     </th><td> <code id="attributes-3:attr-th-abbr"><a href="semantics.html#attr-th-abbr">th</a></code>
     </td><td> Alternative label to use for the header cell when referencing the cell in other contexts
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>accept</code>
     </th><td> <code id="attributes-3:attr-input-accept"><a href="semantics.html#attr-input-accept">input</a></code>
     </td><td> Hint for expected file type in <a href="semantics.html#file-upload-state-(type=file)" id="attributes-3:file-upload-state-(type=file)">file upload controls</a>
     </td><td> <a href="infrastructure.html#set-of-comma-separated-tokens" id="attributes-3:set-of-comma-separated-tokens">Set of comma-separated tokens</a>* consisting of <a href="infrastructure.html#valid-mime-type" id="attributes-3:valid-mime-type">valid MIME types with no parameters</a> or <code>audio/*</code>, <code>video/*</code>, or <code>image/*</code>
    </td></tr><tr><th> <code>accept-charset</code>
     </th><td> <code id="attributes-3:attr-form-accept-charset"><a href="semantics.html#attr-form-accept-charset">form</a></code>
     </td><td> Character encodings to use for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2">form submission</a>
     </td><td> <a href="infrastructure.html#ordered-set-of-unique-space-separated-tokens" id="attributes-3:ordered-set-of-unique-space-separated-tokens">Ordered set of unique space-separated tokens</a>, <a href="infrastructure.html#ascii-case-insensitive" id="attributes-3:ascii-case-insensitive">ASCII case-insensitive</a>, consisting of <a href="https://encoding.spec.whatwg.org/#label" id="attributes-3:encoding-label" data-x-internal="encoding-label">labels</a> of <a href="infrastructure.html#ascii-compatible-encoding" id="attributes-3:ascii-compatible-encoding">ASCII-compatible encodings</a>*
    </td></tr><tr><th> <code>accesskey</code>
     </th><td> <a href="editing.html#the-accesskey-attribute" id="attributes-3:the-accesskey-attribute">HTML elements</a>
     </td><td> Keyboard shortcut to activate or focus element
     </td><td> <a href="infrastructure.html#ordered-set-of-unique-space-separated-tokens" id="attributes-3:ordered-set-of-unique-space-separated-tokens-2">Ordered set of unique space-separated tokens</a>, <a href="infrastructure.html#case-sensitive" id="attributes-3:case-sensitive">case-sensitive</a>, consisting of one Unicode code point in length
    </td></tr><tr><th> <code>action</code>
     </th><td> <code id="attributes-3:attr-fs-action"><a href="semantics.html#attr-fs-action">form</a></code>
     </td><td> <a href="infrastructure.html#url" id="attributes-3:url">URL</a> to use for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-2">form submission</a>
     </td><td> <a href="infrastructure.html#valid-non-empty-url-potentially-surrounded-by-spaces" id="attributes-3:valid-non-empty-url-potentially-surrounded-by-spaces">Valid non-empty URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>allowfullscreen</code>
     </th><td> <code id="attributes-3:attr-iframe-allowfullscreen"><a href="semantics.html#attr-iframe-allowfullscreen">iframe</a></code>
     </td><td> Whether to allow the <code id="attributes-3:the-iframe-element"><a href="semantics.html#the-iframe-element">iframe</a></code>'s contents to use <code id="attributes-3:dom-element-requestfullscreen"><a href="infrastructure.html#dom-element-requestfullscreen">requestFullscreen()</a></code>
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute">Boolean attribute</a>
    </td></tr><tr><th> <code>alt</code>
     </th><td> <code id="attributes-3:attr-area-alt"><a href="semantics.html#attr-area-alt">area</a></code>;
          <code id="attributes-3:attr-img-alt"><a href="semantics.html#attr-img-alt">img</a></code>;
          <code id="attributes-3:attr-input-alt"><a href="semantics.html#attr-input-alt">input</a></code>
     </td><td> Replacement text for use when images are not available
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>async</code>
     </th><td> <code id="attributes-3:attr-script-async"><a href="semantics.html#attr-script-async">script</a></code>
     </td><td> Execute script when available, without blocking
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-2">Boolean attribute</a>
    </td></tr><tr><th> <code>autocomplete</code>
     </th><td> <code id="attributes-3:attr-form-autocomplete"><a href="semantics.html#attr-form-autocomplete">form</a></code>
     </td><td> Default setting for autofill feature for controls in the form
     </td><td> "<code>on</code>"; "<code>off</code>"
    </td></tr><tr><th> <code>autocomplete</code>
     </th><td> <code id="attributes-3:attr-fe-autocomplete"><a href="semantics.html#attr-fe-autocomplete">input</a></code>;
          <code id="attributes-3:attr-fe-autocomplete-2"><a href="semantics.html#attr-fe-autocomplete">select</a></code>;
          <code id="attributes-3:attr-fe-autocomplete-3"><a href="semantics.html#attr-fe-autocomplete">textarea</a></code>
     </td><td> Hint for form autofill feature
     </td><td> <a href="semantics.html#autofill-field" id="attributes-3:autofill-field">Autofill field</a> name and related tokens*
    </td></tr><tr><th> <code>autofocus</code>
     </th><td> <code id="attributes-3:attr-fe-autofocus"><a href="semantics.html#attr-fe-autofocus">button</a></code>;
          <code id="attributes-3:attr-fe-autofocus-2"><a href="semantics.html#attr-fe-autofocus">input</a></code>;
          <code id="attributes-3:attr-fe-autofocus-3"><a href="semantics.html#attr-fe-autofocus">keygen</a></code>;
          <code id="attributes-3:attr-fe-autofocus-4"><a href="semantics.html#attr-fe-autofocus">select</a></code>;
          <code id="attributes-3:attr-fe-autofocus-5"><a href="semantics.html#attr-fe-autofocus">textarea</a></code>
     </td><td> Automatically focus the form control when the page is loaded
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-3">Boolean attribute</a>
    </td></tr><tr><th> <code>autoplay</code>
     </th><td> <code id="attributes-3:attr-media-autoplay"><a href="semantics.html#attr-media-autoplay">audio</a></code>;
          <code id="attributes-3:attr-media-autoplay-2"><a href="semantics.html#attr-media-autoplay">video</a></code>
     </td><td> Hint that the <a href="semantics.html#media-resource" id="attributes-3:media-resource">media resource</a> can be started automatically when the page is loaded
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-4">Boolean attribute</a>
    </td></tr><tr><th> <code>challenge</code>
     </th><td> <code id="attributes-3:attr-keygen-challenge"><a href="semantics.html#attr-keygen-challenge">keygen</a></code>
     </td><td> String to package with the generated and signed public key
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>charset</code>
     </th><td> <code id="attributes-3:attr-meta-charset"><a href="semantics.html#attr-meta-charset">meta</a></code>
     </td><td> <a href="semantics.html#character-encoding-declaration" id="attributes-3:character-encoding-declaration">Character encoding declaration</a>
     </td><td> <a id="attributes-3:encoding-label-2" href="https://encoding.spec.whatwg.org/#label" data-x-internal="encoding-label">Encoding label</a>*
    </td></tr><tr><th> <code>charset</code>
     </th><td> <code id="attributes-3:attr-script-charset"><a href="semantics.html#attr-script-charset">script</a></code>
     </td><td> Character encoding of the external script resource
     </td><td> <a id="attributes-3:encoding-label-3" href="https://encoding.spec.whatwg.org/#label" data-x-internal="encoding-label">Encoding label</a>*
    </td></tr><tr><th> <code>checked</code>
     </th><td> <code id="attributes-3:attr-menuitem-checked"><a href="semantics.html#attr-menuitem-checked">menuitem</a></code>;
          <code id="attributes-3:attr-input-checked"><a href="semantics.html#attr-input-checked">input</a></code>
     </td><td> Whether the command or control is checked
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-5">Boolean attribute</a>
    </td></tr><tr><th> <code>cite</code>
     </th><td> <code id="attributes-3:attr-blockquote-cite"><a href="semantics.html#attr-blockquote-cite">blockquote</a></code>;
          <code id="attributes-3:attr-mod-cite"><a href="semantics.html#attr-mod-cite">del</a></code>;
          <code id="attributes-3:attr-mod-cite-2"><a href="semantics.html#attr-mod-cite">ins</a></code>;
          <code id="attributes-3:attr-q-cite"><a href="semantics.html#attr-q-cite">q</a></code>
     </td><td> Link to the source of the quotation or more information about the edit
     </td><td> <a href="infrastructure.html#valid-url-potentially-surrounded-by-spaces" id="attributes-3:valid-url-potentially-surrounded-by-spaces">Valid URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>class</code>
     </th><td> <a href="dom.html#classes" id="attributes-3:classes">HTML elements</a>
     </td><td> Classes to which the element belongs
     </td><td> <a href="infrastructure.html#set-of-space-separated-tokens" id="attributes-3:set-of-space-separated-tokens">Set of space-separated tokens</a>
    </td></tr><tr><th> <code>cols</code>
     </th><td> <code id="attributes-3:attr-textarea-cols"><a href="semantics.html#attr-textarea-cols">textarea</a></code>
     </td><td> Maximum number of characters per line
     </td><td> <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer">Valid non-negative integer</a> greater than zero
    </td></tr><tr><th> <code>colspan</code>
     </th><td> <code id="attributes-3:attr-tdth-colspan"><a href="semantics.html#attr-tdth-colspan">td</a></code>;
          <code id="attributes-3:attr-tdth-colspan-2"><a href="semantics.html#attr-tdth-colspan">th</a></code>
     </td><td> Number of columns that the cell is to span
     </td><td> <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-2">Valid non-negative integer</a> greater than zero
    </td></tr><tr><th> <code>command</code>
     </th><td> <code id="attributes-3:attr-menuitem-command"><a href="semantics.html#attr-menuitem-command">menuitem</a></code>
     </td><td> Command definition
     </td><td> <a href="infrastructure.html#concept-id" id="attributes-3:concept-id">ID</a>*
    </td></tr><tr><th> <code>content</code>
     </th><td> <code id="attributes-3:attr-meta-content"><a href="semantics.html#attr-meta-content">meta</a></code>
     </td><td> Value of the element
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>contenteditable</code>
     </th><td> <a href="editing.html#attr-contenteditable" id="attributes-3:attr-contenteditable">HTML elements</a>
     </td><td> Whether the element is editable
     </td><td> "<code>true</code>"; "<code>false</code>"
    </td></tr><tr><th> <code>contextmenu</code>
     </th><td> <a href="semantics.html#attr-contextmenu" id="attributes-3:attr-contextmenu">HTML elements</a>
     </td><td> The element's context menu
     </td><td> <a href="infrastructure.html#concept-id" id="attributes-3:concept-id-2">ID</a>*
    </td></tr><tr><th> <code>controls</code>
     </th><td> <code id="attributes-3:attr-media-controls"><a href="semantics.html#attr-media-controls">audio</a></code>;
          <code id="attributes-3:attr-media-controls-2"><a href="semantics.html#attr-media-controls">video</a></code>
     </td><td> Show user agent controls
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-6">Boolean attribute</a>
    </td></tr><tr><th> <code>coords</code>
     </th><td> <code id="attributes-3:attr-area-coords"><a href="semantics.html#attr-area-coords">area</a></code>
     </td><td> Coordinates for the shape to be created in an <a href="semantics.html#image-map" id="attributes-3:image-map">image map</a>
     </td><td> <a href="infrastructure.html#valid-list-of-integers" id="attributes-3:valid-list-of-integers">Valid list of integers</a>*
    </td></tr><tr><th> <code>crossorigin</code>
     </th><td> <code id="attributes-3:attr-media-crossorigin"><a href="semantics.html#attr-media-crossorigin">audio</a></code>;
          <code id="attributes-3:attr-img-crossorigin"><a href="semantics.html#attr-img-crossorigin">img</a></code>;
          <code id="attributes-3:attr-link-crossorigin"><a href="semantics.html#attr-link-crossorigin">link</a></code>;
          <code id="attributes-3:attr-script-crossorigin"><a href="semantics.html#attr-script-crossorigin">script</a></code>;
          <code id="attributes-3:attr-media-crossorigin-2"><a href="semantics.html#attr-media-crossorigin">video</a></code>
     </td><td> How the element handles crossorigin requests
     </td><td> "<code id="attributes-3:attr-crossorigin-anonymous-keyword"><a href="infrastructure.html#attr-crossorigin-anonymous-keyword">anonymous</a></code>"; "<code id="attributes-3:attr-crossorigin-use-credentials-keyword"><a href="infrastructure.html#attr-crossorigin-use-credentials-keyword">use-credentials</a></code>"
    </td></tr><tr><th> <code>data</code>
     </th><td> <code id="attributes-3:attr-object-data"><a href="semantics.html#attr-object-data">object</a></code>
     </td><td> Address of the resource
     </td><td> <a href="infrastructure.html#valid-non-empty-url-potentially-surrounded-by-spaces" id="attributes-3:valid-non-empty-url-potentially-surrounded-by-spaces-2">Valid non-empty URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>datetime</code>
     </th><td> <code id="attributes-3:attr-mod-datetime"><a href="semantics.html#attr-mod-datetime">del</a></code>;
          <code id="attributes-3:attr-mod-datetime-2"><a href="semantics.html#attr-mod-datetime">ins</a></code>
     </td><td> Date and (optionally) time of the change
     </td><td> <a href="infrastructure.html#valid-date-string-with-optional-time" id="attributes-3:valid-date-string-with-optional-time">Valid date string with optional time</a>
    </td></tr><tr><th> <code>datetime</code>
     </th><td> <code id="attributes-3:attr-time-datetime"><a href="semantics.html#attr-time-datetime">time</a></code>
     </td><td> Machine-readable value
     </td><td> <a href="infrastructure.html#valid-month-string" id="attributes-3:valid-month-string">Valid month string</a>,
          <a href="infrastructure.html#valid-date-string" id="attributes-3:valid-date-string">valid date string</a>,
          <a href="infrastructure.html#valid-yearless-date-string" id="attributes-3:valid-yearless-date-string">valid yearless date string</a>,
          <a href="infrastructure.html#valid-time-string" id="attributes-3:valid-time-string">valid time string</a>,
          <a href="infrastructure.html#valid-local-date-and-time-string" id="attributes-3:valid-local-date-and-time-string">valid local date and time string</a>,
          <a href="infrastructure.html#valid-time-zone-offset-string" id="attributes-3:valid-time-zone-offset-string">valid time-zone offset string</a>,
          <a href="infrastructure.html#valid-global-date-and-time-string" id="attributes-3:valid-global-date-and-time-string">valid global date and time string</a>,
          <a href="infrastructure.html#valid-week-string" id="attributes-3:valid-week-string">valid week string</a>,
          <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-3">valid non-negative integer</a>, or
          <a href="infrastructure.html#valid-duration-string" id="attributes-3:valid-duration-string">valid duration string</a>
    </td></tr><tr><th> <code>default</code>
     </th><td> <code id="attributes-3:attr-menuitem-default"><a href="semantics.html#attr-menuitem-default">menuitem</a></code>
     </td><td> Mark the command as being a default command
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-7">Boolean attribute</a>
    </td></tr><tr><th> <code>default</code>
     </th><td> <code id="attributes-3:attr-track-default"><a href="semantics.html#attr-track-default">track</a></code>
     </td><td> Enable the track if no other <a href="semantics.html#text-track" id="attributes-3:text-track">text track</a> is more suitable
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-8">Boolean attribute</a>
    </td></tr><tr><th> <code>defer</code>
     </th><td> <code id="attributes-3:attr-script-defer"><a href="semantics.html#attr-script-defer">script</a></code>
     </td><td> Defer script execution
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-9">Boolean attribute</a>
    </td></tr><tr><th> <code>dir</code>
     </th><td> <a href="dom.html#the-dir-attribute" id="attributes-3:the-dir-attribute">HTML elements</a>
     </td><td> <a href="dom.html#the-directionality" id="attributes-3:the-directionality">The text directionality</a> of the element
     </td><td> "<code id="attributes-3:attr-dir-ltr"><a href="dom.html#attr-dir-ltr">ltr</a></code>"; "<code id="attributes-3:attr-dir-rtl"><a href="dom.html#attr-dir-rtl">rtl</a></code>"; "<code id="attributes-3:attr-dir-auto"><a href="dom.html#attr-dir-auto">auto</a></code>"
    </td></tr><tr><th> <code>dir</code>
     </th><td> <code id="attributes-3:the-bdo-element"><a href="semantics.html#the-bdo-element">bdo</a></code>
     </td><td> <a href="dom.html#the-directionality" id="attributes-3:the-directionality-2">The text directionality</a> of the element
     </td><td> "<code id="attributes-3:attr-dir-ltr-2"><a href="dom.html#attr-dir-ltr">ltr</a></code>"; "<code id="attributes-3:attr-dir-rtl-2"><a href="dom.html#attr-dir-rtl">rtl</a></code>"
    </td></tr><tr><th> <code>dirname</code>
     </th><td> <code id="attributes-3:attr-fe-dirname"><a href="semantics.html#attr-fe-dirname">input</a></code>;
          <code id="attributes-3:attr-fe-dirname-2"><a href="semantics.html#attr-fe-dirname">textarea</a></code>
     </td><td> Name of form field to use for sending the element's <a href="dom.html#the-directionality" id="attributes-3:the-directionality-3">directionality</a> in <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-3">form submission</a>
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>disabled</code>
     </th><td> <code id="attributes-3:attr-fe-disabled"><a href="semantics.html#attr-fe-disabled">button</a></code>;
          <code id="attributes-3:attr-menuitem-disabled"><a href="semantics.html#attr-menuitem-disabled">menuitem</a></code>;
          <code id="attributes-3:attr-fieldset-disabled"><a href="semantics.html#attr-fieldset-disabled">fieldset</a></code>;
          <code id="attributes-3:attr-fe-disabled-2"><a href="semantics.html#attr-fe-disabled">input</a></code>;
          <code id="attributes-3:attr-fe-disabled-3"><a href="semantics.html#attr-fe-disabled">keygen</a></code>;
          <code id="attributes-3:attr-optgroup-disabled"><a href="semantics.html#attr-optgroup-disabled">optgroup</a></code>;
          <code id="attributes-3:attr-option-disabled"><a href="semantics.html#attr-option-disabled">option</a></code>;
          <code id="attributes-3:attr-fe-disabled-4"><a href="semantics.html#attr-fe-disabled">select</a></code>;
          <code id="attributes-3:attr-fe-disabled-5"><a href="semantics.html#attr-fe-disabled">textarea</a></code>
     </td><td> Whether the form control is disabled
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-10">Boolean attribute</a>
    </td></tr><tr><th> <code>download</code>
     </th><td> <code id="attributes-3:attr-hyperlink-download"><a href="semantics.html#attr-hyperlink-download">a</a></code>;
          <code id="attributes-3:attr-hyperlink-download-2"><a href="semantics.html#attr-hyperlink-download">area</a></code>
     </td><td> Whether to download the resource instead of navigating to it, and its file name if so
     </td><td> Text
    </td></tr><tr><th> <code>draggable</code>
     </th><td> <a href="editing.html#the-draggable-attribute" id="attributes-3:the-draggable-attribute">HTML elements</a>
     </td><td> Whether the element is draggable
     </td><td> "<code>true</code>"; "<code>false</code>"
    </td></tr><tr><th> <code>dropzone</code>
     </th><td> <a href="editing.html#the-dropzone-attribute" id="attributes-3:the-dropzone-attribute">HTML elements</a>
     </td><td> Accepted item types for drag-and-drop
     </td><td> <a href="infrastructure.html#unordered-set-of-unique-space-separated-tokens" id="attributes-3:unordered-set-of-unique-space-separated-tokens">Unordered set of unique space-separated tokens</a>, <a href="infrastructure.html#ascii-case-insensitive" id="attributes-3:ascii-case-insensitive-2">ASCII case-insensitive</a>, consisting of accepted types and drag feedback*
    </td></tr><tr><th> <code>enctype</code>
     </th><td> <code id="attributes-3:attr-fs-enctype"><a href="semantics.html#attr-fs-enctype">form</a></code>
     </td><td> Form data set encoding type to use for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-4">form submission</a>
     </td><td> "<code id="attributes-3:attr-fs-enctype-urlencoded"><a href="semantics.html#attr-fs-enctype-urlencoded">application/x-www-form-urlencoded</a></code>"; "<code id="attributes-3:attr-fs-enctype-formdata"><a href="semantics.html#attr-fs-enctype-formdata">multipart/form-data</a></code>"; "<code id="attributes-3:attr-fs-enctype-text"><a href="semantics.html#attr-fs-enctype-text">text/plain</a></code>"
    </td></tr><tr><th> <code>for</code>
     </th><td> <code id="attributes-3:attr-label-for"><a href="semantics.html#attr-label-for">label</a></code>
     </td><td> Associate the label with form control
     </td><td> <a href="infrastructure.html#concept-id" id="attributes-3:concept-id-3">ID</a>*
    </td></tr><tr><th> <code>for</code>
     </th><td> <code id="attributes-3:attr-output-for"><a href="semantics.html#attr-output-for">output</a></code>
     </td><td> Specifies controls from which the output was calculated
     </td><td> <a href="infrastructure.html#unordered-set-of-unique-space-separated-tokens" id="attributes-3:unordered-set-of-unique-space-separated-tokens-2">Unordered set of unique space-separated tokens</a>, <a href="infrastructure.html#case-sensitive" id="attributes-3:case-sensitive-2">case-sensitive</a>, consisting of IDs*
    </td></tr><tr><th> <code>form</code>
     </th><td> <code id="attributes-3:attr-fae-form"><a href="semantics.html#attr-fae-form">button</a></code>;
          <code id="attributes-3:attr-fae-form-2"><a href="semantics.html#attr-fae-form">fieldset</a></code>;
          <code id="attributes-3:attr-fae-form-3"><a href="semantics.html#attr-fae-form">input</a></code>;
          <code id="attributes-3:attr-fae-form-4"><a href="semantics.html#attr-fae-form">keygen</a></code>;
          <code id="attributes-3:attr-fae-form-5"><a href="semantics.html#attr-fae-form">label</a></code>;
          <code id="attributes-3:attr-fae-form-6"><a href="semantics.html#attr-fae-form">object</a></code>;
          <code id="attributes-3:attr-fae-form-7"><a href="semantics.html#attr-fae-form">output</a></code>;
          <code id="attributes-3:attr-fae-form-8"><a href="semantics.html#attr-fae-form">select</a></code>;
          <code id="attributes-3:attr-fae-form-9"><a href="semantics.html#attr-fae-form">textarea</a></code>
     </td><td> Associates the control with a <code id="attributes-3:the-form-element"><a href="semantics.html#the-form-element">form</a></code> element
     </td><td> <a href="infrastructure.html#concept-id" id="attributes-3:concept-id-4">ID</a>*
    </td></tr><tr><th> <code>formaction</code>
     </th><td> <code id="attributes-3:attr-fs-formaction"><a href="semantics.html#attr-fs-formaction">button</a></code>;
          <code id="attributes-3:attr-fs-formaction-2"><a href="semantics.html#attr-fs-formaction">input</a></code>
     </td><td> <a href="infrastructure.html#url" id="attributes-3:url-2">URL</a> to use for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-5">form submission</a>
     </td><td> <a href="infrastructure.html#valid-non-empty-url-potentially-surrounded-by-spaces" id="attributes-3:valid-non-empty-url-potentially-surrounded-by-spaces-3">Valid non-empty URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>formenctype</code>
     </th><td> <code id="attributes-3:attr-fs-formenctype"><a href="semantics.html#attr-fs-formenctype">button</a></code>;
          <code id="attributes-3:attr-fs-formenctype-2"><a href="semantics.html#attr-fs-formenctype">input</a></code>
     </td><td> Form data set encoding type to use for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-6">form submission</a>
     </td><td> "<code id="attributes-3:attr-fs-enctype-urlencoded-2"><a href="semantics.html#attr-fs-enctype-urlencoded">application/x-www-form-urlencoded</a></code>"; "<code id="attributes-3:attr-fs-enctype-formdata-2"><a href="semantics.html#attr-fs-enctype-formdata">multipart/form-data</a></code>"; "<code id="attributes-3:attr-fs-enctype-text-2"><a href="semantics.html#attr-fs-enctype-text">text/plain</a></code>"
    </td></tr><tr><th> <code>formmethod</code>
     </th><td> <code id="attributes-3:attr-fs-formmethod"><a href="semantics.html#attr-fs-formmethod">button</a></code>;
          <code id="attributes-3:attr-fs-formmethod-2"><a href="semantics.html#attr-fs-formmethod">input</a></code>
     </td><td> HTTP method to use for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-7">form submission</a>
     </td><td> "<code>GET</code>"; "<code>POST</code>"
    </td></tr><tr><th> <code>formnovalidate</code>
     </th><td> <code id="attributes-3:attr-fs-formnovalidate"><a href="semantics.html#attr-fs-formnovalidate">button</a></code>;
          <code id="attributes-3:attr-fs-formnovalidate-2"><a href="semantics.html#attr-fs-formnovalidate">input</a></code>
     </td><td> Bypass form control validation for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-8">form submission</a>
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-11">Boolean attribute</a>
    </td></tr><tr><th> <code>formtarget</code>
     </th><td> <code id="attributes-3:attr-fs-formtarget"><a href="semantics.html#attr-fs-formtarget">button</a></code>;
          <code id="attributes-3:attr-fs-formtarget-2"><a href="semantics.html#attr-fs-formtarget">input</a></code>
     </td><td> <a href="browsers.html#browsing-context" id="attributes-3:browsing-context">Browsing context</a> for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-9">form submission</a>
     </td><td> <a href="browsers.html#valid-browsing-context-name-or-keyword" id="attributes-3:valid-browsing-context-name-or-keyword">Valid browsing context name or keyword</a>
    </td></tr><tr><th> <code>headers</code>
     </th><td> <code id="attributes-3:attr-tdth-headers"><a href="semantics.html#attr-tdth-headers">td</a></code>;
          <code id="attributes-3:attr-tdth-headers-2"><a href="semantics.html#attr-tdth-headers">th</a></code>
     </td><td> The header cells for this cell
     </td><td> <a href="infrastructure.html#unordered-set-of-unique-space-separated-tokens" id="attributes-3:unordered-set-of-unique-space-separated-tokens-3">Unordered set of unique space-separated tokens</a>, <a href="infrastructure.html#case-sensitive" id="attributes-3:case-sensitive-3">case-sensitive</a>, consisting of IDs*
    </td></tr><tr><th> <code>height</code>
     </th><td> <code id="attributes-3:attr-canvas-height"><a href="semantics.html#attr-canvas-height">canvas</a></code>;
          <code id="attributes-3:attr-dim-height"><a href="semantics.html#attr-dim-height">embed</a></code>;
          <code id="attributes-3:attr-dim-height-2"><a href="semantics.html#attr-dim-height">iframe</a></code>;
          <code id="attributes-3:attr-dim-height-3"><a href="semantics.html#attr-dim-height">img</a></code>;
          <code id="attributes-3:attr-dim-height-4"><a href="semantics.html#attr-dim-height">input</a></code>;
          <code id="attributes-3:attr-dim-height-5"><a href="semantics.html#attr-dim-height">object</a></code>;
          <code id="attributes-3:attr-dim-height-6"><a href="semantics.html#attr-dim-height">video</a></code>
     </td><td> Vertical dimension
     </td><td> <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-4">Valid non-negative integer</a>
    </td></tr><tr><th> <code>hidden</code>
     </th><td> <a href="editing.html#the-hidden-attribute" id="attributes-3:the-hidden-attribute">HTML elements</a>
     </td><td> Whether the element is relevant
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-12">Boolean attribute</a>
    </td></tr><tr><th> <code>high</code>
     </th><td> <code id="attributes-3:attr-meter-high"><a href="semantics.html#attr-meter-high">meter</a></code>
     </td><td> Low limit of high range
     </td><td> <a href="infrastructure.html#valid-floating-point-number" id="attributes-3:valid-floating-point-number">Valid floating-point number</a>*
    </td></tr><tr><th> <code>href</code>
     </th><td> <code id="attributes-3:attr-hyperlink-href"><a href="semantics.html#attr-hyperlink-href">a</a></code>;
          <code id="attributes-3:attr-hyperlink-href-2"><a href="semantics.html#attr-hyperlink-href">area</a></code>
     </td><td> Address of the <a href="semantics.html#hyperlink" id="attributes-3:hyperlink">hyperlink</a>
     </td><td> <a href="infrastructure.html#valid-url-potentially-surrounded-by-spaces" id="attributes-3:valid-url-potentially-surrounded-by-spaces-2">Valid URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>href</code>
     </th><td> <code id="attributes-3:attr-link-href"><a href="semantics.html#attr-link-href">link</a></code>
     </td><td> Address of the <a href="semantics.html#hyperlink" id="attributes-3:hyperlink-2">hyperlink</a>
     </td><td> <a href="infrastructure.html#valid-non-empty-url-potentially-surrounded-by-spaces" id="attributes-3:valid-non-empty-url-potentially-surrounded-by-spaces-4">Valid non-empty URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>href</code>
     </th><td> <code id="attributes-3:attr-base-href"><a href="semantics.html#attr-base-href">base</a></code>
     </td><td> <a href="infrastructure.html#document-base-url" id="attributes-3:document-base-url">Document base URL</a>
     </td><td> <a href="infrastructure.html#valid-url-potentially-surrounded-by-spaces" id="attributes-3:valid-url-potentially-surrounded-by-spaces-3">Valid URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>hreflang</code>
     </th><td> <code id="attributes-3:attr-hyperlink-hreflang"><a href="semantics.html#attr-hyperlink-hreflang">a</a></code>;
          <code id="attributes-3:attr-hyperlink-hreflang-2"><a href="semantics.html#attr-hyperlink-hreflang">area</a></code>;
          <code id="attributes-3:attr-link-hreflang"><a href="semantics.html#attr-link-hreflang">link</a></code>
     </td><td> Language of the linked resource
     </td><td> Valid BCP 47 language tag
    </td></tr><tr><th> <code>http-equiv</code>
     </th><td> <code id="attributes-3:attr-meta-http-equiv"><a href="semantics.html#attr-meta-http-equiv">meta</a></code>
     </td><td> Pragma directive
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>icon</code>
     </th><td> <code id="attributes-3:attr-menuitem-icon"><a href="semantics.html#attr-menuitem-icon">menuitem</a></code>
     </td><td> Icon for the command
     </td><td> <a href="infrastructure.html#valid-non-empty-url-potentially-surrounded-by-spaces" id="attributes-3:valid-non-empty-url-potentially-surrounded-by-spaces-5">Valid non-empty URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>id</code>
     </th><td> <a href="dom.html#the-id-attribute" id="attributes-3:the-id-attribute">HTML elements</a>
     </td><td> The element's <a href="infrastructure.html#concept-id" id="attributes-3:concept-id-5">ID</a>
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>inputmode</code>
     </th><td> <code id="attributes-3:attr-fe-inputmode"><a href="semantics.html#attr-fe-inputmode">input</a></code>;
          <code id="attributes-3:attr-fe-inputmode-2"><a href="semantics.html#attr-fe-inputmode">textarea</a></code>
     </td><td> Hint for selecting an input modality
     </td><td> "<code id="attributes-3:attr-fe-inputmode-keyword-verbatim"><a href="semantics.html#attr-fe-inputmode-keyword-verbatim">verbatim</a></code>";
          "<code id="attributes-3:attr-fe-inputmode-keyword-latin"><a href="semantics.html#attr-fe-inputmode-keyword-latin">latin</a></code>";
          "<code id="attributes-3:attr-fe-inputmode-keyword-latin-name"><a href="semantics.html#attr-fe-inputmode-keyword-latin-name">latin-name</a></code>";
          "<code id="attributes-3:attr-fe-inputmode-keyword-latin-prose"><a href="semantics.html#attr-fe-inputmode-keyword-latin-prose">latin-prose</a></code>";
          "<code id="attributes-3:attr-fe-inputmode-keyword-full-width-latin"><a href="semantics.html#attr-fe-inputmode-keyword-full-width-latin">full-width-latin</a></code>";
          "<code id="attributes-3:attr-fe-inputmode-keyword-kana"><a href="semantics.html#attr-fe-inputmode-keyword-kana">kana</a></code>";
          "<code id="attributes-3:attr-fe-inputmode-keyword-kana-name"><a href="semantics.html#attr-fe-inputmode-keyword-kana-name">kana-name</a></code>";
          "<code id="attributes-3:attr-fe-inputmode-keyword-katakana"><a href="semantics.html#attr-fe-inputmode-keyword-katakana">katakana</a></code>";
          
          "<code id="attributes-3:attr-fe-inputmode-keyword-numeric"><a href="semantics.html#attr-fe-inputmode-keyword-numeric">numeric</a></code>";
          "<code id="attributes-3:attr-fe-inputmode-keyword-tel"><a href="semantics.html#attr-fe-inputmode-keyword-tel">tel</a></code>";
          "<code id="attributes-3:attr-fe-inputmode-keyword-email"><a href="semantics.html#attr-fe-inputmode-keyword-email">email</a></code>";
          "<code id="attributes-3:attr-fe-inputmode-keyword-url"><a href="semantics.html#attr-fe-inputmode-keyword-url">url</a></code>"
    </td></tr><tr><th> <code>ismap</code>
     </th><td> <code id="attributes-3:attr-img-ismap"><a href="semantics.html#attr-img-ismap">img</a></code>
     </td><td> Whether the image is a server-side image map
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-13">Boolean attribute</a>
    </td></tr><tr><th> <code>itemid</code>
     </th><td> <a href="http://www.w3.org/TR/microdata/#attr-itemid" id="attributes-3:attr-itemid">HTML elements</a>
     </td><td> <a href="http://www.w3.org/TR/microdata/#global-identifier" id="attributes-3:global-identifier">Global identifier</a> for a microdata item
     </td><td> <a href="infrastructure.html#valid-url-potentially-surrounded-by-spaces" id="attributes-3:valid-url-potentially-surrounded-by-spaces-4">Valid URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>itemprop</code>
     </th><td> <a href="http://www.w3.org/TR/microdata/#attr-itemprop" id="attributes-3:names:-the-itemprop-attribute">HTML elements</a>
     </td><td> <a href="http://www.w3.org/TR/microdata/#property-names" id="attributes-3:property-names">Property names</a> of a microdata item
     </td><td> <a href="infrastructure.html#unordered-set-of-unique-space-separated-tokens" id="attributes-3:unordered-set-of-unique-space-separated-tokens-4">Unordered set of unique space-separated tokens</a>, <a href="infrastructure.html#case-sensitive" id="attributes-3:case-sensitive-4">case-sensitive</a>, consisting of <a href="infrastructure.html#absolute-url" id="attributes-3:absolute-url">valid absolute URLs</a>, <a href="http://www.w3.org/TR/microdata/#defined-property-name" id="attributes-3:defined-property-name">defined property names</a>, or text*
    </td></tr><tr><th> <code>itemref</code>
     </th><td> <a href="http://www.w3.org/TR/microdata/#attr-itemref" id="attributes-3:attr-itemref">HTML elements</a>
     </td><td> Referenced elements
     </td><td> <a href="infrastructure.html#unordered-set-of-unique-space-separated-tokens" id="attributes-3:unordered-set-of-unique-space-separated-tokens-5">Unordered set of unique space-separated tokens</a>, <a href="infrastructure.html#case-sensitive" id="attributes-3:case-sensitive-5">case-sensitive</a>, consisting of IDs*
    </td></tr><tr><th> <code>itemscope</code>
     </th><td> <a href="http://www.w3.org/TR/microdata/#attr-itemscope" id="attributes-3:attr-itemscope">HTML elements</a>
     </td><td> Introduces a microdata item
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-14">Boolean attribute</a>
    </td></tr><tr><th> <code>itemtype</code>
     </th><td> <a href="http://www.w3.org/TR/microdata/#attr-itemtype" id="attributes-3:attr-itemtype">HTML elements</a>
     </td><td> <a href="http://www.w3.org/TR/microdata/#item-types" id="attributes-3:item-types">Item types</a> of a microdata item
     </td><td> <a href="infrastructure.html#unordered-set-of-unique-space-separated-tokens" id="attributes-3:unordered-set-of-unique-space-separated-tokens-6">Unordered set of unique space-separated tokens</a>, <a href="infrastructure.html#case-sensitive" id="attributes-3:case-sensitive-6">case-sensitive</a>, consisting of <a href="infrastructure.html#absolute-url" id="attributes-3:absolute-url-2">valid absolute URL</a>*
    </td></tr><tr><th> <code>keytype</code>
     </th><td> <code id="attributes-3:attr-keygen-keytype"><a href="semantics.html#attr-keygen-keytype">keygen</a></code>
     </td><td> The type of cryptographic key to generate
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>kind</code>
     </th><td> <code id="attributes-3:attr-track-kind"><a href="semantics.html#attr-track-kind">track</a></code>
     </td><td> The type of text track
     </td><td> "<code id="attributes-3:attr-track-kind-subtitles"><a href="semantics.html#attr-track-kind-subtitles">subtitles</a></code>";
          "<code id="attributes-3:attr-track-kind-captions"><a href="semantics.html#attr-track-kind-captions">captions</a></code>";
          "<code id="attributes-3:attr-track-kind-descriptions"><a href="semantics.html#attr-track-kind-descriptions">descriptions</a></code>";
          "<code id="attributes-3:attr-track-kind-chapters"><a href="semantics.html#attr-track-kind-chapters">chapters</a></code>";
          "<code id="attributes-3:attr-track-kind-metadata"><a href="semantics.html#attr-track-kind-metadata">metadata</a></code>"
    </td></tr><tr><th> <code>label</code>
     </th><td> <code id="attributes-3:attr-menuitem-label"><a href="semantics.html#attr-menuitem-label">menuitem</a></code>;
          <code id="attributes-3:attr-menu-label"><a href="semantics.html#attr-menu-label">menu</a></code>;
          <code id="attributes-3:attr-optgroup-label"><a href="semantics.html#attr-optgroup-label">optgroup</a></code>;
          <code id="attributes-3:attr-option-label"><a href="semantics.html#attr-option-label">option</a></code>;
          <code id="attributes-3:attr-track-label"><a href="semantics.html#attr-track-label">track</a></code>
     </td><td> User-visible label
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>lang</code>
     </th><td> <a href="dom.html#attr-lang" id="attributes-3:attr-lang">HTML elements</a>
     </td><td> <a href="dom.html#language" id="attributes-3:language">Language</a> of the element
     </td><td> Valid BCP 47 language tag or the empty string
    </td></tr><tr><th> <code>list</code>
     </th><td> <code id="attributes-3:attr-input-list"><a href="semantics.html#attr-input-list">input</a></code>
     </td><td> List of autocomplete options
     </td><td> <a href="infrastructure.html#concept-id" id="attributes-3:concept-id-6">ID</a>*
    </td></tr><tr><th> <code>loop</code>
     </th><td> <code id="attributes-3:attr-media-loop"><a href="semantics.html#attr-media-loop">audio</a></code>;
          <code id="attributes-3:attr-media-loop-2"><a href="semantics.html#attr-media-loop">video</a></code>
     </td><td> Whether to loop the <a href="semantics.html#media-resource" id="attributes-3:media-resource-2">media resource</a>
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-15">Boolean attribute</a>
    </td></tr><tr><th> <code>low</code>
     </th><td> <code id="attributes-3:attr-meter-low"><a href="semantics.html#attr-meter-low">meter</a></code>
     </td><td> High limit of low range
     </td><td> <a href="infrastructure.html#valid-floating-point-number" id="attributes-3:valid-floating-point-number-2">Valid floating-point number</a>*
    </td></tr><tr><th> <code>manifest</code>
     </th><td> <code id="attributes-3:attr-html-manifest"><a href="semantics.html#attr-html-manifest">html</a></code>
     </td><td> <a href="browsers.html#concept-appcache-manifest" id="attributes-3:concept-appcache-manifest">Application cache manifest</a>
     </td><td> <a href="infrastructure.html#valid-non-empty-url-potentially-surrounded-by-spaces" id="attributes-3:valid-non-empty-url-potentially-surrounded-by-spaces-6">Valid non-empty URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>max</code>
     </th><td> <code id="attributes-3:attr-input-max"><a href="semantics.html#attr-input-max">input</a></code>
     </td><td> Maximum value
     </td><td> Varies*
    </td></tr><tr><th> <code>max</code>
     </th><td> <code id="attributes-3:attr-meter-max"><a href="semantics.html#attr-meter-max">meter</a></code>;
          <code id="attributes-3:attr-progress-max"><a href="semantics.html#attr-progress-max">progress</a></code>
     </td><td> Upper bound of range
     </td><td> <a href="infrastructure.html#valid-floating-point-number" id="attributes-3:valid-floating-point-number-3">Valid floating-point number</a>*
    </td></tr><tr><th> <code>maxlength</code>
     </th><td> <code id="attributes-3:attr-input-maxlength"><a href="semantics.html#attr-input-maxlength">input</a></code>;
          <code id="attributes-3:attr-textarea-maxlength"><a href="semantics.html#attr-textarea-maxlength">textarea</a></code>
     </td><td> Maximum length of value
     </td><td> <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-5">Valid non-negative integer</a>
    </td></tr><tr><th> <code>media</code>
     </th><td> <code id="attributes-3:attr-link-media"><a href="semantics.html#attr-link-media">link</a></code>;
          <code id="attributes-3:attr-style-media"><a href="semantics.html#attr-style-media">style</a></code>
     </td><td> Applicable media
     </td><td> <a href="infrastructure.html#valid-media-query-list" id="attributes-3:valid-media-query-list">Valid media query list</a>
    </td></tr><tr><th> <code>mediagroup</code>
     </th><td> <code id="attributes-3:attr-media-mediagroup"><a href="semantics.html#attr-media-mediagroup">audio</a></code>;
          <code id="attributes-3:attr-media-mediagroup-2"><a href="semantics.html#attr-media-mediagroup">video</a></code>
     </td><td> Groups <a href="semantics.html#media-element" id="attributes-3:media-element">media elements</a> together with an implicit <code id="attributes-3:mediacontroller"><a href="semantics.html#mediacontroller">MediaController</a></code>
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>menu</code>
     </th><td> <code id="attributes-3:attr-button-menu"><a href="semantics.html#attr-button-menu">button</a></code>
     </td><td> Specifies the element's <a href="semantics.html#designated-pop-up-menu" id="attributes-3:designated-pop-up-menu">designated pop-up menu</a>
     </td><td> <a href="infrastructure.html#concept-id" id="attributes-3:concept-id-7">ID</a>*
    </td></tr><tr><th> <code>method</code>
     </th><td> <code id="attributes-3:attr-fs-method"><a href="semantics.html#attr-fs-method">form</a></code>
     </td><td> HTTP method to use for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-10">form submission</a>
     </td><td> "<code id="attributes-3:attr-fs-method-get-keyword"><a href="semantics.html#attr-fs-method-get-keyword">GET</a></code>";
          "<code id="attributes-3:attr-fs-method-post-keyword"><a href="semantics.html#attr-fs-method-post-keyword">POST</a></code>";
          "<code id="attributes-3:attr-fs-method-dialog-keyword"><a href="semantics.html#attr-fs-method-dialog-keyword">dialog</a></code>"
    </td></tr><tr><th> <code>min</code>
     </th><td> <code id="attributes-3:attr-input-min"><a href="semantics.html#attr-input-min">input</a></code>
     </td><td> Minimum value
     </td><td> Varies*
    </td></tr><tr><th> <code>min</code>
     </th><td> <code id="attributes-3:attr-meter-min"><a href="semantics.html#attr-meter-min">meter</a></code>
     </td><td> Lower bound of range
     </td><td> <a href="infrastructure.html#valid-floating-point-number" id="attributes-3:valid-floating-point-number-4">Valid floating-point number</a>*
    </td></tr><tr><th> <code>minlength</code>
     </th><td> <code id="attributes-3:attr-input-minlength"><a href="semantics.html#attr-input-minlength">input</a></code>;
          <code id="attributes-3:attr-textarea-minlength"><a href="semantics.html#attr-textarea-minlength">textarea</a></code>
     </td><td> Minimum length of value
     </td><td> <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-6">Valid non-negative integer</a>
    </td></tr><tr><th> <code>multiple</code>
     </th><td> <code id="attributes-3:attr-input-multiple"><a href="semantics.html#attr-input-multiple">input</a></code>;
          <code id="attributes-3:attr-select-multiple"><a href="semantics.html#attr-select-multiple">select</a></code>
     </td><td> Whether to allow multiple values
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-16">Boolean attribute</a>
    </td></tr><tr><th> <code>muted</code>
     </th><td> <code id="attributes-3:attr-media-muted"><a href="semantics.html#attr-media-muted">audio</a></code>;
          <code id="attributes-3:attr-media-muted-2"><a href="semantics.html#attr-media-muted">video</a></code>
     </td><td> Whether to mute the <a href="semantics.html#media-resource" id="attributes-3:media-resource-3">media resource</a> by default
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-17">Boolean attribute</a>
    </td></tr><tr><th> <code>name</code>
     </th><td> <code id="attributes-3:attr-fe-name"><a href="semantics.html#attr-fe-name">button</a></code>;
          <code id="attributes-3:attr-fe-name-2"><a href="semantics.html#attr-fe-name">fieldset</a></code>;
          <code id="attributes-3:attr-fe-name-3"><a href="semantics.html#attr-fe-name">input</a></code>;
          <code id="attributes-3:attr-fe-name-4"><a href="semantics.html#attr-fe-name">keygen</a></code>;
          <code id="attributes-3:attr-fe-name-5"><a href="semantics.html#attr-fe-name">output</a></code>;
          <code id="attributes-3:attr-fe-name-6"><a href="semantics.html#attr-fe-name">select</a></code>;
          <code id="attributes-3:attr-fe-name-7"><a href="semantics.html#attr-fe-name">textarea</a></code>
     </td><td> Name of form control to use for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-11">form submission</a> and in the <code id="attributes-3:dom-form-elements"><a href="semantics.html#dom-form-elements">form.elements</a></code> API 
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>name</code>
     </th><td> <code id="attributes-3:attr-form-name"><a href="semantics.html#attr-form-name">form</a></code>
     </td><td> Name of form to use in the <code id="attributes-3:dom-document-forms"><a href="dom.html#dom-document-forms">document.forms</a></code> API
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>name</code>
     </th><td> <code id="attributes-3:attr-iframe-name"><a href="semantics.html#attr-iframe-name">iframe</a></code>;
          <code id="attributes-3:attr-object-name"><a href="semantics.html#attr-object-name">object</a></code>
     </td><td> Name of <a href="browsers.html#nested-browsing-context" id="attributes-3:nested-browsing-context">nested browsing context</a>
     </td><td> <a href="browsers.html#valid-browsing-context-name-or-keyword" id="attributes-3:valid-browsing-context-name-or-keyword-2">Valid browsing context name or keyword</a>
    </td></tr><tr><th> <code>name</code>
     </th><td> <code id="attributes-3:attr-map-name"><a href="semantics.html#attr-map-name">map</a></code>
     </td><td> Name of <a href="semantics.html#image-map" id="attributes-3:image-map-2">image map</a> to reference from the <code id="attributes-3:attr-hyperlink-usemap"><a href="semantics.html#attr-hyperlink-usemap">usemap</a></code> attribute
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>name</code>
     </th><td> <code id="attributes-3:attr-meta-name"><a href="semantics.html#attr-meta-name">meta</a></code>
     </td><td> Metadata name
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>name</code>
     </th><td> <code id="attributes-3:attr-param-name"><a href="semantics.html#attr-param-name">param</a></code>
     </td><td> Name of parameter
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>nonce</code>
     </th><td> <code id="attributes-3:attr-script-nonce"><a href="semantics.html#attr-script-nonce">script</a></code>;
          <code id="attributes-3:attr-style-nonce"><a href="semantics.html#attr-style-nonce">style</a></code>
     </td><td> Cryptographic nonce used in <cite>Content Security Policy</cite> checks <a href="references.html#refsCSP">[CSP]</a>
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>novalidate</code>
     </th><td> <code id="attributes-3:attr-fs-novalidate"><a href="semantics.html#attr-fs-novalidate">form</a></code>
     </td><td> Bypass form control validation for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-12">form submission</a>
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-18">Boolean attribute</a>
    </td></tr><tr><th> <code>open</code>
     </th><td> <code id="attributes-3:attr-details-open"><a href="semantics.html#attr-details-open">details</a></code>
     </td><td> Whether the details are visible
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-19">Boolean attribute</a>
    </td></tr><tr><th> <code>open</code>
     </th><td> <code id="attributes-3:attr-dialog-open"><a href="semantics.html#attr-dialog-open">dialog</a></code>
     </td><td> Whether the dialog box is showing
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-20">Boolean attribute</a>
    </td></tr><tr><th> <code>optimum</code>
     </th><td> <code id="attributes-3:attr-meter-optimum"><a href="semantics.html#attr-meter-optimum">meter</a></code>
     </td><td> Optimum value in gauge
     </td><td> <a href="infrastructure.html#valid-floating-point-number" id="attributes-3:valid-floating-point-number-5">Valid floating-point number</a>*
    </td></tr><tr><th> <code>pattern</code>
     </th><td> <code id="attributes-3:attr-input-pattern"><a href="semantics.html#attr-input-pattern">input</a></code>
     </td><td> Pattern to be matched by the form control's value
     </td><td> Regular expression matching the JavaScript <i>Pattern</i> production
    </td></tr><tr><th> <code>placeholder</code>
     </th><td> <code id="attributes-3:attr-input-placeholder"><a href="semantics.html#attr-input-placeholder">input</a></code>;
          <code id="attributes-3:attr-textarea-placeholder"><a href="semantics.html#attr-textarea-placeholder">textarea</a></code>
     </td><td> User-visible label to be placed within the form control
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>poster</code>
     </th><td> <code id="attributes-3:attr-video-poster"><a href="semantics.html#attr-video-poster">video</a></code>
     </td><td> Poster frame to show prior to video playback
     </td><td> <a href="infrastructure.html#valid-non-empty-url-potentially-surrounded-by-spaces" id="attributes-3:valid-non-empty-url-potentially-surrounded-by-spaces-7">Valid non-empty URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>preload</code>
     </th><td> <code id="attributes-3:attr-media-preload"><a href="semantics.html#attr-media-preload">audio</a></code>;
          <code id="attributes-3:attr-media-preload-2"><a href="semantics.html#attr-media-preload">video</a></code>
     </td><td> Hints how much buffering the <a href="semantics.html#media-resource" id="attributes-3:media-resource-4">media resource</a> will likely need
     </td><td> "<code id="attributes-3:attr-media-preload-none"><a href="semantics.html#attr-media-preload-none">none</a></code>";
          "<code id="attributes-3:attr-media-preload-metadata"><a href="semantics.html#attr-media-preload-metadata">metadata</a></code>";
          "<code id="attributes-3:attr-media-preload-auto"><a href="semantics.html#attr-media-preload-auto">auto</a></code>"
    </td></tr><tr><th> <code>radiogroup</code>
     </th><td> <code id="attributes-3:attr-menuitem-radiogroup"><a href="semantics.html#attr-menuitem-radiogroup">menuitem</a></code>
     </td><td> Name of group of commands to treat as a radio button group
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>readonly</code>
     </th><td> <code id="attributes-3:attr-input-readonly"><a href="semantics.html#attr-input-readonly">input</a></code>;
          <code id="attributes-3:attr-textarea-readonly"><a href="semantics.html#attr-textarea-readonly">textarea</a></code>
     </td><td> Whether to allow the value to be edited by the user
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-21">Boolean attribute</a>
    </td></tr><tr><th> <code>rel</code>
     </th><td> <code id="attributes-3:attr-hyperlink-rel"><a href="semantics.html#attr-hyperlink-rel">a</a></code>;
          <code id="attributes-3:attr-hyperlink-rel-2"><a href="semantics.html#attr-hyperlink-rel">area</a></code>;
          <code id="attributes-3:attr-link-rel"><a href="semantics.html#attr-link-rel">link</a></code>
     </td><td> Relationship between the document containing the hyperlink and the destination resource
     </td><td> <a href="infrastructure.html#set-of-space-separated-tokens" id="attributes-3:set-of-space-separated-tokens-3">Set of space-separated tokens</a>*
    </td></tr><tr><th> <code>required</code>
     </th><td> <code id="attributes-3:attr-input-required"><a href="semantics.html#attr-input-required">input</a></code>;
          <code id="attributes-3:attr-select-required"><a href="semantics.html#attr-select-required">select</a></code>;
          <code id="attributes-3:attr-textarea-required"><a href="semantics.html#attr-textarea-required">textarea</a></code>
     </td><td> Whether the control is required for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-13">form submission</a>
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-22">Boolean attribute</a>
    </td></tr><tr><th> <code>reversed</code>
     </th><td> <code id="attributes-3:attr-ol-reversed"><a href="semantics.html#attr-ol-reversed">ol</a></code>
     </td><td> Number the list backwards
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-23">Boolean attribute</a>
    </td></tr><tr><th> <code>rows</code>
     </th><td> <code id="attributes-3:attr-textarea-rows"><a href="semantics.html#attr-textarea-rows">textarea</a></code>
     </td><td> Number of lines to show
     </td><td> <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-7">Valid non-negative integer</a> greater than zero
    </td></tr><tr><th> <code>rowspan</code>
     </th><td> <code id="attributes-3:attr-tdth-rowspan"><a href="semantics.html#attr-tdth-rowspan">td</a></code>;
          <code id="attributes-3:attr-tdth-rowspan-2"><a href="semantics.html#attr-tdth-rowspan">th</a></code>
     </td><td> Number of rows that the cell is to span
     </td><td> <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-8">Valid non-negative integer</a>
    </td></tr><tr><th> <code>sandbox</code>
     </th><td> <code id="attributes-3:attr-iframe-sandbox"><a href="semantics.html#attr-iframe-sandbox">iframe</a></code>
     </td><td> Security rules for nested content
     </td><td> <a href="infrastructure.html#unordered-set-of-unique-space-separated-tokens" id="attributes-3:unordered-set-of-unique-space-separated-tokens-7">Unordered set of unique space-separated tokens</a>, <a href="infrastructure.html#ascii-case-insensitive" id="attributes-3:ascii-case-insensitive-3">ASCII case-insensitive</a>, consisting of
          "<code id="attributes-3:attr-iframe-sandbox-allow-forms"><a href="browsers.html#attr-iframe-sandbox-allow-forms">allow-forms</a></code>",
          "<code id="attributes-3:attr-iframe-sandbox-allow-modals"><a href="browsers.html#attr-iframe-sandbox-allow-modals">allow-modals</a></code>",
          "<code id="attributes-3:attr-iframe-sandbox-allow-pointer-lock"><a href="browsers.html#attr-iframe-sandbox-allow-pointer-lock">allow-pointer-lock</a></code>",
          "<code id="attributes-3:attr-iframe-sandbox-allow-popups"><a href="browsers.html#attr-iframe-sandbox-allow-popups">allow-popups</a></code>",
          "<code id="attributes-3:attr-iframe-sandbox-allow-popups-to-escape-sandbox"><a href="browsers.html#attr-iframe-sandbox-allow-popups-to-escape-sandbox">allow-popups-to-escape-sandbox</a></code>",
          "<code id="attributes-3:attr-iframe-sandbox-allow-same-origin"><a href="browsers.html#attr-iframe-sandbox-allow-same-origin">allow-same-origin</a></code>",
          "<code id="attributes-3:attr-iframe-sandbox-allow-scripts"><a href="browsers.html#attr-iframe-sandbox-allow-scripts">allow-scripts</a></code> and
          "<code id="attributes-3:attr-iframe-sandbox-allow-top-navigation"><a href="browsers.html#attr-iframe-sandbox-allow-top-navigation">allow-top-navigation</a></code>"
    </td></tr><tr><th> <code>spellcheck</code>
     </th><td> <a href="editing.html#attr-spellcheck" id="attributes-3:attr-spellcheck">HTML elements</a>
     </td><td> Whether the element is to have its spelling and grammar checked
     </td><td> "<code>true</code>"; "<code>false</code>"
    </td></tr><tr><th> <code>scope</code>
     </th><td> <code id="attributes-3:attr-th-scope"><a href="semantics.html#attr-th-scope">th</a></code>
     </td><td> Specifies which cells the header cell applies to
     </td><td> "<code id="attributes-3:attr-th-scope-row"><a href="semantics.html#attr-th-scope-row">row</a></code>";
          "<code id="attributes-3:attr-th-scope-col"><a href="semantics.html#attr-th-scope-col">col</a></code>";
          "<code id="attributes-3:attr-th-scope-rowgroup"><a href="semantics.html#attr-th-scope-rowgroup">rowgroup</a></code>";
          "<code id="attributes-3:attr-th-scope-colgroup"><a href="semantics.html#attr-th-scope-colgroup">colgroup</a></code>"
    </td></tr><tr><th> <code>scoped</code>
     </th><td> <code id="attributes-3:attr-style-scoped"><a href="semantics.html#attr-style-scoped">style</a></code>
     </td><td> Whether the styles apply to the entire document or just the parent subtree
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-24">Boolean attribute</a>
    </td></tr><tr><th> <code>seamless</code>
     </th><td> <code id="attributes-3:attr-iframe-seamless"><a href="semantics.html#attr-iframe-seamless">iframe</a></code>
     </td><td> Whether to apply the document's styles to the nested content
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-25">Boolean attribute</a>
    </td></tr><tr><th> <code>selected</code>
     </th><td> <code id="attributes-3:attr-option-selected"><a href="semantics.html#attr-option-selected">option</a></code>
     </td><td> Whether the option is selected by default
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-26">Boolean attribute</a>
    </td></tr><tr><th> <code>shape</code>
     </th><td> <code id="attributes-3:attr-area-shape"><a href="semantics.html#attr-area-shape">area</a></code>
     </td><td> The kind of shape to be created in an <a href="semantics.html#image-map" id="attributes-3:image-map-3">image map</a>
     </td><td> "<code id="attributes-3:attr-area-shape-keyword-circle"><a href="semantics.html#attr-area-shape-keyword-circle">circle</a></code>";
          "<code id="attributes-3:attr-area-shape-keyword-default"><a href="semantics.html#attr-area-shape-keyword-default">default</a></code>";
          "<code id="attributes-3:attr-area-shape-keyword-poly"><a href="semantics.html#attr-area-shape-keyword-poly">poly</a></code>";
          "<code id="attributes-3:attr-area-shape-keyword-rect"><a href="semantics.html#attr-area-shape-keyword-rect">rect</a></code>"
    </td></tr><tr><th> <code>size</code>
     </th><td> <code id="attributes-3:attr-input-size"><a href="semantics.html#attr-input-size">input</a></code>;
          <code id="attributes-3:attr-select-size"><a href="semantics.html#attr-select-size">select</a></code>
     </td><td> Size of the control
     </td><td> <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-9">Valid non-negative integer</a> greater than zero
    </td></tr><tr><th> <code>sizes</code>
     </th><td> <code id="attributes-3:attr-link-sizes"><a href="semantics.html#attr-link-sizes">link</a></code>
     </td><td> Sizes of the icons (for <code id="attributes-3:attr-link-rel-2"><a href="semantics.html#attr-link-rel">rel</a></code>="<code id="attributes-3:rel-icon"><a href="semantics.html#rel-icon">icon</a></code>")
     </td><td> <a href="infrastructure.html#unordered-set-of-unique-space-separated-tokens" id="attributes-3:unordered-set-of-unique-space-separated-tokens-8">Unordered set of unique space-separated tokens</a>, <a href="infrastructure.html#ascii-case-insensitive" id="attributes-3:ascii-case-insensitive-4">ASCII case-insensitive</a>, consisting of sizes*
    </td></tr><tr><th> <code>sortable</code>
     </th><td> <code id="attributes-3:attr-table-sortable"><a href="semantics.html#attr-table-sortable">table</a></code>
     </td><td> Enables a sorting interface for the table
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-27">Boolean attribute</a>
    </td></tr><tr><th> <code>sorted</code>
     </th><td> <code id="attributes-3:attr-th-sorted"><a href="semantics.html#attr-th-sorted">th</a></code>
     </td><td> <a href="semantics.html#column-sort-direction" id="attributes-3:column-sort-direction">Column sort direction</a> and <a href="semantics.html#column-key-ordinality" id="attributes-3:column-key-ordinality">ordinality</a>
     </td><td> <a href="infrastructure.html#set-of-space-separated-tokens" id="attributes-3:set-of-space-separated-tokens-4">Set of space-separated tokens</a>, <a href="infrastructure.html#ascii-case-insensitive" id="attributes-3:ascii-case-insensitive-5">ASCII case-insensitive</a>, consisting of neither, one, or both of "<code id="attributes-3:attr-th-sorted-reversed"><a href="semantics.html#attr-th-sorted-reversed">reversed</a></code>" and a <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-10">valid non-negative integer</a> greater than zero
    </td></tr><tr><th> <code>span</code>
     </th><td> <code id="attributes-3:attr-col-span"><a href="semantics.html#attr-col-span">col</a></code>;
          <code id="attributes-3:attr-colgroup-span"><a href="semantics.html#attr-colgroup-span">colgroup</a></code>
     </td><td> Number of columns spanned by the element
     </td><td> <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-11">Valid non-negative integer</a> greater than zero
    </td></tr><tr><th> <code>src</code>
     </th><td> <code id="attributes-3:attr-media-src"><a href="semantics.html#attr-media-src">audio</a></code>;
          <code id="attributes-3:attr-embed-src"><a href="semantics.html#attr-embed-src">embed</a></code>;
          <code id="attributes-3:attr-iframe-src"><a href="semantics.html#attr-iframe-src">iframe</a></code>;
          <code id="attributes-3:attr-img-src"><a href="semantics.html#attr-img-src">img</a></code>;
          <code id="attributes-3:attr-input-src"><a href="semantics.html#attr-input-src">input</a></code>;
          <code id="attributes-3:attr-script-src"><a href="semantics.html#attr-script-src">script</a></code>;
          <code id="attributes-3:attr-source-src"><a href="semantics.html#attr-source-src">source</a></code>;
          <code id="attributes-3:attr-track-src"><a href="semantics.html#attr-track-src">track</a></code>;
          <code id="attributes-3:attr-media-src-2"><a href="semantics.html#attr-media-src">video</a></code>
     </td><td> Address of the resource
     </td><td> <a href="infrastructure.html#valid-non-empty-url-potentially-surrounded-by-spaces" id="attributes-3:valid-non-empty-url-potentially-surrounded-by-spaces-8">Valid non-empty URL potentially surrounded by spaces</a>
    </td></tr><tr><th> <code>srcdoc</code>
     </th><td> <code id="attributes-3:attr-iframe-srcdoc"><a href="semantics.html#attr-iframe-srcdoc">iframe</a></code>
     </td><td> A document to render in the <code id="attributes-3:the-iframe-element-2"><a href="semantics.html#the-iframe-element">iframe</a></code>
     </td><td> The source of <a href="semantics.html#an-iframe-srcdoc-document" id="attributes-3:an-iframe-srcdoc-document">an <code>iframe</code> <code>srcdoc</code> document</a>*
    </td></tr><tr><th> <code>srclang</code>
     </th><td> <code id="attributes-3:attr-track-srclang"><a href="semantics.html#attr-track-srclang">track</a></code>
     </td><td> Language of the text track
     </td><td> Valid BCP 47 language tag
    </td></tr><tr><th> <code>srcset</code>
     </th><td> <code id="attributes-3:attr-img-srcset"><a href="semantics.html#attr-img-srcset">img</a></code>
     </td><td> Images to use in different situations (e.g. high-resolution displays, small monitors, etc)
     </td><td> Comma-separated list of <span>image candidate strings</span>
    </td></tr><tr><th> <code>start</code>
     </th><td> <code id="attributes-3:attr-ol-start"><a href="semantics.html#attr-ol-start">ol</a></code>
     </td><td> <a href="semantics.html#ordinal-value" id="attributes-3:ordinal-value">Ordinal value</a> of the first item
     </td><td> <a href="infrastructure.html#valid-integer" id="attributes-3:valid-integer">Valid integer</a>
    </td></tr><tr><th> <code>step</code>
     </th><td> <code id="attributes-3:attr-input-step"><a href="semantics.html#attr-input-step">input</a></code>
     </td><td> Granularity to be matched by the form control's value
     </td><td> <a href="infrastructure.html#valid-floating-point-number" id="attributes-3:valid-floating-point-number-6">Valid floating-point number</a> greater than zero, or "<code>any</code>"
    </td></tr><tr><th> <code>style</code>
     </th><td> <a href="dom.html#the-style-attribute" id="attributes-3:the-style-attribute">HTML elements</a>
     </td><td> Presentational and formatting instructions
     </td><td> CSS declarations*
    </td></tr><tr><th> <code>tabindex</code>
     </th><td> <a href="editing.html#attr-tabindex" id="attributes-3:attr-tabindex">HTML elements</a>
     </td><td> Whether the element is focusable, and the relative order of the element for the purposes of sequential focus navigation
     </td><td> <a href="infrastructure.html#valid-integer" id="attributes-3:valid-integer-2">Valid integer</a>
    </td></tr><tr><th> <code>target</code>
     </th><td> <code id="attributes-3:attr-hyperlink-target"><a href="semantics.html#attr-hyperlink-target">a</a></code>;
          <code id="attributes-3:attr-hyperlink-target-2"><a href="semantics.html#attr-hyperlink-target">area</a></code>
     </td><td> <a href="browsers.html#browsing-context" id="attributes-3:browsing-context-2">Browsing context</a> for <a href="semantics.html#hyperlink" id="attributes-3:hyperlink-3">hyperlink</a> <a href="browsers.html#navigate" id="attributes-3:navigate">navigation</a>
     </td><td> <a href="browsers.html#valid-browsing-context-name-or-keyword" id="attributes-3:valid-browsing-context-name-or-keyword-3">Valid browsing context name or keyword</a>
    </td></tr><tr><th> <code>target</code>
     </th><td> <code id="attributes-3:attr-base-target"><a href="semantics.html#attr-base-target">base</a></code>
     </td><td> Default <a href="browsers.html#browsing-context" id="attributes-3:browsing-context-3">browsing context</a> for <a href="semantics.html#hyperlink" id="attributes-3:hyperlink-4">hyperlink</a> <a href="browsers.html#navigate" id="attributes-3:navigate-2">navigation</a> and <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-14">form submission</a>
     </td><td> <a href="browsers.html#valid-browsing-context-name-or-keyword" id="attributes-3:valid-browsing-context-name-or-keyword-4">Valid browsing context name or keyword</a>
    </td></tr><tr><th> <code>target</code>
     </th><td> <code id="attributes-3:attr-fs-target"><a href="semantics.html#attr-fs-target">form</a></code>
     </td><td> <a href="browsers.html#browsing-context" id="attributes-3:browsing-context-4">Browsing context</a> for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-15">form submission</a>
     </td><td> <a href="browsers.html#valid-browsing-context-name-or-keyword" id="attributes-3:valid-browsing-context-name-or-keyword-5">Valid browsing context name or keyword</a>
    </td></tr><tr><th> <code>title</code>
     </th><td> <a href="dom.html#attr-title" id="attributes-3:attr-title">HTML elements</a>
     </td><td> Advisory information for the element
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>title</code>
     </th><td> <code id="attributes-3:attr-abbr-title"><a href="semantics.html#attr-abbr-title">abbr</a></code>;
          <code id="attributes-3:attr-dfn-title"><a href="semantics.html#attr-dfn-title">dfn</a></code>
     </td><td> Full term or expansion of abbreviation
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>title</code>
     </th><td> <code id="attributes-3:attr-input-title"><a href="semantics.html#attr-input-title">input</a></code>
     </td><td> Description of pattern (when used with <code id="attributes-3:attr-input-pattern-2"><a href="semantics.html#attr-input-pattern">pattern</a></code> attribute)
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>title</code>
     </th><td> <code id="attributes-3:attr-menuitem-title"><a href="semantics.html#attr-menuitem-title">menuitem</a></code>
     </td><td> Hint describing the command
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>title</code>
     </th><td> <code id="attributes-3:attr-link-title"><a href="semantics.html#attr-link-title">link</a></code>
     </td><td> Title of the link
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>title</code>
     </th><td> <code id="attributes-3:attr-link-title-2"><a href="semantics.html#attr-link-title">link</a></code>;
          <code id="attributes-3:attr-style-title"><a href="semantics.html#attr-style-title">style</a></code>
     </td><td> Alternative style sheet set name
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>translate</code>
     </th><td> <a href="dom.html#attr-translate" id="attributes-3:attr-translate">HTML elements</a>
     </td><td> Whether the element is to be translated when the page is localized
     </td><td> "<code>yes</code>"; "<code>no</code>"
    </td></tr><tr><th> <code>type</code>
     </th><td> <code id="attributes-3:attr-hyperlink-type"><a href="semantics.html#attr-hyperlink-type">a</a></code>;
          <code id="attributes-3:attr-hyperlink-type-2"><a href="semantics.html#attr-hyperlink-type">area</a></code>;
          <code id="attributes-3:attr-link-type"><a href="semantics.html#attr-link-type">link</a></code>
     </td><td> Hint for the type of the referenced resource
     </td><td> <a href="infrastructure.html#valid-mime-type" id="attributes-3:valid-mime-type-2">Valid MIME type</a>
    </td></tr><tr><th> <code>type</code>
     </th><td> <code id="attributes-3:attr-button-type"><a href="semantics.html#attr-button-type">button</a></code>
     </td><td> Type of button
     </td><td> "<code id="attributes-3:attr-button-type-submit"><a href="semantics.html#attr-button-type-submit">submit</a></code>";
          "<code id="attributes-3:attr-button-type-reset"><a href="semantics.html#attr-button-type-reset">reset</a></code>";
          "<code id="attributes-3:attr-button-type-button"><a href="semantics.html#attr-button-type-button">button</a></code>";
          "<code id="attributes-3:attr-button-type-menu"><a href="semantics.html#attr-button-type-menu">menu</a></code>"
    </td></tr><tr><th> <code>type</code>
     </th><td> <code id="attributes-3:attr-embed-type"><a href="semantics.html#attr-embed-type">embed</a></code>;
          <code id="attributes-3:attr-object-type"><a href="semantics.html#attr-object-type">object</a></code>;
          <code id="attributes-3:attr-script-type"><a href="semantics.html#attr-script-type">script</a></code>;
          <code id="attributes-3:attr-source-type"><a href="semantics.html#attr-source-type">source</a></code>;
          <code id="attributes-3:attr-style-type"><a href="semantics.html#attr-style-type">style</a></code>
     </td><td> Type of embedded resource
     </td><td> <a href="infrastructure.html#valid-mime-type" id="attributes-3:valid-mime-type-3">Valid MIME type</a>
    </td></tr><tr><th> <code>type</code>
     </th><td> <code id="attributes-3:attr-input-type"><a href="semantics.html#attr-input-type">input</a></code>
     </td><td> Type of form control
     </td><td> <a href="semantics.html#attr-input-type" id="attributes-3:attr-input-type-2"><code>input</code> type keyword</a>
    </td></tr><tr><th> <code>type</code>
     </th><td> <code id="attributes-3:attr-menu-type"><a href="semantics.html#attr-menu-type">menu</a></code>
     </td><td> Type of menu
     </td><td> "<code id="attributes-3:popup-menu-state"><a href="semantics.html#popup-menu-state">popup</a></code>"; "<code id="attributes-3:toolbar-state"><a href="semantics.html#toolbar-state">toolbar</a></code>"
    </td></tr><tr><th> <code>type</code>
     </th><td> <code id="attributes-3:attr-menuitem-type"><a href="semantics.html#attr-menuitem-type">menuitem</a></code>
     </td><td> Type of command
     </td><td> "<code id="attributes-3:attr-menuitem-type-keyword-command"><a href="semantics.html#attr-menuitem-type-keyword-command">command</a></code>";
          "<code id="attributes-3:attr-menuitem-type-keyword-checkbox"><a href="semantics.html#attr-menuitem-type-keyword-checkbox">checkbox</a></code>";
          "<code id="attributes-3:attr-menuitem-type-keyword-radio"><a href="semantics.html#attr-menuitem-type-keyword-radio">radio</a></code>"
    </td></tr><tr><th> <code>type</code>
     </th><td> <code id="attributes-3:attr-ol-type"><a href="semantics.html#attr-ol-type">ol</a></code>
     </td><td> Kind of list marker
     </td><td> "<code id="attributes-3:attr-ol-type-keyword-decimal"><a href="semantics.html#attr-ol-type-keyword-decimal">1</a></code>";
          "<code id="attributes-3:attr-ol-type-keyword-lower-alpha"><a href="semantics.html#attr-ol-type-keyword-lower-alpha">a</a></code>";
          "<code id="attributes-3:attr-ol-type-keyword-upper-alpha"><a href="semantics.html#attr-ol-type-keyword-upper-alpha">A</a></code>";
          "<code id="attributes-3:attr-ol-type-keyword-lower-roman"><a href="semantics.html#attr-ol-type-keyword-lower-roman">i</a></code>";
          "<code id="attributes-3:attr-ol-type-keyword-upper-roman"><a href="semantics.html#attr-ol-type-keyword-upper-roman">I</a></code>"
    </td></tr><tr><th> <code>typemustmatch</code>
     </th><td> <code id="attributes-3:attr-object-typemustmatch"><a href="semantics.html#attr-object-typemustmatch">object</a></code>
     </td><td> Whether the <code id="attributes-3:attr-object-type-2"><a href="semantics.html#attr-object-type">type</a></code> attribute and the <a href="infrastructure.html#content-type" id="attributes-3:content-type">Content-Type</a> value need to match for the resource to be used
     </td><td> <a href="infrastructure.html#boolean-attribute" id="attributes-3:boolean-attribute-28">Boolean attribute</a>
    </td></tr><tr><th> <code>usemap</code>
     </th><td> <code id="attributes-3:attr-hyperlink-usemap-2"><a href="semantics.html#attr-hyperlink-usemap">img</a></code>;
          <code id="attributes-3:attr-hyperlink-usemap-3"><a href="semantics.html#attr-hyperlink-usemap">object</a></code>
     </td><td> Name of <a href="semantics.html#image-map" id="attributes-3:image-map-4">image map</a> to use
     </td><td> <a href="infrastructure.html#valid-hash-name-reference" id="attributes-3:valid-hash-name-reference">Valid hash-name reference</a>*
    </td></tr><tr><th> <code>value</code>
     </th><td> <code id="attributes-3:attr-button-value"><a href="semantics.html#attr-button-value">button</a></code>;
          <code id="attributes-3:attr-option-value"><a href="semantics.html#attr-option-value">option</a></code>
     </td><td> Value to be used for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-16">form submission</a>
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>value</code>
     </th><td> <code id="attributes-3:attr-data-value"><a href="semantics.html#attr-data-value">data</a></code>
     </td><td> Machine-readable value
     </td><td> <a href="dom.html#attribute-text">Text</a>*
    </td></tr><tr><th> <code>value</code>
     </th><td> <code id="attributes-3:attr-input-value"><a href="semantics.html#attr-input-value">input</a></code>
     </td><td> Value of the form control
     </td><td> Varies*
    </td></tr><tr><th> <code>value</code>
     </th><td> <code id="attributes-3:attr-li-value"><a href="semantics.html#attr-li-value">li</a></code>
     </td><td> <a href="semantics.html#ordinal-value" id="attributes-3:ordinal-value-2">Ordinal value</a> of the list item
     </td><td> <a href="infrastructure.html#valid-integer" id="attributes-3:valid-integer-3">Valid integer</a>
    </td></tr><tr><th> <code>value</code>
     </th><td> <code id="attributes-3:attr-meter-value"><a href="semantics.html#attr-meter-value">meter</a></code>;
          <code id="attributes-3:attr-progress-value"><a href="semantics.html#attr-progress-value">progress</a></code>
     </td><td> Current value of the element
     </td><td> <a href="infrastructure.html#valid-floating-point-number" id="attributes-3:valid-floating-point-number-7">Valid floating-point number</a>
    </td></tr><tr><th> <code>value</code>
     </th><td> <code id="attributes-3:attr-param-value"><a href="semantics.html#attr-param-value">param</a></code>
     </td><td> Value of parameter
     </td><td> <a href="dom.html#attribute-text">Text</a>
    </td></tr><tr><th> <code>width</code>
     </th><td> <code id="attributes-3:attr-canvas-width"><a href="semantics.html#attr-canvas-width">canvas</a></code>;
          <code id="attributes-3:attr-dim-width"><a href="semantics.html#attr-dim-width">embed</a></code>;
          <code id="attributes-3:attr-dim-width-2"><a href="semantics.html#attr-dim-width">iframe</a></code>;
          <code id="attributes-3:attr-dim-width-3"><a href="semantics.html#attr-dim-width">img</a></code>;
          <code id="attributes-3:attr-dim-width-4"><a href="semantics.html#attr-dim-width">input</a></code>;
          <code id="attributes-3:attr-dim-width-5"><a href="semantics.html#attr-dim-width">object</a></code>;
          <code id="attributes-3:attr-dim-width-6"><a href="semantics.html#attr-dim-width">video</a></code>
     </td><td> Horizontal dimension
     </td><td> <a href="infrastructure.html#valid-non-negative-integer" id="attributes-3:valid-non-negative-integer-12">Valid non-negative integer</a>
    </td></tr><tr><th> <code>wrap</code>
     </th><td> <code id="attributes-3:attr-textarea-wrap"><a href="semantics.html#attr-textarea-wrap">textarea</a></code>
     </td><td> How the value of the form control is to be wrapped for <a href="semantics.html#form-submission-2" id="attributes-3:form-submission-2-17">form submission</a>
     </td><td> "<code id="attributes-3:attr-textarea-wrap-soft"><a href="semantics.html#attr-textarea-wrap-soft">soft</a></code>";
          "<code id="attributes-3:attr-textarea-wrap-hard"><a href="semantics.html#attr-textarea-wrap-hard">hard</a></code>"
  </td></tr>
 <tr><th id="ix-handler-onabort"> <code>onabort</code>
     </th><td> <a href="webappapis.html#handler-onabort" id="attributes-3:handler-onabort">HTML elements</a>
     </td><td> <code id="attributes-3:event-abort"><a href="index.html#event-abort">abort</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onautocomplete"> <code>onautocomplete</code>
     </th><td> <a href="webappapis.html#handler-onautocomplete" id="attributes-3:handler-onautocomplete">HTML elements</a>
     </td><td> <code id="attributes-3:event-autocomplete"><a href="index.html#event-autocomplete">autocomplete</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-2">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onautocompleteerror"> <code>onautocompleteerror</code>
     </th><td> <a href="webappapis.html#handler-onautocompleteerror" id="attributes-3:handler-onautocompleteerror">HTML elements</a>
     </td><td> <code id="attributes-3:event-autocompleteerror"><a href="index.html#event-autocompleteerror">autocompleteerror</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-3">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onafterprint"> <code>onafterprint</code>
     </th><td> <code id="attributes-3:handler-window-onafterprint"><a href="webappapis.html#handler-window-onafterprint">body</a></code>
     </td><td> <code id="attributes-3:event-afterprint"><a href="index.html#event-afterprint">afterprint</a></code> event handler for <code id="attributes-3:window"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-4">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onbeforeprint"> <code>onbeforeprint</code>
     </th><td> <code id="attributes-3:handler-window-onbeforeprint"><a href="webappapis.html#handler-window-onbeforeprint">body</a></code>
     </td><td> <code id="attributes-3:event-beforeprint"><a href="index.html#event-beforeprint">beforeprint</a></code> event handler for <code id="attributes-3:window-2"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-5">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onbeforeunload"> <code>onbeforeunload</code>
     </th><td> <code id="attributes-3:handler-window-onbeforeunload"><a href="webappapis.html#handler-window-onbeforeunload">body</a></code>
     </td><td> <code id="attributes-3:event-beforeunload"><a href="index.html#event-beforeunload">beforeunload</a></code> event handler for <code id="attributes-3:window-3"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-6">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onblur"> <code>onblur</code>
     </th><td> <a href="webappapis.html#handler-onblur" id="attributes-3:handler-onblur">HTML elements</a>
     </td><td> <code id="attributes-3:event-blur"><a href="index.html#event-blur">blur</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-7">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-oncancel"> <code>oncancel</code>
     </th><td> <a href="webappapis.html#handler-oncancel" id="attributes-3:handler-oncancel">HTML elements</a>
     </td><td> <code id="attributes-3:event-cancel"><a href="index.html#event-cancel">cancel</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-8">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-oncanplay"> <code>oncanplay</code>
     </th><td> <a href="webappapis.html#handler-oncanplay" id="attributes-3:handler-oncanplay">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-canplay"><a href="semantics.html#event-media-canplay">canplay</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-9">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-oncanplaythrough"> <code>oncanplaythrough</code>
     </th><td> <a href="webappapis.html#handler-oncanplaythrough" id="attributes-3:handler-oncanplaythrough">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-canplaythrough"><a href="semantics.html#event-media-canplaythrough">canplaythrough</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-10">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onchange"> <code>onchange</code>
     </th><td> <a href="webappapis.html#handler-onchange" id="attributes-3:handler-onchange">HTML elements</a>
     </td><td> <code id="attributes-3:event-change"><a href="index.html#event-change">change</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-11">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onclick"> <code>onclick</code>
     </th><td> <a href="webappapis.html#handler-onclick" id="attributes-3:handler-onclick">HTML elements</a>
     </td><td> <code id="attributes-3:event-click"><a href="infrastructure.html#event-click">click</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-12">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onclose"> <code>onclose</code>
     </th><td> <a href="webappapis.html#handler-onclose" id="attributes-3:handler-onclose">HTML elements</a>
     </td><td> <code id="attributes-3:event-close"><a href="index.html#event-close">close</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-13">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-oncontextmenu"> <code>oncontextmenu</code>
     </th><td> <a href="webappapis.html#handler-oncontextmenu" id="attributes-3:handler-oncontextmenu">HTML elements</a>
     </td><td> <code id="attributes-3:event-contextmenu"><a href="index.html#event-contextmenu">contextmenu</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-14">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-oncuechange"> <code>oncuechange</code>
     </th><td> <a href="webappapis.html#handler-oncuechange" id="attributes-3:handler-oncuechange">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-cuechange"><a href="semantics.html#event-media-cuechange">cuechange</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-15">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ondblclick"> <code>ondblclick</code>
     </th><td> <a href="webappapis.html#handler-ondblclick" id="attributes-3:handler-ondblclick">HTML elements</a>
     </td><td> <code id="attributes-3:event-dblclick"><a href="infrastructure.html#event-dblclick">dblclick</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-16">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ondrag"> <code>ondrag</code>
     </th><td> <a href="webappapis.html#handler-ondrag" id="attributes-3:handler-ondrag">HTML elements</a>
     </td><td> <code id="attributes-3:event-dnd-drag"><a href="editing.html#event-dnd-drag">drag</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-17">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ondragend"> <code>ondragend</code>
     </th><td> <a href="webappapis.html#handler-ondragend" id="attributes-3:handler-ondragend">HTML elements</a>
     </td><td> <code id="attributes-3:event-dnd-dragend"><a href="editing.html#event-dnd-dragend">dragend</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-18">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ondragenter"> <code>ondragenter</code>
     </th><td> <a href="webappapis.html#handler-ondragenter" id="attributes-3:handler-ondragenter">HTML elements</a>
     </td><td> <code id="attributes-3:event-dnd-dragenter"><a href="editing.html#event-dnd-dragenter">dragenter</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-19">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ondragexit"> <code>ondragexit</code>
     </th><td> <a href="webappapis.html#handler-ondragexit" id="attributes-3:handler-ondragexit">HTML elements</a>
     </td><td> <code id="attributes-3:event-dnd-dragexit"><a href="editing.html#event-dnd-dragexit">dragexit</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-20">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ondragleave"> <code>ondragleave</code>
     </th><td> <a href="webappapis.html#handler-ondragleave" id="attributes-3:handler-ondragleave">HTML elements</a>
     </td><td> <code id="attributes-3:event-dnd-dragleave"><a href="editing.html#event-dnd-dragleave">dragleave</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-21">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ondragover"> <code>ondragover</code>
     </th><td> <a href="webappapis.html#handler-ondragover" id="attributes-3:handler-ondragover">HTML elements</a>
     </td><td> <code id="attributes-3:event-dnd-dragover"><a href="editing.html#event-dnd-dragover">dragover</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-22">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ondragstart"> <code>ondragstart</code>
     </th><td> <a href="webappapis.html#handler-ondragstart" id="attributes-3:handler-ondragstart">HTML elements</a>
     </td><td> <code id="attributes-3:event-dnd-dragstart"><a href="editing.html#event-dnd-dragstart">dragstart</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-23">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ondrop"> <code>ondrop</code>
     </th><td> <a href="webappapis.html#handler-ondrop" id="attributes-3:handler-ondrop">HTML elements</a>
     </td><td> <code id="attributes-3:event-dnd-drop"><a href="editing.html#event-dnd-drop">drop</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-24">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ondurationchange"> <code>ondurationchange</code>
     </th><td> <a href="webappapis.html#handler-ondurationchange" id="attributes-3:handler-ondurationchange">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-durationchange"><a href="semantics.html#event-media-durationchange">durationchange</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-25">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onemptied"> <code>onemptied</code>
     </th><td> <a href="webappapis.html#handler-onemptied" id="attributes-3:handler-onemptied">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-emptied"><a href="semantics.html#event-media-emptied">emptied</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-26">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onended"> <code>onended</code>
     </th><td> <a href="webappapis.html#handler-onended" id="attributes-3:handler-onended">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-ended"><a href="semantics.html#event-media-ended">ended</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-27">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onerror"> <code>onerror</code>
     </th><td> <a href="webappapis.html#handler-onerror" id="attributes-3:handler-onerror">HTML elements</a>
     </td><td> <code id="attributes-3:event-error"><a href="index.html#event-error">error</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-28">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onfocus"> <code>onfocus</code>
     </th><td> <a href="webappapis.html#handler-onfocus" id="attributes-3:handler-onfocus">HTML elements</a>
     </td><td> <code id="attributes-3:event-focus"><a href="index.html#event-focus">focus</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-29">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onhashchange"> <code>onhashchange</code>
     </th><td> <code id="attributes-3:handler-window-onhashchange"><a href="webappapis.html#handler-window-onhashchange">body</a></code>
     </td><td> <code id="attributes-3:event-hashchange"><a href="index.html#event-hashchange">hashchange</a></code> event handler for <code id="attributes-3:window-4"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-30">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-oninput"> <code>oninput</code>
     </th><td> <a href="webappapis.html#handler-oninput" id="attributes-3:handler-oninput">HTML elements</a>
     </td><td> <code id="attributes-3:event-input"><a href="index.html#event-input">input</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-31">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-oninvalid"> <code>oninvalid</code>
     </th><td> <a href="webappapis.html#handler-oninvalid" id="attributes-3:handler-oninvalid">HTML elements</a>
     </td><td> <code id="attributes-3:event-invalid"><a href="index.html#event-invalid">invalid</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-32">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onkeydown"> <code>onkeydown</code>
     </th><td> <a href="webappapis.html#handler-onkeydown" id="attributes-3:handler-onkeydown">HTML elements</a>
     </td><td> <code id="attributes-3:event-keydown"><a href="infrastructure.html#event-keydown">keydown</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-33">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onkeypress"> <code>onkeypress</code>
     </th><td> <a href="webappapis.html#handler-onkeypress" id="attributes-3:handler-onkeypress">HTML elements</a>
     </td><td> <code id="attributes-3:event-keypress"><a href="infrastructure.html#event-keypress">keypress</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-34">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onkeyup"> <code>onkeyup</code>
     </th><td> <a href="webappapis.html#handler-onkeyup" id="attributes-3:handler-onkeyup">HTML elements</a>
     </td><td> <code id="attributes-3:event-keyup"><a href="infrastructure.html#event-keyup">keyup</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-35">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onlanguagechange"> <code>onlanguagechange</code>
     </th><td> <code id="attributes-3:handler-window-onlanguagechange"><a href="webappapis.html#handler-window-onlanguagechange">body</a></code>
     </td><td> <code id="attributes-3:event-languagechange"><a href="index.html#event-languagechange">languagechange</a></code> event handler for <code id="attributes-3:window-5"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-36">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onload"> <code>onload</code>
     </th><td> <a href="webappapis.html#handler-onload" id="attributes-3:handler-onload">HTML elements</a>
     </td><td> <code id="attributes-3:event-load"><a href="index.html#event-load">load</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-37">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onloadeddata"> <code>onloadeddata</code>
     </th><td> <a href="webappapis.html#handler-onloadeddata" id="attributes-3:handler-onloadeddata">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-loadeddata"><a href="semantics.html#event-media-loadeddata">loadeddata</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-38">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onloadedmetadata"> <code>onloadedmetadata</code>
     </th><td> <a href="webappapis.html#handler-onloadedmetadata" id="attributes-3:handler-onloadedmetadata">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-loadedmetadata"><a href="semantics.html#event-media-loadedmetadata">loadedmetadata</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-39">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onloadstart"> <code>onloadstart</code>
     </th><td> <a href="webappapis.html#handler-onloadstart" id="attributes-3:handler-onloadstart">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-loadstart"><a href="semantics.html#event-media-loadstart">loadstart</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-40">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onmessage"> <code>onmessage</code>
     </th><td> <code id="attributes-3:handler-window-onmessage"><a href="webappapis.html#handler-window-onmessage">body</a></code>
     </td><td> <code id="attributes-3:event-message"><a href="index.html#event-message">message</a></code> event handler for <code id="attributes-3:window-6"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-41">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onmousedown"> <code>onmousedown</code>
     </th><td> <a href="webappapis.html#handler-onmousedown" id="attributes-3:handler-onmousedown">HTML elements</a>
     </td><td> <code id="attributes-3:event-mousedown"><a href="infrastructure.html#event-mousedown">mousedown</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-42">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onmouseenter"> <code>onmouseenter</code>
     </th><td> <a href="webappapis.html#handler-onmouseenter" id="attributes-3:handler-onmouseenter">HTML elements</a>
     </td><td> <code id="attributes-3:event-mouseenter"><a href="infrastructure.html#event-mouseenter">mouseenter</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-43">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onmouseleave"> <code>onmouseleave</code>
     </th><td> <a href="webappapis.html#handler-onmouseleave" id="attributes-3:handler-onmouseleave">HTML elements</a>
     </td><td> <code id="attributes-3:event-mouseleave"><a href="infrastructure.html#event-mouseleave">mouseleave</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-44">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onmousemove"> <code>onmousemove</code>
     </th><td> <a href="webappapis.html#handler-onmousemove" id="attributes-3:handler-onmousemove">HTML elements</a>
     </td><td> <code id="attributes-3:event-mousemove"><a href="infrastructure.html#event-mousemove">mousemove</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-45">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onmouseout"> <code>onmouseout</code>
     </th><td> <a href="webappapis.html#handler-onmouseout" id="attributes-3:handler-onmouseout">HTML elements</a>
     </td><td> <code id="attributes-3:event-mouseout"><a href="infrastructure.html#event-mouseout">mouseout</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-46">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onmouseover"> <code>onmouseover</code>
     </th><td> <a href="webappapis.html#handler-onmouseover" id="attributes-3:handler-onmouseover">HTML elements</a>
     </td><td> <code id="attributes-3:event-mouseover"><a href="infrastructure.html#event-mouseover">mouseover</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-47">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onmouseup"> <code>onmouseup</code>
     </th><td> <a href="webappapis.html#handler-onmouseup" id="attributes-3:handler-onmouseup">HTML elements</a>
     </td><td> <code id="attributes-3:event-mouseup"><a href="infrastructure.html#event-mouseup">mouseup</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-48">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onwheel"> <code>onwheel</code>
     </th><td> <a href="webappapis.html#handler-onwheel" id="attributes-3:handler-onwheel">HTML elements</a>
     </td><td> <code id="attributes-3:event-wheel"><a href="infrastructure.html#event-wheel">wheel</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-49">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onoffline"> <code>onoffline</code>
     </th><td> <code id="attributes-3:handler-window-onoffline"><a href="webappapis.html#handler-window-onoffline">body</a></code>
     </td><td> <code id="attributes-3:event-offline"><a href="index.html#event-offline">offline</a></code> event handler for <code id="attributes-3:window-7"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-50">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-ononline"> <code>ononline</code>
     </th><td> <code id="attributes-3:handler-window-ononline"><a href="webappapis.html#handler-window-ononline">body</a></code>
     </td><td> <code id="attributes-3:event-online"><a href="index.html#event-online">online</a></code> event handler for <code id="attributes-3:window-8"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-51">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onpagehide"> <code>onpagehide</code>
     </th><td> <code id="attributes-3:handler-window-onpagehide"><a href="webappapis.html#handler-window-onpagehide">body</a></code>
     </td><td> <code id="attributes-3:event-pagehide"><a href="index.html#event-pagehide">pagehide</a></code> event handler for <code id="attributes-3:window-9"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-52">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onpageshow"> <code>onpageshow</code>
     </th><td> <code id="attributes-3:handler-window-onpageshow"><a href="webappapis.html#handler-window-onpageshow">body</a></code>
     </td><td> <code id="attributes-3:event-pageshow"><a href="index.html#event-pageshow">pageshow</a></code> event handler for <code id="attributes-3:window-10"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-53">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onpause"> <code>onpause</code>
     </th><td> <a href="webappapis.html#handler-onpause" id="attributes-3:handler-onpause">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-pause"><a href="semantics.html#event-media-pause">pause</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-54">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onplay"> <code>onplay</code>
     </th><td> <a href="webappapis.html#handler-onplay" id="attributes-3:handler-onplay">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-play"><a href="semantics.html#event-media-play">play</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-55">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onplaying"> <code>onplaying</code>
     </th><td> <a href="webappapis.html#handler-onplaying" id="attributes-3:handler-onplaying">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-playing"><a href="semantics.html#event-media-playing">playing</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-56">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onpopstate"> <code>onpopstate</code>
     </th><td> <code id="attributes-3:handler-window-onpopstate"><a href="webappapis.html#handler-window-onpopstate">body</a></code>
     </td><td> <code id="attributes-3:event-popstate"><a href="index.html#event-popstate">popstate</a></code> event handler for <code id="attributes-3:window-11"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-57">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onprogress"> <code>onprogress</code>
     </th><td> <a href="webappapis.html#handler-onprogress" id="attributes-3:handler-onprogress">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-progress"><a href="semantics.html#event-media-progress">progress</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-58">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onratechange"> <code>onratechange</code>
     </th><td> <a href="webappapis.html#handler-onratechange" id="attributes-3:handler-onratechange">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-ratechange"><a href="semantics.html#event-media-ratechange">ratechange</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-59">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onreset"> <code>onreset</code>
     </th><td> <a href="webappapis.html#handler-onreset" id="attributes-3:handler-onreset">HTML elements</a>
     </td><td> <code id="attributes-3:event-reset"><a href="index.html#event-reset">reset</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-60">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onresize"> <code>onresize</code>
     </th><td> <a href="webappapis.html#handler-onresize" id="attributes-3:handler-onresize">HTML elements</a>
     </td><td> <code id="attributes-3:event-resize"><a href="infrastructure.html#event-resize">resize</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-61">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onscroll"> <code>onscroll</code>
     </th><td> <a href="webappapis.html#handler-onscroll" id="attributes-3:handler-onscroll">HTML elements</a>
     </td><td> <code id="attributes-3:event-scroll"><a href="infrastructure.html#event-scroll">scroll</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-62">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onseeked"> <code>onseeked</code>
     </th><td> <a href="webappapis.html#handler-onseeked" id="attributes-3:handler-onseeked">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-seeked"><a href="semantics.html#event-media-seeked">seeked</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-63">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onseeking"> <code>onseeking</code>
     </th><td> <a href="webappapis.html#handler-onseeking" id="attributes-3:handler-onseeking">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-seeking"><a href="semantics.html#event-media-seeking">seeking</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-64">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onselect"> <code>onselect</code>
     </th><td> <a href="webappapis.html#handler-onselect" id="attributes-3:handler-onselect">HTML elements</a>
     </td><td> <code id="attributes-3:event-select"><a href="index.html#event-select">select</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-65">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onshow"> <code>onshow</code>
     </th><td> <a href="webappapis.html#handler-onshow" id="attributes-3:handler-onshow">HTML elements</a>
     </td><td> <code id="attributes-3:event-show"><a href="index.html#event-show">show</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-66">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onsort"> <code>onsort</code>
     </th><td> <a href="webappapis.html#handler-onsort" id="attributes-3:handler-onsort">HTML elements</a>
     </td><td> <code id="attributes-3:event-sort"><a href="index.html#event-sort">sort</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-67">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onstalled"> <code>onstalled</code>
     </th><td> <a href="webappapis.html#handler-onstalled" id="attributes-3:handler-onstalled">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-stalled"><a href="semantics.html#event-media-stalled">stalled</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-68">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onstorage"> <code>onstorage</code>
     </th><td> <code id="attributes-3:handler-window-onstorage"><a href="webappapis.html#handler-window-onstorage">body</a></code>
     </td><td> <code id="attributes-3:event-storage"><a href="index.html#event-storage">storage</a></code> event handler for <code id="attributes-3:window-12"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-69">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onsubmit"> <code>onsubmit</code>
     </th><td> <a href="webappapis.html#handler-onsubmit" id="attributes-3:handler-onsubmit">HTML elements</a>
     </td><td> <code id="attributes-3:event-submit"><a href="index.html#event-submit">submit</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-70">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onsuspend"> <code>onsuspend</code>
     </th><td> <a href="webappapis.html#handler-onsuspend" id="attributes-3:handler-onsuspend">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-suspend"><a href="semantics.html#event-media-suspend">suspend</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-71">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ontimeupdate"> <code>ontimeupdate</code>
     </th><td> <a href="webappapis.html#handler-ontimeupdate" id="attributes-3:handler-ontimeupdate">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-timeupdate"><a href="semantics.html#event-media-timeupdate">timeupdate</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-72">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-ontoggle"> <code>ontoggle</code>
     </th><td> <a href="webappapis.html#handler-ontoggle" id="attributes-3:handler-ontoggle">HTML elements</a>
     </td><td> <code id="attributes-3:event-toggle"><a href="index.html#event-toggle">toggle</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-73">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-window-onunload"> <code>onunload</code>
     </th><td> <code id="attributes-3:handler-window-onunload"><a href="webappapis.html#handler-window-onunload">body</a></code>
     </td><td> <code id="attributes-3:event-unload"><a href="index.html#event-unload">unload</a></code> event handler for <code id="attributes-3:window-13"><a href="browsers.html#window">Window</a></code> object
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-74">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onvolumechange"> <code>onvolumechange</code>
     </th><td> <a href="webappapis.html#handler-onvolumechange" id="attributes-3:handler-onvolumechange">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-volumechange"><a href="semantics.html#event-media-volumechange">volumechange</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-75">Event handler content attribute</a>

    </td></tr><tr><th id="ix-handler-onwaiting"> <code>onwaiting</code>
     </th><td> <a href="webappapis.html#handler-onwaiting" id="attributes-3:handler-onwaiting">HTML elements</a>
     </td><td> <code id="attributes-3:event-media-waiting"><a href="semantics.html#event-media-waiting">waiting</a></code> event handler
     </td><td> <a href="webappapis.html#event-handler-content-attributes" id="attributes-3:event-handler-content-attributes-76">Event handler content attribute</a>

  </td></tr>"""