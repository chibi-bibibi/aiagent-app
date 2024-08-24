#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request
from flask_restx import Resource, Api, fields
# from .models.api_models import llm_api_model

from app.utils.groq import create_llm_answer


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
llm_api_model = api.model("LLM用Json Body", {
    "content": fields.String
})
@api.route("/llm-demo")
class Llm(Resource):
    @api.doc(body=llm_api_model)
    def post(self):
        body = request.json
        llm_answer = create_llm_answer(body["content"])
        return {"ans": llm_answer}

@api.route("/agent-demo")
class AiAgent(Resource):
    def get(self):
        llm_answer = create_llm_answer("What is 25 + 4 + 10?")
        agent_answer = run_conversation("What is 25 + 4 + 10?")
        print(agent_answer)
        return {
            "name": "Alice",
            "message": llm_answer
        }

from groq import Groq
import json

client = Groq()
MODEL = 'llama3-groq-70b-8192-tool-use-preview'

def calculate(expression):
    """Evaluate a mathematical expression"""
    try:
        # result = "This is Caculate Tool."
        result = eval(expression)
        print("result", result)
        return json.dumps({"result": result})
    except:
        return json.dumps({"error": "Invalid expression"})

def check_project_rank(expression):
    
    print(expression)
    try:
        result = {}
        str_len = len(expression)
        result["project_name"] = expression
        if str_len >= 10:
            result["rank"] = 3
            result["price"] = 100000
        elif str_len >= 5 and str_len < 10:
            result["rank"] = 2
            result["price"] = 50000
        else:
            result["rank"] = 1
            result["price"] = 10000
        print(result)
        return json.dumps({"result": result})
    
    except:
        return json.dumps({"result": result})



def run_conversation(user_prompt):
    messages=[
        {
            "role": "system",
            "content": "あなたは事務アシスタントです。適切な関数を使用して事務処理を実行し、日本語で結果を提供します。"
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "数式を評価する",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "評価する数式",
                        }
                    },
                    "required": ["expression"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "check_project_rank",
                "description": "プロジェクト情報を評価する",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "評価する文字列",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "calculate": calculate,
            "check_project_rank": check_project_rank
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                expression=function_args.get("expression")
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        print(messages)
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        print("koko1")
        print(second_response)
        return second_response.choices[0].message.content

user_prompt = "プロジェクト情報：CreateApp"
print(run_conversation(user_prompt))