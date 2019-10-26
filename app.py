# these contents can be put into a file called app.py
# and run by executing:
# python app.py

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    prediction = 0.5
    return jsonify({
        'prediction': prediction
    })

if __name__ == "__main__":
    app.run(debug=True)