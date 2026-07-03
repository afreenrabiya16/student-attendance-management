from extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    roll_number = db.Column(db.String(20), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)

    department = db.Column(db.String(100), nullable=False)

    year = db.Column(db.Integer, nullable=False)

    section = db.Column(db.String(10), nullable=False)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    attendance = db.relationship(
        "Attendance",
        backref="student",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student {self.roll_number}>"