from flask import Flask, jsonify, request
from flask_cors import CORS
from matchRate import TokenAnalyzer


app = Flask(__name__)
CORS(app)
analyzer = TokenAnalyzer()
analyzer.load_data('res_3.json')

@app.route('/', methods=['POST'])
def info():
    data = request.get_json()
    results = analyzer.get_results(data['query'])
    return jsonify(results)


app.run(host='0.0.0.0', port=5000, debug=True)
