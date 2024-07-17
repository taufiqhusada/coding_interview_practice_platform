from flask import jsonify

def convert_to_json_resp(content):
    data = {
            "data" : content,
        }
    return jsonify(data)