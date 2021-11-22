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
class Proxy():
        @staticmethod 
        def set_url(url): 
                if url.startswith("data:"): 
                        return url 
                else: return "/proxy/8085"+url 
        @staticmethod 
        def get_url(): 
                return "/proxy/8085" 
```

* add the proxy on the start

```python
myRemi = Thread(target=start, 
                         args=(MyApp,),
                         kwargs={'address':'127.0.0.1', 
                                 'port':8085, 
                                 'multiple_instance':True,
                                 'enable_file_cache':True, 
                                 'update_interval':0.5, 
                                 'start_browser':False,
                                 'proxy':Proxy})
```
If the proxy kwarg is not provided, remi behaves as legacy

## Disclaimer

Only jupyter-server-proxy was tested, but other proxy should work