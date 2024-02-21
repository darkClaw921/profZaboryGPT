from flask_restx import Api, Resource, fields
from flask import Flask 
from amocrm.v2 import tokens
app = Flask(__name__)
api = Api(app, version='1.0', title='Strategies',)

@api.route('/s')
@api.doc(description='Возвращает список доступных стратегий')
class Get_strategies(Resource):
    def get(self):
        return [
  {
    "id": 1,
    "name": "ByBit",
    "url": "https://www.bybit.com/",
    "apiUrl": "https://bybit-exchange.github.io/docs/category/derivatives"
  },
  {
    "id": 2,
    "name": "Gate",
    "url": "gate.io",
    "apiUrl": "https://api.gateio.ws/api/v4"
  }
]
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5002')