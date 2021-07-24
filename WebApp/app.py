#!/home/linuxbrew/.linuxbrew/bin/python3
from flask import Flask, redirect, url_for, request, render_template, send_from_directory
from SpotifyClient import SpotifyClient

app = Flask(__name__)
sc = SpotifyClient()

#redirect to spotify
@app.route("/", methods=["GET"])
def root():
    redirect_link = sc.build_url()
    return redirect(redirect_link)

#awaiting token
@app.route('/homepage', methods=["GET","POST"])
def setup():
    if request.method == "GET":
        code = sc.return_code(request.url)
        payload = sc.authorize(code)
        data = sc.search_api(token=sc.access_token, query=input("query:\n"))
    return render_template("Welcome.html", data=data, token=sc.access_token)


if __name__ == "__main__":
    app.run(ssl_context=('certs/cert.pem', 'certs/key.pem'), host="0.0.0.0", port=443)

    


