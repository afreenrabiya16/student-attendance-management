from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from extensions import db
from models.student import Student

student_bp = Blueprint("student", __name__)


@student_bp.route("/test", methods=["GET"])
def test_student():
    return {
        "message": "Student route is working!"
    }, 200

@student_bp.route("/add", methods=["POST"])
@jwt_required()
def add_student():

    data = request.get_json()

    if not data:
        return {"message": "No data provided"}, 400

    required_fields = [
        "roll_number",
        "name",
        "department",
        "year",
        "section"
    ]

    for field in required_fields:
        if field not in data:
            return {"message": f"{field} is required"}, 400

    existing_student = Student.query.filter_by(
        roll_number=data["roll_number"]
    ).first()

    if existing_student:
        return {"message": "Roll number already exists"}, 409

    student = Student(
        roll_number=data["roll_number"],
        name=data["name"],
        department=data["department"],
        year=data["year"],
        section=data["section"]
    )

    db.session.add(student)
    db.session.commit()

    return {
        "message": "Student added successfully"
    }, 201

@student_bp.route("/all", methods=["GET"])
def get_students():

    students = Student.query.all()

    student_list = []

    for student in students:
        student_list.append({
            "id": student.id,
            "roll_number": student.roll_number,
            "name": student.name,
            "department": student.department,
            "year": student.year,
            "section": student.section
        })

    return student_list, 200

@student_bp.route("/<int:student_id>", methods=["GET"])
def get_student(student_id):

    student = db.session.get(Student, student_id)

    if not student:
        return {"message": "Student not found"}, 404

    return {
        "id": student.id,
        "roll_number": student.roll_number,
        "name": student.name,
        "department": student.department,
        "year": student.year,
        "section": student.section
    }, 200

@student_bp.route("/update/<int:student_id>", methods=["PUT"])
def update_student(student_id):

    student = db.session.get(Student, student_id)

    if not student:
        return {"message": "Student not found"}, 404

    data = request.get_json()

    if not data:
        return {"message": "No data provided"}, 400

    student.name = data.get("name", student.name)
    student.department = data.get("department", student.department)
    student.year = data.get("year", student.year)
    student.section = data.get("section", student.section)

    db.session.commit()

    return {
        "message": "Student updated successfully"
    }, 200

@student_bp.route("/delete/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    student = db.session.get(Student, student_id)

    if not student:
        return {"message": "Student not found"}, 404

    db.session.delete(student)
    db.session.commit()

    return {
        "message": "Student deleted successfully"
    }, 200