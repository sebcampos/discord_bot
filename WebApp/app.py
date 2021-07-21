#!/home/linuxbrew/.linuxbrew/bin/python3
from flask import Flask, redirect, url_for, request, render_template, send_from_directory


app = Flask(__name__)



@app.route("/", methods=["GET"])
def root():
    return "running"

#awaiting token
@app.route('/post_me', methods=["GET","POST"])
def setup():
    if request.method == "POST" or request.method == "GET":
        print(request)
    return "<h1>Testing</h1>"


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=80)

    


