from flask import Flask
from flask import redirect, url_for
from flask import render_template
from markupsafe import escape


app = Flask(__name__)  # __name__ -> 當前頁 面名稱

@app.route("/hello")
@app.route("/hello/<string:username>")
def say_hello(username=None):
    return render_template("hello.html",name=username)

@app.route("/for/<get_list>")
def li_list(get_list):
    return render_template("forlist.html",news=get_list)


@app.route("/joke")
def joke():
    return "<h1>There is JOKE! HaHa!</h1>"

@app.route("/<int:num>")
def add(num):
    return f"<h1>We get {num+100}</h1>"

@app.route("/add100/<int:getnum>")
def get_add(getnum):
    return redirect(url_for('add', num=getnum)) # url_for(route_function_name)

@app.route("/<string:fruit>")
def get_fruit(fruit):
    return f"<h1>We get {fruit}</h1>"

@app.route("/eat/<string:what_fruit>")
def eat_fruit(what_fruit):
    return redirect(url_for('get_fruit', fruit=what_fruit)) # url_for(route_function_name)

@app.route("/<float:a_float>")
def round_float(a_float):
    return f"<h1>{a_float} -> {round(a_float)}</h1>"

@app.route("/round/<float:get_float>")
def get_float(get_float):
    return redirect(url_for('round_float', a_float=get_float)) # url_for(route_function_name)


# @app.route('/')
# def index():
#     return redirect(url_for('login'))

# @app.route('/login')
# def login():
#     abort(401)

# command_ line下: flask --app flask_linebot.py run 執行程式
# 或是直接寫入
if __name__ == "__main__":
    app.run(debug = True)
