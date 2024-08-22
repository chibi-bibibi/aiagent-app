#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request
from flask_restx import Resource, Api


#Flaskオブジェクトの生成
app = Flask(__name__)
api = Api(app)

# #「/」へアクセスがあった場合に、"Hello World"の文字列を返す
# @app.route("/")
# def hello():
#     # return "Hello World!"
#     return render_template("main.html")

# #「/index」へアクセスがあった場合に、「index.html」を返す
# @app.route("/index")
# def index():
#     return render_template("index.html")

@api.route("/agent-demo")
class AiAgent(Resource):
    def get(self):
        return {
            "name": "Alice",
            "message": "Hello World"
        }