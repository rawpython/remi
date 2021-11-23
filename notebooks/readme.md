# Notebooks with remi

## Install

In a virtual environment

`pip install jupyterlab, jupyter-server-proxy`

jupyter-server-proxy is the proxy we use for jupyter lab

Pythonnet needs Visual Studio Build Tools 2019 and needs github install in Windows

`pip install git+https://github.com/pythonnet/pythonnet.git`

pip install pywebview

## Notebooks

* JlabRemiHelloWorld.ipynb => the "HelloWorld" application
* JlabRemiWidgets_Overview.ipynb => the remi widget overview app
* JlabRemiEditor.ipynb => the remi 'IDE'

## Using...

### Create a Proxy class

* 8085 is supposed to be the remi port on localhost

```python
remiport = 8085
# overload _net_interface_ip, _overload and _process_all
class MyApp(Editor):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args,)
            
    def _net_interface_ip(self):
        ip = super()._net_interface_ip()
        return ip + f"/proxy/{remiport}"
    
    def _overload(self, data, **kwargs):
        if "filename" in kwargs:
            filename = kwargs['filename']
        else:
            return data
        paths = self.all_paths()
        for pattern in paths.keys():
            if ( filename.endswith(".css") or filename.endswith(".html") or filename.endswith(".js") or filename.endswith("internal") ):
                if type(data) == str:
                    data = re.sub(f"/{pattern}:", f"/proxy/{remiport}/{pattern}:", data)
                else:
                    data = re.sub(f"/{pattern}:", f"/proxy/{remiport}/{pattern}:", data.decode()).encode()
        return data
 
```

* add the proxy on the start

```python
myRemi = Thread(target=start, 
                         args=(MyApp,),
                         kwargs={'address':'127.0.0.1', 
                                 'port':{remiport}, 
                                 'multiple_instance':True,
                                 'enable_file_cache':True, 
                                 'update_interval':0.5, 
                                 'start_browser':False,
                                 'proxy':Proxy})
```
If the proxy kwarg is not provided, remi behaves as legacy

## Disclaimer

Only jupyter-server-proxy was tested, but other proxy should work
