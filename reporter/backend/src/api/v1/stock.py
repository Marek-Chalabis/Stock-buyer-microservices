from flask.views import MethodView
from flask import Flask, jsonify, request
from api.v1.tasks import divide
class Stock(MethodView):
    def post(self):
        #new_language_name = request.json()
        print(request.json)
        divide.delay()
    def get(self):
        return {'dasd': 123}