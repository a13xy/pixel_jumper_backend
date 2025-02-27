from flask import Flask, request, jsonify

from utils import load_data, save_data, LEVEL_CAPS, error_response

app = Flask(__name__)


@app.route("/create-user", methods=["POST"])
def create_user():
    data = load_data()
    login = request.args.get("login")
    password = request.args.get("password")

    if len(login) < 5:
        return jsonify(error_response("USERNAME_TOO_SHORT")), 400

    if len(password) < 8:
        return jsonify(error_response("PASSWORD_TO_SHORT")), 400

    if login in data:
        return jsonify(error_response("ACCOUNT_ALREADY_EXISTS")), 400

    data[login] = {"password": password, "level": 1.0, "high_score": 0}
    save_data(data)

    return jsonify({"status": "SUCCESS"}), 201

@app.route("/login", methods=["GET"])
def get_user():
    data = load_data()
    login = request.args.get("login")
    password = request.args.get("password")

    if login not in data:
        return jsonify(error_response("ACCOUNT_DO_NOT_EXIST")), 404

    if data[login]["password"] != password:
        return jsonify(error_response("WRONG_PASSWORD")), 404

    return jsonify({"status": "SUCCESS", "user_data": data[login]}), 200

@app.route("/change-password", methods=["PUT"])
def change_password():
    data = load_data()
    login = request.args.get("login")
    password = request.args.get("password")
    new_password = request.args.get("new_password")

    if login not in data:
        return jsonify(error_response("ACCOUNT_DO_NOT_EXIST")), 404

    if not new_password or len(new_password) < 8:
        return jsonify(error_response("PASSWORD_TOO_WEAK")), 400

    if data[login]["password"] != password:
        return jsonify(error_response("WRONG_PASSWORD")), 400

    data[login]["password"] = new_password
    save_data(data)

    return jsonify({"status": "SUCCESS"}), 200

@app.route("/provide-result", methods=["PUT"])
def provide_result():
    data = load_data()
    login = request.args.get("login")
    score = request.args.get("score")

    if login not in data:
        return jsonify(error_response("ACCOUNT_DO_NOT_EXIST")), 404

    current_lvl = data[login]["level"]
    current_cap = LEVEL_CAPS[int(current_lvl) - 1]

    try:
        score = int(score)
    except TypeError:
        return jsonify(error_response("WRONG_FORMAT"))

    data[login]["high_score"] = max(score, data[login]["high_score"])
    data[login]["level"] += score / current_cap

    save_data(data)

    return jsonify({"status": "SUCCESS"}), 200

@app.route("/delete-user", methods=["DELETE"])
def delete_user():
    data = load_data()
    login = request.args.get("login")
    password = request.args.get("password")

    if not login or not password:
        return jsonify(error_response("INCORRECT_CREDENTIALS")), 400

    if login not in data:
        return jsonify(error_response("ACCOUNT_DO_NOT_EXIST")), 404

    if data[login]["password"] != password:
        return jsonify(error_response("INCORRECT_CREDENTIALS")), 403

    del data[login]
    save_data(data)

    return jsonify({"status": "SUCCESS"}), 200




if __name__ == "__main__":
    app.run(debug=True)