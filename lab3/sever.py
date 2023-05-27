from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def info():
    data = request.get_json()
    print(data)
    results = [
        {
            'title': "There's a shortage of truckers, but TuSimple thinks it has a solution: no driver needed - CNN",
            'summary': "The e-commerce boom has exacerbated a global truck driver shortage, but could autonomous trucks help fix the problem?",
            'matchRate': "90%",
            'url': "https://www.cnn.com/2021/07/14/world/tusimple-autonomous-truck-spc-intl/index.html"
        },
        {
            'title': "Result 2",
            'summary': 'Hide Caption 5 of 8 Photos: The robots running our warehousesAlthough not specifically designed for warehouses, Boston Dynamics\' dog-like robot "Spot" can lift objects, pick itself up after a fall, open and walk through doors, and even remind people to practice social distancing.',
            'matchRate': "85%",
            'url': "https://example.com/result2"
        },
        {
            'title': "Result 3",
            'summary': "Summary of result 3",
            'matchRate': "80%",
            'url': "https://example.com/result3"
        }
    ]
    return jsonify(results)


app.run(host='0.0.0.0', port=5000, debug=True)
