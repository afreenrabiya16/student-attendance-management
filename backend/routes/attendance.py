from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required
from datetime import datetime

from extensions import db
from models.attendance import Attendance

attendance_bp = Blueprint("attendance", __name__)


@attendance_bp.route("/test", methods=["GET"])
def test_attendance():
    return {
        "message": "Attendance route is working!"
    }, 200

@attendance_bp.route("/mark", methods=["POST"])
@jwt_required()
def mark_attendance():

    data = request.get_json()

    attendance_date = datetime.strptime(
        data["date"],
        "%Y-%m-%d"
    ).date()

    existing_attendance = Attendance.query.filter_by(
        student_id=data["student_id"],
        date=attendance_date
    ).first()

    if existing_attendance:
        return {
            "message": "Attendance already marked for this student on this date."
        }, 400

    attendance = Attendance(
        student_id=data["student_id"],
        date=attendance_date,
        status=data["status"]
    )

    db.session.add(attendance)
    db.session.commit()

    return {
        "message": "Attendance marked successfully!"
    }, 201

@attendance_bp.route("/student/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student_attendance(student_id):

    attendance_records = Attendance.query.filter_by(
        student_id=student_id
    ).all()

    attendance_list = []

    for record in attendance_records:
        attendance_list.append({
            "id": record.id,
            "date": record.date.strftime("%Y-%m-%d"),
            "status": record.status
        })

    return {
        "student_id": student_id,
        "attendance": attendance_list
    }, 200

@attendance_bp.route("/date/<attendance_date>", methods=["GET"])
@jwt_required()
def get_attendance_by_date(attendance_date):

    attendance_date = datetime.strptime(
        attendance_date,
        "%Y-%m-%d"
    ).date()

    attendance_records = Attendance.query.filter_by(
        date=attendance_date
    ).all()

    attendance_list = []

    for record in attendance_records:
        attendance_list.append({
            "id": record.id,
            "student_id": record.student_id,
            "status": record.status
        })

    return {
        "date": attendance_date.strftime("%Y-%m-%d"),
        "attendance": attendance_list
    }, 200

@attendance_bp.route("/update/<int:attendance_id>", methods=["PUT"])
@jwt_required()
def update_attendance(attendance_id):

    attendance = Attendance.query.get(attendance_id)

    if not attendance:
        return {
            "message": "Attendance record not found."
        }, 404

    data = request.get_json()

    if "status" in data:
        attendance.status = data["status"]

    if "date" in data:
        attendance.date = datetime.strptime(
            data["date"],
            "%Y-%m-%d"
        ).date()

    db.session.commit()

    return {
        "message": "Attendance updated successfully!"
    }, 200

@attendance_bp.route("/delete/<int:attendance_id>", methods=["DELETE"])
@jwt_required()
def delete_attendance(attendance_id):

    attendance = Attendance.query.get(attendance_id)

    if not attendance:
        return {
            "message": "Attendance record not found."
        }, 404

    db.session.delete(attendance)
    db.session.commit()

    return {
        "message": "Attendance deleted successfully!"
    }, 200

@attendance_bp.route("/percentage/<int:student_id>", methods=["GET"])
@jwt_required()
def attendance_percentage(student_id):

    total_classes = Attendance.query.filter_by(
        student_id=student_id
    ).count()

    present_classes = Attendance.query.filter_by(
        student_id=student_id,
        status="Present"
    ).count()

    if total_classes == 0:
        return {
            "student_id": student_id,
            "attendance_percentage": 0
        }, 200

    percentage = round((present_classes / total_classes) * 100, 2)

    return {
        "student_id": student_id,
        "total_classes": total_classes,
        "present_classes": present_classes,
        "attendance_percentage": percentage
    }, 200

@attendance_bp.route("/summary/<int:student_id>", methods=["GET"])
@jwt_required()
def attendance_summary(student_id):

    total = Attendance.query.filter_by(student_id=student_id).count()

    present = Attendance.query.filter_by(
        student_id=student_id,
        status="Present"
    ).count()

    absent = Attendance.query.filter_by(
        student_id=student_id,
        status="Absent"
    ).count()

    percentage = 0

    if total > 0:
        percentage = round((present / total) * 100, 2)

    return {
        "student_id": student_id,
        "total_classes": total,
        "present": present,
        "absent": absent,
        "attendance_percentage": percentage
    }, 200