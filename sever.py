from flask import Flask, jsonify, request
from flask_cors import CORS
from lab3.matchRate import TokenAnalyzer
from lab2.main import RetrievalModel

app = Flask(__name__)
CORS(app)

lab3_analyzer = TokenAnalyzer()
lab3_analyzer.load_data('./doucments/res_3.json')
lab2_analyzer = RetrievalModel('./doucments/DouLuo_Json')


@app.route('/', methods=['POST'])
def lab3():
    data = request.get_json()
    results = lab3_analyzer.get_results(data['query'])
    return jsonify(results)

@app.route('/lab2', methods=['POST'])
def lab2():
    data = request.get_json()
    print(data)
    results = lab2_analyzer.search(data['query'])
    return jsonify(results)


app.run(host='0.0.0.0', port=5000, debug=True)
