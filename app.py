from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"
    



# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route('/',methods=['GET', 'POST'])
def hello_world():

    if request.method == 'POST':
        print("post request")
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()

    # this renders html page when we start the application'
    return render_template('index.html',allTodo=allTodo)


@app.route('/products')
def products():
    return 'this is a list of products'

@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "Show called"

@app.route('/update/<int:sno>',methods=['POST','GET'])
def update(sno):
    if request.method=='POST':
        print("Update request")
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()

    allTodo = Todo.query.all()
    # return render_template('index.html',allTodo=allTodo)
    # return "Delete called"
    return redirect('/')




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True,port=8000)
