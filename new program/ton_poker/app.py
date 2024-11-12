from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('client', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('client', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 