from remi import start, App
from cli import start_app


from simple_app import MyApp

if __name__ == "__main__":
    start_app(MyApp, standalone=True)
