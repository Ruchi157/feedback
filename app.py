# -*- coding: utf-8 -*-
# app.py

from flask import Flask, render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, IntegerField, StringField, \
        SubmitField


class StepForm(Form):
    """Subform.

    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    STEPS = StringField('Steps')
    

class MainForm(FlaskForm):
    """Parent form."""
    step01 = FieldList(
        FormField(StepForm),
        min_entries=1,
        max_entries=50
    )


# Create models
db = SQLAlchemy()


class Step01(db.Model):
    """Stores Feedback."""
    __tablename__ = 'Feedback'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    olmid = db.Column(db.String(100))
    manager = db.Column(db.String(100))
    team_name = db.Column(db.String(100))
    activity_name = db.Column(db.String(100)) 
    remarks = db.Column(db.String(100))

def __init__(self, name):
   self.name = name


class Feedback01(db.Model):
    """Stores step01 of a step02."""
    __tablename__ = 'Steps_Table'

    id = db.Column(db.Integer, primary_key=True)
    Feedback_id = db.Column(db.Integer, db.ForeignKey('Feedback.id'))

    STEPS = db.Column(db.String(100))

    # Relationship
    step02 = db.relationship(
        'Step01',
        backref=db.backref('step01', lazy='dynamic', collection_class=list)
    )



# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sosecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///q1.db'
db.init_app(app)
db.create_all(app=app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()
    MSG=""
    if form.validate_on_submit():
        # Create step02
        new_step02 = Step01(name=request.form.get("name"),olmid=request.form.get("olmid"),manager=request.form.get("manager"),team_name=request.form.get("team_name"),activity_name=request.form.get("activity_name"),remarks=request.form.get("remarks"))

        db.session.add(new_step02)

        for feedback01 in form.step01.data:
            new_feedback01 = Feedback01(**feedback01)

            # Add to step02
            new_step02.step01.append(new_feedback01)

        print(request.form)

        db.session.commit()
        MSG=" FEEDBACK SUBMITTED"
    Feedback = Step01.query
    print(Feedback)

    return render_template(
        'index.html',
        form=form,
        Feedback=Feedback,MSG=MSG
    )



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7050,threaded=True)  