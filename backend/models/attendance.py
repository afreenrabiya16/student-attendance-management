from extensions import db


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(10),
        nullable=False
    )  # Present / Absent

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Attendance Student={self.student_id} Date={self.date}>"