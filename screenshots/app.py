from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    priority = db.Column(db.String(10), nullable=False, default="Medium")
    priority_level = db.Column(db.Integer, default=2)

@app.route('/')
def index():
    # show all todos
    #todo_list = Todo.query.all()
    todo_list = Todo.query.order_by(Todo.priority_level.desc()).all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    task_priority = request.form.get("priority")

    priority_map = {
        "Low": 1,
        "Medium": 2,
        "High": 3
    }

    new_todo = Todo(title=title, complete=False, priority=task_priority, priority_level=priority_map[task_priority])
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # update item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # delete item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():   # <-- REQUIRED
        db.create_all()
    app.run(debug=True)

