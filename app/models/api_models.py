from flask_restx import fields 
from __init__ import api


llm_api_model = api.model("Json Bodyです", {
    "key1": fields.String,
    "key2": fields.Integer,
    "key3": fields.Boolean,
})