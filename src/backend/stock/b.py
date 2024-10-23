from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Use a better structure for storing data in production.
posted_data = ""

# POST: Receive and store data from the user
@app.route('/post', methods=['POST'])
def post_data():
    global posted_data
    if request.is_json:  # Check if the request contains valid JSON
        data = request.json.get('info')  # Extract 'info' from the JSON body
        if data:
            posted_data = data  # Store the data
            return jsonify({'message': 'Oke con dê'}), 200
        else:
            return jsonify({'message': 'Thông tin không hợp lệ'}), 400
    else:
        return jsonify({'message': 'Request không có JSON hợp lệ'}), 400

# GET: Return the previously posted information
@app.route('/', methods=['GET'])
def get_data():
    if posted_data:
        return jsonify({'posted_info': posted_data}), 200
    else:
        return jsonify({'message': 'Chưa có thông tin nào được post'}), 204  # No Content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
