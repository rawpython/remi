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

# Hardcoded fallback version — used when package metadata is unavailable
# (e.g. PyInstaller frozen builds, editable installs without metadata).
# Keep in sync with setup.py.
_FALLBACK_VERSION = "2026.03.24"
__version__ = _FALLBACK_VERSION

# importlib.metadata is available in Python 3.8+; pkg_resources for older.
try:
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version(__name__)
    except PackageNotFoundError:
        pass  # metadata absent (frozen build etc.) — fallback stays
except ImportError:
    try:
        from pkg_resources import get_distribution, DistributionNotFound
        try:
            __version__ = get_distribution(__name__).version
        except DistributionNotFound:
            pass  # package not installed — fallback stays
    except ImportError:
        print("WARNING: cannot check remi version, please install "
              "importlib-metadata (Python >= 3.8) or setuptools")