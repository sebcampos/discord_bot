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
        print(request.url)
    return response.content


if __name__ == "__main__":
    app.run(ssl_context=("certs/cert.pem", "certs/key.pem") ,host="0.0.0.0", port=443)


    


