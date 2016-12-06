"""Main View for Database queries and listing."""
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


from flask import (Blueprint,
                   current_app,
                   jsonify,
                   request)

from sql_json_bridge.config import load_database_configs

legacy = Blueprint('legacy', __name__)


def get_database_config(database_name):
    for db in current_app.config["DATABASES"]:
        if db.match(database_name) is not None:
            return current_app.config["DATABASES"][db]


@legacy.route("/query/<database_name>")
@legacy.route("/update/<database_name>")
def run_query(database_name):
    # TODO: Write something...
    db = get_database_config(database_name).driver
    if db is None:
        return jsonify(
            ERROR="Could not find matching database."
        )

    data = request.get_json(silent=True)
    if data is not None and "sql" in data:
        sql = data["sql"]
    else:
        sql = request.values.get('sql')
    if sql is None:
        return jsonify(ERROR="SQL query missing from request."), 400

    try:
        result = db.run_query(sql)
    except Exception as e:
        return jsonify(ERROR=": ".join(str(i) for i in e.args)), 422

    return jsonify(result=result)


@legacy.route("/list")
def list():
    load_database_configs(
        current_app.config["DATABASE_CONFIG_LOCATION"]
    )
    configs = current_app.config["DATABASES"].values()
    return jsonify(str(config["identifier"]) for config in configs)
