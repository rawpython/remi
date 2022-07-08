from .gui import (
    Widget,
    Button,
    TextInput,
    SpinBox,
    Label,
    GenericDialog,
    InputDialog,
    ListView,
    ListItem,
    DropDown,
    DropDownItem,
    Image,
    Table,
    TableRow,
    TableItem,
    TableTitle,
    Input,
    Slider,
    ColorPicker,
    Date,
    GenericObject,
    FileFolderNavigator,
    FileFolderItem,
    FileSelectionDialog,
    Menu,
    MenuItem,
    FileUploader,
    FileDownloader,
    VideoPlayer,
)

from .server import App, Server, start
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
