"""This module is not an example REMI program but a module used by the example
programs to provide a common cli interface.
"""
import remi

def start_app(application, **start_app_kwargs):
    try:
        import click

        @click.command()
        # We could of course specify defaults here, but we don't want to
        # maintain defaults in both the `remi/server.py` and here, so what we
        # do is *not* pass in any values that the user does not explicitly
        # specify. The boolean flags we have to give a default of 'None' to
        # *avoid* giving a True or False default.
        @click.option('--start-browser/--no-start-browser', default=None)
        @click.option('--debug/--no-debug', default=None)
        # Note, if you specify 'standalone' then some of the other arguements
        # are not applicable, we should somehow state this.
        @click.option('--standalone/--no-standalone', default=None)
        @click.option('--address')
        @click.option('--port', type=int)
        @click.option('--websocket-protocol')
        @click.option('--host-name')
        @click.option('--websocket-port', type=int)
        @click.option('--title')
        @click.option('--username')
        @click.option('--password')
        @click.option('--multiple-instance/--no-multiple-instance', default=None)
        @click.option('--enable_file_cache/--no-enable-file-cache', default=None)
        @click.option('--update_interval', type=float)
        @click.option('--websocket_timeout_timer_ms', type=int)
        @click.option('--websocket_protocol')
        @click.option('--pending_messages_queue_length', type=int)
        def run(**kwargs):
            # So if a command-line argument is explicitly given by the user then
            # that overrides whatever was passed to 'start_app' (usually from
            # the code of the example application).
            for keyword, value in kwargs.items():
                if value is not None:
                    start_app_kwargs[keyword] = value
            remi.start(application, **start_app_kwargs)

    except ImportError:
        import sys
        if len(sys.argv) > 1:
            print("To give command-line arguments you need to install 'click'")
            print("pip install click")
            sys.exit(1)
        def run():
            remi.start(application, debug=True, address='0.0.0.0')
    run()