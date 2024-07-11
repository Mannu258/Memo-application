from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite3.db"
app.config["SECRET_KEY"] = "1234"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "No-reply@mojopanda.com"
app.config["MAIL_PASSWORD"] = "ekzr xoxk cmli cefa"

db = SQLAlchemy(app)
mail = Mail(app)


# Define your database model
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    from_person = db.Column(db.String(100), nullable=False)
    to_person = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)
    followup = db.Column(db.String(100), nullable=True)


class Crediantials(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.username}"


# Create the database tables
with app.app_context():
    db.create_all()


# Define your routes
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        # Retrieve form data
        date = request.form.get("date")
        From = request.form.get("from")
        TO = request.form.get("to")
        subject = request.form.get("subject")
        details = request.form.get("details")
        followup = request.form.get("followup")
        # all if else from condition
        first = ""

        if From == "SUSHANTO MITTRA (MANAGING DIRECTOR)":
            first = "sm@mojopanda.com"
        elif From == "KANTA GIRI (DIRECTOR)":
            first = "kg@mojopanda.com"
        elif From == "VIPIN KUMAR (MANAGER)":
            first = "vipin@mojopanda.com"
        elif From == "ABHISHEK KUMAR (MERCHANDISER)":
            first = "abhishek@mojopanda.com"
        elif From == "POOJA (HR)":
            first = "hr@mojopanda.com"
        elif From == "VINAY (ACCOUNTANT)":
            first = "accounts@mojopanda.com"
        elif From == "NITISH (EXECUTIVE)":
            first = "admin_3@mojopanda.com"

        # all else on to condition
        second = ""

        if TO == "MPE-0123 Abdul Kalam Khan":
            second = "Manager_Organic@mojopanda.com"
        elif TO == "MPE-0103 Abhishek Mittal":
            second = "abhishek@mojopanda.com"
        elif TO == "MPE-0113 Akash":
            second = "Admin_Mojo@mojopanda.com"
        elif TO == "MPE-0127 Arabaz Khan":
            second = "arabazkhan4312@gmail.com"
        elif TO == "MPE-0128 Dewanshu":
            second = "Dewanshu@mojopanda.com"
        elif TO == "MPE-0116 Jainder Singh Bhandari":
            second = "Bhandari.cert@mojopanda.com"
        elif TO == "MPE-0093 Kamlesh Singh":
            second = "hr@mojopanda.com"
        elif TO == "MPE-0029 Kanta Giri":
            second = "kg@mojopanda.com"

        elif TO == "MPE-0096 Kavita":
            second = "hr@mojopanda.com"
        elif TO == "MPE-0125 Mandeep Kumar Mishra":
            second = "mandeep_mis@mojopanda.com"
        elif TO == "MPE-0072 Mohan Singh":
            second = "hr@mojopanda.com"
        elif TO == "MPE-0102 Neeraj Kumar":
            second = "hr@mojopanda.com"
        elif TO == "MPE-0002 Nilam Devi":
            second = "hr@mojopanda.com"
        elif TO == "MPE-0118 Nitish Sharma":
            second = "admin_3@mojopanda.com"
        elif TO == "MPE-0115 Pooja":
            second = "hr@mojopanda.com"
        elif TO == "MPE-0112 Protap Chandra Dey":
            second = "hr@mojopanda.com"
        memo = Memo(
            date=date,
            from_person=From,
            to_person=TO,
            subject=subject,
            details=details,
            followup=followup
        )
        db.session.add(memo)
        db.session.commit()
        # first = "jeemannu90@gmail.com"
        # second = "mandeepkumarmannu123@gmail.com"
        try:
            msg = Message(
                subject,
                sender="No-reply@mojopanda.com",
                recipients=["sm@mojopanda.com", f"{first}", f"{second}"],
            )
            # msg = Message(subject, sender='No-reply@mojopanda.com', recipients=[f"mishramandeep@outlook.com"])

            msg.body = f"Date: {date}\nFrom: {From} (Reporter)\nTo: {TO}\nSubject: {subject}\nDetails: {details}\nFollow-Up: {followup}\n\nDear Employee,\n\nI hope this message finds you well. As part of our ongoing efforts, I wanted to share the following information:\n\n{details}\n\nPlease review and take any necessary actions. If you have any questions or need further clarification, feel free to reach out.\n\nThank you for your attention.\n\nBest regards,\nMojopanda Exim Pvt Ltd"

            mail.send(msg)
            print(f"Email sent to {TO} regarding {subject}")
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")
        print(date, From, TO, subject, details, followup)
        print(first, second)
        return render_template("thankyou.html")
    return render_template("index.html")


@app.route("/administrator", methods=["POST", "GET"])
def Admin():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["password"]
        admi = Crediantials.query.filter_by(
            username=username, password=password
        ).first()
        if admi:
            data = Memo.query.order_by(Memo.id.desc()).all()
            return render_template("Database.html", data=data)
        else:
            return render_template("login.html")

    return render_template("login.html")

@app.route("/delete/<int:id>")
def delete(id):
    query = Memo.query.filter_by(id=id).first()
    db.session.delete(query)  # Mark the user for deletion
    db.session.commit()
    return f"Memo with ID {id} has been successfully deleted."


if __name__ == "__main__":
    app.run(debug=True, port=8000)
