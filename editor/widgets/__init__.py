try:
    from .toolbox_EPICS import EPICSBooleanButton, EPICSLed, EPICSValueMeterWidget, EPICSPlotPV
except:
    print("In order to use EPICS widgets install pyepics")

try:
    from .toolbox_opencv import OpencvImRead, OpencvCrop, OpencvVideo, OpencvThreshold, OpencvSplit, OpencvCvtColor, OpencvAddWeighted, OpencvBitwiseNot, OpencvBitwiseAnd, OpencvBitwiseOr,\
                            OpencvBilateralFilter, OpencvBlurFilter, OpencvDilateFilter, OpencvErodeFilter, OpencvLaplacianFilter, OpencvCanny, OpencvFindContours
except:
    print("In order to use OpenCv widgets install python-opencv")

from .toolbox_scheduling import TimerWidget

try:
    from .toolbox_siemens import PLCSiemens, ButtonSetResetBit, BitStatusWidget, WordEditWidget
except:
    print("In order to use Siemens widgets install python-snap7")
