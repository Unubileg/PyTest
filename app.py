from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def add_student(students, data):
    students.append(data)
    save_students(students)

def remove_student(students, last_name):
    for student in students:
        if student["last_name"] == last_name:
            students.remove(student)
            save_students(students)
            return True
    return False

def modify_student(students, last_name, new_data):
    for student in students:
        if student["last_name"] == last_name:
            student.update(new_data)
            save_students(students)
            return True
    return False

def search_student(students, last_name):
    for student in students:
        if student["last_name"] == last_name:
            return student
    return None

def load_students():
    try:
        with open("students.json", "r") as file:
            students = json.load(file)
        return students
    except FileNotFoundError:
        return []

def save_students(students):
    with open("students.json", "w") as file:
        json.dump(students, file)

@app.route("/")
def index():
    students = load_students()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    students = load_students()
    data = {
        "last_name": request.form["last_name"],
        "first_name": request.form["first_name"],
        "id_number": request.form["id_number"],
        "major": request.form["major"],
        "email": request.form["email"]
    }
    add_student(students, data)
    return redirect(url_for("index"))

@app.route("/remove", methods=["POST"])
def remove():
    students = load_students()
    last_name = request.form["last_name"]
    if remove_student(students, last_name):
        return redirect(url_for("index"))
    return "Student not found."

@app.route("/modify", methods=["POST"])
def modify():
    students = load_students()
    last_name = request.form["last_name"]
    new_data = {
        "first_name": request.form["first_name"],
        "id_number": request.form["id_number"],
        "major": request.form["major"],
        "email": request.form["email"]
    }
    if modify_student(students, last_name, new_data):
        return redirect(url_for("index"))
    return "Student not found."

@app.route("/search", methods=["POST"])
def search():
    students = load_students()
    last_name = request.form["last_name"]
    student = search_student(students, last_name)
    if student:
        return render_template("student_details.html", student=student)
    return "Student not found."

@app.route("/upload_json", methods=["POST"])
def upload_json():
    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]
    if file.filename == "":
        return "No selected file"

    if file and file.filename.endswith(".json"):
        try:
            uploaded_data = json.load(file)
            if isinstance(uploaded_data, list):
                students = load_students()
                students.extend(uploaded_data)
                save_students(students)
                return redirect(url_for("index"))
            else:
                return "Invalid JSON format"
        except json.JSONDecodeError:
            return "Invalid JSON format"
    else:
        return "Please upload a JSON file"

if __name__ == "__main__":
    app.run(debug=True)
