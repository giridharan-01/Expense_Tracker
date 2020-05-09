from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy   
from datetime import datetime
import sqlite3

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///exp.db'
db=SQLAlchemy(app)

class Exp(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    amount=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        desc=request.form['desc']
        amt=request.form['amount']
        new_exp=Exp(name=desc,amount=amt)

        try:
            db.session.add(new_exp)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error in adding the expense'
    
    else:
        info=Exp.query.order_by(Exp.date_created).all()
        return render_template('index.html',info=info)

@app.route('/total',methods=['POST'])

def total():
    if request.method=='POST':
        info=Exp.query.order_by(Exp.date_created).all()
        # return render_template('total.html',info=info)
        tot=0
        for i in info:
            tot+=int(i.amount)
        return render_template('total.html',tot=tot)
    else:
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    to_del=Exp.query.get_or_404(id)

    try:
        db.session.delete(to_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error in deleting the expense'

if __name__ == "__main__":
    app.run(debug=True)