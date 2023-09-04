import pathlib
from urllib.parse import urlparse

import bcrypt
import pymongo
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response, session

from configuration import load_config
from helpers.account import is_strong_password, generate_profile_image, hash_password

app = Flask(__name__)
config = load_config()
app.secret_key = config["secret_key"]
uri = f"mongodb+srv://{config['username']}:{config['password']}@cluster0.stl7rpk.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
database = client.get_database(config["database"])
records = database.get_collection(config["storage_collection"])


@app.route("/")
def dashboard():
    if "username" in session:
        shared_files = records.find({})
        files = []
        for shared_file in shared_files:
            title = shared_file["title"]
            filename = shared_file["filename"]
            extension = shared_file["extension"]
            file_id = shared_file["_id"]
            parsed_url = urlparse(request.base_url)
            file_url = f"{parsed_url.scheme}://{parsed_url.hostname}/share/{file_id}"
            files.append({
                "file_id": file_id,
                "title": title,
                "filename": filename,
                "extension": extension,
                "file_url": file_url
            })

        return render_template("dashboard.html", files=files)
    else:
        return redirect(url_for("login"))


@app.route("/upload_file")
def upload_file():
    if "username" in session:
        return render_template("file_share.html")

    return redirect(url_for("login"))


@app.route("/delete", methods=["GET"])
def delete_file():
    if "username" in session:
        if request.method == "GET":
            file_id = request.args.get("id")
            records.delete_one({"_id": ObjectId(file_id)})
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


@app.route("/share/<file_id>")
def share_page(file_id):
    file = records.find_one({"_id": ObjectId(file_id)})
    filename = file["filename"]
    size = round(len(file["file"]) / 1048576, 2)
    extension = file["extension"]
    data = {"filename": filename, "size": size, "extension": extension, "file_id": file_id}
    return render_template("download.html", file=data)


@app.route("/download/<file_id>")
def download_file(file_id):
    file = records.find_one({"_id": ObjectId(file_id)})
    file_binary = file["file"]
    filename = file["filename"]
    response = make_response(file_binary)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@app.route("/upload", methods=["POST"])
def upload():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        share_title = request.form.get("share_title")
        submitted_file = request.files.get("file")

        if submitted_file.filename == "":
            message = {
                "status": "danger",
                "icon": "error",
                "message": "The file provided doesn't have a valid filename.",
                "success": False
            }
            return render_template("file_share_result.html", message=message)

        binary_file = submitted_file.read()
        if len(binary_file) > 5242880:  # If file is bigger than 5MB
            message = {
                "status": "danger",
                "icon": "error",
                "message": "The file exceeds the size limit of 5MB.",
                "success": False
            }
            return render_template("file_share_result.html", message=message)

        filename = submitted_file.filename
        extension = pathlib.Path(filename).suffix

        data = {
            "title": share_title,
            "file": binary_file,
            "filename": filename,
            "extension": extension,
        }
        result = records.insert_one(data)
        if result.acknowledged:
            message = {
                "status": "success",
                "icon": "success",
                "message": "The file has successfully been uploaded.",
                "success": True
            }
            return render_template("file_share_result.html", message=message)
        else:
            message = {
                "status": "danger",
                "icon": "error",
                "message": "Couldn't upload file. Please try again.",
                "success": False
            }
            return render_template("file_share_result.html", message=message)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")
        accounts = database.get_collection(config["account_collection"])
        user_found = accounts.find_one({"username": username})
        if user_found:
            message = "This username already exists."
            return render_template("register.html", message=message)

        if password != password_confirmation:
            message = "Passwords do not match."
            return render_template("register.html", message=message)

        if is_strong_password(password):
            profile_image = generate_profile_image()
            hashed_password = hash_password(password)
            account_data = {
                "username": username,
                "password": hashed_password,
                "profile_image": profile_image
            }
            accounts.insert_one(account_data)
            return redirect(url_for("login"))
        else:
            message = "The password's strength is weak."
            return render_template("register.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        accounts = database.get_collection(config["account_collection"])
        account = accounts.find_one({"username": username})
        if not account:
            message = "This user doesn't exist."
            return render_template("login.html", message=message)

        remote_password = account["password"]
        if bcrypt.checkpw(password.encode("utf-8"), remote_password):
            session["username"] = account["username"]
            return redirect(url_for("dashboard"))
        else:
            message = "Wrong password. Please try again."
            return render_template("login.html", message=message)


@app.route("/profile")
def profile():
    if "username" in session:
        username = session["username"]
        accounts = database.get_collection(config["account_collection"])
        account = accounts.find_one({"username": username})
        profile_image = account["profile_image"].decode()
        account_data = {"username": username, "profile_image": profile_image}
        return render_template("profile.html", account_data=account_data)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("email", None)
        session.pop("username", None)
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()
