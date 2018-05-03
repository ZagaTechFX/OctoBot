import logging
import threading

import dash_core_components as dcc
import dash_html_components as html
from flask import request

from config.cst import CONFIG_CRYPTO_CURRENCIES
from interfaces.web import app_instance, load_callbacks, get_bot


class WebApp(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.server = None
        self.app = None

    def run(self):
        # Define the WSGI application object
        self.app = app_instance
        self.server = self.app.server

        self.app.layout = html.Div(children=[
            dcc.Graph(id='live-graph', animate=True),

            dcc.Dropdown(id='cryptocurrency-name',
                         options=[{'label': s, 'value': s}
                                  for s in self.config[CONFIG_CRYPTO_CURRENCIES].keys()],
                         value=next(iter(self.config[CONFIG_CRYPTO_CURRENCIES].keys())),
                         multi=False
                         ),

            dcc.Interval(
                id='graph-update',
                interval=5 * 1000
            ),
        ])

        load_callbacks()
        self.app.run_server(host='localhost', port=5000, debug=False, threaded=True)

    def stop(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            self.logger.warning("Not running with the Werkzeug Server")
        func()
