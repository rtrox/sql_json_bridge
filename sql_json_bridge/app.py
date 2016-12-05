"""SQL JSON Bridge"""
# Copyright (C) 2016 Russell Troxel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging

from logging.handlers import TimedRotatingFileHandler

from config import load_database_configs

from flask import Flask, jsonify

from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions

DEFAULT_BLUEPRINTS = []


def make_json_error(ex):
    """
    Return a jsonified default http error code.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    response = jsonify(message=str(ex))
    response.status_code = (ex.code
                            if isinstance(ex, HTTPException)
                            else 500)
    return response


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""
    if app.config.get("LEGACY_SUPPORT", False):
        from legacy.views import legacy
        blueprints.append(legacy)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_app(app):
    """Retrieve App Configuration."""
    app.config.from_object('default_config')
    try:
        app.config.from_envvar('SQL_JSON_BRIDGE_CONFIG')
    except:
        pass

    load_database_configs(
        app.config.get("DATABASE_CONFIG_LOCATION")
    )

    # for code in default_exceptions.iterkeys():
    #     app.error_handler_spec[None][code] = make_json_error


def configure_logging(app):
    """Add Rotating Handler to app."""
    logfile = app.config.get('LOG_FILE')
    handler = TimedRotatingFileHandler(
        logfile,
        when="D",
        interval=1,
        backupCount=14,
        utc=True
    )
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)


def create_app(app_name=None, blueprints=None):
    """Create the flask app."""
    if app_name is None:
        app_name = "sql_json_bridge"
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name)

    configure_app(app)
    configure_logging(app)

    configure_blueprints(app, blueprints)

    return app



if __name__ == "__main__":
    app = create_app(app_name=__name__)
    app.run(host="0.0.0.0", port=5000, debug=True)
