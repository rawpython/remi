import remi.server as server

from simple_app import MyApp

if __name__ == "__main__":
    s = server.StandaloneServer(MyApp, start=True)
