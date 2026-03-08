from flask import Flask, jsonify, make_response, request
import time
import hashlib
import json

app = Flask(__name__)

students = {
    "1": {"name": "An", "major": "IT"},
    "2": {"name": "Bianh", "major": "Design"}
}

# Non cacheable
@app.route("/no-cache", methods=["GET"])
def get_time_no_cache():
    response = make_response(jsonify({
        "message": "Luôn luôn lấy dữ liệu mới nhất từ server",
        "server_time": time.time()
    }))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

# Cacheable 1
@app.route("/maxage-cached", methods=["GET"])
def get_students_maxage():
    response = make_response(jsonify({
        "data": students,
        "generated_at": time.time()
    }))
    
    response.headers["Cache-Control"] = "public, max-age=60"
    return response

# Cacheable 2
@app.route("/etag-cached", methods=["GET"])
def get_students_etag():
    data_str = json.dumps(students, sort_keys=True).encode('utf-8')
    current_etag = hashlib.md5(data_str).hexdigest()   # get current etag of data
    # client_etag = request.headers.get("If-None-Match") # get user etag
    if request.if_none_match.contains(current_etag):   # check
        print("using cache")
        response = make_response("", 304)
        return response
    response = make_response(jsonify(students), 200)
    response.set_etag(current_etag)
    return response

if __name__ == "__main__":
    app.run(port=5000)