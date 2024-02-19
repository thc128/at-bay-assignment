import logging
from flask import Flask


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/status", methods=['GET','POST'])
def get_status():
    try:
        return {"status": "All is ok"}, 200
    except:
        logging.exception("An error occured")
        return {}, 500