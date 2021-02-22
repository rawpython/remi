import traceback
from remi import gui


def default_icon(name, view_w=2, view_h=0.6):
    """
    A simple function to make a default svg icon for the widgets
      such icons can be replaced later with a good one
    """
    icon = gui.Svg(width=100,height=30)
    icon.set_viewbox(-view_w/2,-view_h/2,view_w,view_h)
    text = gui.SvgText(0,0,name)
    text.style['font-size'] = "0.2px"
    text.style['text-anchor'] = "middle"
    stroke_width = 0.01
    rect = gui.SvgRectangle(-view_w/2+stroke_width,-view_h/2+stroke_width,view_w-stroke_width*2,view_h-stroke_width*2)
    rect.set_fill("none")
    rect.set_stroke(0.01,'black')
    icon.append([rect, text])
    return icon

try:
    from .toolbox_EPICS import EPICSBooleanButton, EPICSLed, EPICSValueMeterWidget, EPICSPlotPV, EPICSValueGaugeWidget
except Exception:
    class EPICSPlaceholder(gui.Label):
        icon = default_icon("missing EPICS")
        def __init__(self, msg="In order to use EPICS widgets install pyepics \n" + traceback.format_exc()):
            super(EPICSPlaceholder, self).__init__(msg)
            self.css_white_space = 'pre'

try:
    from .toolbox_opencv import OpencvImRead, OpencvCrop, OpencvVideo, OpencvThreshold, OpencvSplit, OpencvCvtColor, OpencvAddWeighted, OpencvBitwiseNot, OpencvBitwiseAnd, OpencvBitwiseOr,\
                            OpencvBilateralFilter, OpencvBlurFilter, OpencvDilateFilter, OpencvErodeFilter, OpencvLaplacianFilter, OpencvCanny, OpencvFindContours, OpencvInRangeGrayscale,\
                            OpencvMatchTemplate
except Exception:
    class OPENCVPlaceholder(gui.Label):
        icon = default_icon("missing OPENCV")
        def __init__(self, msg="In order to use OpenCv widgets install python-opencv \n" + traceback.format_exc()):
            super(OPENCVPlaceholder, self).__init__(msg)
            self.css_white_space = 'pre'

from .toolbox_scheduling import TimerWidget

try:
    from .toolbox_siemens import PLCSiemens, SiemensButton, BitStatusWidget, WordEditWidget, ByteViewWidget
except Exception:
    class SIEMENSPlaceholder(gui.Label):
        icon = default_icon("missing SIEMENS")
        def __init__(self, msg="In order to use Siemens widgets install python-snap7 \n" + traceback.format_exc()):
            super(SIEMENSPlaceholder, self).__init__(msg)
            self.css_white_space = 'pre'
