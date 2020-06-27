import os
import json

from flask import Flask

from api.schema import SCHEMA
from api.view import APIView

app = Flask(__name__)


@app.route('/')
def entrypoint():
    return '<h1>GraphQL API entrypoint</h1>'

app.add_url_rule(
    '/api',
    view_func=APIView.as_view()
)

if __name__ == '__main__':
    app.run()
