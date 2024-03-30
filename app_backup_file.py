from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name") # ("name", "defaultvalue")
        return render_template("greet.html", name=name)
    else:
        return render_template("index.html")

# ANNOTATION:
# Form methods can be specified. e.g.: GET = args visible in url, POST = args not visible.
# POST needs to given in decorator as argument if used: methods=["POST",...] AND in the html form method.
# if you use "POST", use request.form.get instead of request.args.get


# @app.route("/greet", methods=["POST"])
# def greet():

# if __name__ == "__main__":
#     app.run()

