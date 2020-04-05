# -*- coding: utf-8 -*-
# app.py

from flask import Flask, render_template
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
db.create_all(app=app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()

    if form.validate_on_submit():
        # Create step02
        new_step02 = Step01()

        db.session.add(new_step02)

        for feedback01 in form.step01.data:
            new_feedback01 = Feedback01(**feedback01)

            # Add to step02
            new_step02.step01.append(new_feedback01)

        db.session.commit()


    Feedback = Step01.query

    return render_template(
        'index.html',
        form=form,
        Feedback=Feedback
    )


@app.route('/<Feedback_id>', methods=['GET'])
def show_step02(Feedback_id):
    """Show the details of a step02."""
    step02 = Step01.query.filter_by(id=Feedback_id).first()

    return render_template(
        'show.html',
        step02=step02
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7050)  