from flask import Flask, request, jsonify

from utils import load_data, save_data, LEVEL_CAPS, error_response

app = Flask(__name__)


@app.route("/create-user", methods=["POST"])
def create_user():
    data = load_data()
    login = request.args.get("login")
    password = request.args.get("password")

    if not login or not password:
        return jsonify({"error": "Login and password are required"}), 400

    if login in data:
        return jsonify({"error": "User already exists"}), 400

    data[login] = {"password": password, "level": 1.0, "high_score": 0}
    save_data(data)

    return jsonify({"message": "User created successfully"}), 201

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
        return jsonify({"error": "User not found"}), 404

    if not new_password:
        return jsonify({"error": "New password is required"}), 400

    if data[login]["password"] != password:
        return jsonify({"error": "Incorrect password!"}), 400

    data[login]["password"] = new_password
    save_data(data)

    return jsonify({"message": "Password updated successfully"}), 200

@app.route("/provide-result", methods=["PUT"])
def provide_result():
    data = load_data()
    login = request.args.get("login")
    score = request.args.get("score")

    if login not in data:
        return jsonify({"error": "User not found"}), 404

    current_lvl = data[login]["level"]
    current_cap = LEVEL_CAPS[int(current_lvl) - 1]

    try:
        score = int(score)
    except TypeError:
        return jsonify({"error": f"Wrong score format, received {type(score)} when needed int"})

    data[login]["high_score"] = max(score, data[login]["high_score"])
    data[login]["level"] += score / current_cap

    save_data(data)

    return jsonify({"message": "Profile results updated successfully"}), 200

@app.route("/delete-user", methods=["DELETE"])
def delete_user():
    data = load_data()
    login = request.args.get("login")
    password = request.args.get("password")

    if not login or not password:
        return jsonify({"error": "Login and password are required"}), 400

    if login not in data:
        return jsonify({"error": "User not found"}), 404

    if data[login]["password"] != password:
        return jsonify({"error": "Incorrect password"}), 403

    del data[login]
    save_data(data)

    return jsonify({"message": "User deleted successfully"}), 200




if __name__ == "__main__":
    app.run(debug=True)