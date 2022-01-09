from sys import exec_prefix
from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, ToDo

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = ToDo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "Error in database adding."    
            
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Problem with task delete."


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task_to_update = ToDo.query.get_or_404(id)
    
    if request.method == "POST":
        task_to_update.content = request.form["content"]
        try:        
            db.session.commit()
            return redirect("/")
        except:
            return "Problem with task update."
    else:
        return render_template("update", task=task_to_update)
    

if __name__ == "__main__":
    app.run(debug=True)