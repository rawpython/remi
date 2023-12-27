try:
    from editor import Editor
except ImportError:
    from editor.editor import Editor

from remi import start

if __name__ == "__main__":
    start(
        Editor,
        debug=False,
        address="0.0.0.0",
        port=8082,
        update_interval=0.01,
        multiple_instance=True,
    )
