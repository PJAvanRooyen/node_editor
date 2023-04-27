from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/increment', methods=['POST'])
def increment():
    value = request.json['value']

    # Increment the value by 1
    result = int(value) + 1

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)
