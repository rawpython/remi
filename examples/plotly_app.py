"""
    Author: https://github.com/saewoonam
"""

import remi.gui as gui
from remi import start, App
import threading
import random
import time
import datetime
import json


class LabelSpinBox(gui.HBox):
    def __init__(self, label='label', default_value=0,
                 min=0, max=100, step=1, labelWidth=100,
                 spinBoxWidth=80, *args):
        super(self.__class__, self).__init__(*args)

        self._label = gui.Label(label, width=labelWidth)
        self._spinbox = gui.SpinBox(default_value=default_value,
                                    min=min, max=max,
                                    step=step, width=spinBoxWidth)

        self.append(self._label, 'label')
        self.append(self._spinbox, 'spinbox')

        self.set_on_change_listener = self._spinbox.set_on_change_listener
        self.set_value = self._spinbox.set_value
        self.get_value = self._spinbox.get_value
        self.setValue = self.set_value


class PlotlyWidget(gui.Widget):
    def __init__(self, data=None, update=None, updateRate=1,
                 **kwargs):
        super(PlotlyWidget, self).__init__(**kwargs)
        self.updateRate = updateRate
        self.data = data
        self.update = update

        javascript_code = gui.Tag()
        javascript_code.type = 'script'
        javascript_code.attributes['type'] = 'text/javascript'
        code = """
        var PLOT = document.getElementById('plot');
        var url = "plot/get_refresh";
        var plotOptions = {
                           title: 'Title goes here'
                          ,xaxis: {title: 'time'}
                          ,yaxis: {title: 'random number',type: 'linear'}
                          };
        plotOptions['margin'] = {t:50, l:50, r:30};

        Plotly.d3.json(url,
            function(error, data) {
                Plotly.plot(PLOT, data, plotOptions);
            });
        """
        javascript_code.add_child('code',   # Add to Tag
                                  code % {'id': id(self), })
        self.add_child('javascript_code', javascript_code)   # Add to widget

    def get_refresh(self):
        if self.data is None:
            return None, None

        txt = json.dumps(self.data)
        headers = {'Content-type': 'text/plain'}
        return [txt, headers]


class MyApp(App):
    def __init__(self, *args):
        html_head = '<script src="https://cdn.plot.ly/plotly-latest.min.js">'
        html_head += '</script>'
        self.data = []
        for idx in range(2):
            self.data.extend([{'x': [], 'y': [], 'type': 'scatter', 'mode':
                              'markers+lines', 'name': 'name %d' % idx}])
        super(MyApp, self).__init__(*args, html_head=html_head)

    def main(self):
        wid = gui.HBox()
        wid.style['position'] = 'absolute'
        ctrl = gui.VBox(width=400)
        ctrl.style['justify-content'] = 'space-around'

        plotContainer = gui.Widget()

        plt = PlotlyWidget(data=self.data, id='plot')
        self.plt = plt
        plotContainer.append(plt)

        self.historyBox = LabelSpinBox(default_value=100, min=1, max=10000000,
                                       step=1, label='history')

        lbl = gui.Label('GUI')

        bt = gui.Button('Start', width=200, height=30)
        bt.style['margin'] = 'auto 50px'
        bt.style['background-color'] = 'green'

        self.started = False

        # setting the listener for the onclick event of the button
        bt.set_on_click_listener(self.on_button_pressed, ctrl)

        ctrl.append(lbl)
        ctrl.append(self.historyBox)
        ctrl.append(bt)

        # returning the root widget
        wid.append(ctrl)
        wid.append(plotContainer)

        return wid

    def run(self):
        while self.running:
            for idx in range(len(self.data)):
                x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.data[idx]['x'].append(x)
                self.data[idx]['y'].append(random.random())
            if len(self.data[0]['x']) == 1:  # Can't extend an empty plot
                cmd = ''
                for idx in range(len(self.data)):
                    lastx = self.data[idx]['x']
                    lasty = self.data[idx]['y']
                    cmd += """
                    PLOT.data[%(key)s].x = [%(x)s];
                    PLOT.data[%(key)s].y = [%(y)s];
                    Plotly.redraw(PLOT);""" % {'key': idx,
                                               'x': lastx, 'y': lasty}

            else:
                xarray = []
                yarray = []
                for idx in range(len(self.data)):
                    xarray.append([self.data[idx]['x'][-1]])
                    yarray.append([self.data[idx]['y'][-1]])
                xarray = repr(xarray)
                yarray = repr(yarray)
                indices = repr(list(range(len(self.data))))
                cmd = """
                var update = {x:%(x)s, y:%(y)s};
                Plotly.extendTraces(PLOT, update, %(indices)s,%(history)s);
                """ % {'x': xarray, 'y': yarray, 'indices': indices,
                       'history': self.historyBox._spinbox.get_value()}
            self.execute_javascript(cmd)
            time.sleep(1)

    def stop(self):
        self.running = False
        self.thread.join()

    # listener function
    def on_button_pressed(self, widget, settings):
        if not self.started:
            # self.plt.status.play()
            widget.set_text('Stop')
            widget.style['background-color'] = 'red'
            for idx in range(len(self.data)):
                self.data[idx]['x'] = []
                self.data[idx]['y'] = []
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
        else:
            # self.plt.status.stop()
            self.stop()
            widget.set_text('Start')
            widget.style['background-color'] = 'green'
        self.started = not self.started

if __name__ == "__main__":
    # starts the webserver
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,
    #        enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=False, port=8081, address='0.0.0.0', start_browser=False)
