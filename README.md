# DESCRIPTION
This is development fork of [Remi GUI](https://github.com/dddomodossola/remi). It aims at adding the "url_root" feature in remi, see [here](https://github.com/dddomodossola/remi/issues/430), with the branch of the same name.
The main usage of this feature is to access remi instance (or even multiple simultaneous remi instances) from one single port on a server, i.e port 80 or 443. To specify the remi instance you want to reach from the client, use "url_root" : myserver.com/\<url_root\>

# HOWTO
To try this feature, you can use apache as frontend webserver (port 80 by default), then write some rules (rewrite) to forward traffic on remi server (port 8080 for example). Below is a sample installation/configuration steps.

* install remi from this repo
* install apache2 and enable mod_rewrite, proxy, proxy_http, proxy_wstunnel (`a2enmod rewrite proxy proxy_http proxy_wstunnel` on linux)
* write the following rules at the end of your apache virtualhost, replace "foo" with your "url_root" (see 000-default.conf):
```
RewriteEngine On
RewriteCond %{HTTP:Upgrade} =websocket [NC]
RewriteRule /foo(.*)    ws://127.0.0.1:8080/$1 [P,L]
RewriteCond %{HTTP:Upgrade} !=websocket [NC]
RewriteRule /foo(.*)    http://127.0.0.1:8080/$1 [P,L]
```
* set url_root in your remi script (see url_root_test.py for example)
* restart apache, launch remi, use your browser to reach http://localhost/foo (note we use the default port 80 of apache frontend)

# TODO
At least :

* move `url_root` to the right place inside remi (note that this variable should also be accessible from `gui.py`)
* ~~make `url_root` an optional parameter which defaults to `""`~~ Currently done in `class App[...]`.
* test this feature with https/wss
* continue implementation of some Remi widgets: where hard links are sent to the client (currently done : Image, VideoPlayer, SvgImage, FileFolderItem).
* For `Image`, `VideoPlayer`, `SvgImage` widgets, setters were modified to unconditionally prefix the input src url with `url_root`. This will cause problem for embedding contents from external server/website.
* ~~issue with no immediate clean solution: all calls (by default 3) to "/res:" in "style.css" are broken as they are not prefixed with "url_root". We should discuss about that.~~ Finally fixed by replacing all three absolute imports by relative imports (/res -> ./res) in style.css.
