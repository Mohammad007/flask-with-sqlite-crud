from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crud.sqlite"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.email


@app.route('/')
def home():
    user = User.query.all()
    user_edit = ''
    return render_template('index.html', user=user, user_edit=user_edit)

@app.route('/add', methods=["POST"])
def add():
    if request.form:
        user = User(name=request.form.get("name"), email=request.form.get("email"), address=request.form.get("address"))
        db.session.add(user)
        db.session.commit()
    return redirect('/')

@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    id = id
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET"])
def edit(id):
    id = id
    user_edit = User.query.filter_by(id=id).first()
    user = User.query.all()
    return render_template('index.html', user=user, user_edit=user_edit)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    name = request.form.get("name")
    email = request.form.get("email")
    address = request.form.get("address")
    id = id
    user = User.query.filter_by(id=id).first()
    user.name = name
    user.email = email
    user.address = address
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
