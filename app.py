from flask import Flask, request, jsonify

app = Flask(__name__)

def add(a, b):
    return a + b

@app.route('/add')
def add_route():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    result = add(a, b)
    return jsonify({
        "a": a,
        "b": b,
        "operation": "add",
        "result": result
    })

if __name__ == '__main__':
    app.run(debug=True)
