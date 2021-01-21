from flask import Flask, render_template, jsonify, abort, request
from flask_caching import Cache
from db import GithubDatabase

config = {"CACHE_TYPE": "simple"}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/', defaults={'page': 1}, methods=['GET'])
@app.route('/page/<int:page>')
@cache.cached(timeout=86400)
def home(page):
    if page > 0:
        return render_template(
            'users.html',
            users=get_users_from_db(page),
            page=page
        )
    else:
        abort(404)


@app.route('/api/profiles')
def get_data():
    gdb = GithubDatabase()
    params = request.args.to_dict()
    if "user" in params:  # Request for only one user
        user = gdb.get_username(params["user"])
        gdb.close()
        result = {
            "username": user[0][0],
            "id": user[0][1],
            "image_url": user[0][2],
            "type": user[0][3],
            "profile_url": user[0][4]
        }
        return jsonify(result)
    else:  # Request for all records available
        results = gdb.get_records(perpage=None)
        gdb.close()
        users = []
        for user in results:
            users.append(
                {
                    "username": user[0],
                    "id": user[1],
                    "image_url": user[2],
                    "type": user[3],
                    "profile_url": user[4]
                }
            )
        return jsonify(results=users, count=len(results))


def get_users_from_db(page, offset=25):
    """
        Utility function for the main site. It connects to the database to
        obtain specific chunk of records.
        Returns:
            - records. List of tuples with the user information recorded. E.g.:
            [('user', 1, 'img_url', 'User', 'profile_url'), (...)]
    """
    gdb = GithubDatabase()
    # Defining pagination depending on which page the user is on
    if page > 1:
        limit = (page - 1) * 25
    else:
        limit = 0
    records = gdb.get_records(limit, offset)
    gdb.close()
    return records


if __name__ == "__main__":
    app.run(debug=True)
