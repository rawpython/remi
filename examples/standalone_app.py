from remi import start, App

from helloworld_app import MyApp

if __name__ == "__main__":
    start(MyApp, standalone=True)
