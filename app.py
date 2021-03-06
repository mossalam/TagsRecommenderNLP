from flask import Flask
import pandas as pd
from flask import render_template
from flask import request
from typing import Optional, Dict, Any, Union
from flask import jsonify
import FB_Model as fm


from ContentBased import ContentBased
app = Flask(__name__)
cb = ContentBased()


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/api/tags", methods = ['post', 'get'])
def getTags():
    title = request.args.get("title")
    body = request.args.get("body")

    if body is None or title is None:
        req = {"title": None, "body": None}
        res = {
        'tags':[],
        'req': req
        }

        return jsonify(res)

    tags = cb.getTags(title, body)

    if len(tags) < 20:
        text = cb.clean("{} {}".format(title, body))
        tags =  list(fm.get_ferq_with_txt(text, list(tags)))


    req = {"title": title, "body": body}

    res = {
    'tags': tags,

    'req': req
    }

    return jsonify(res)

if __name__ == "__main__":
    app.run()
