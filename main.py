from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import InputRequired
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
db = SQLAlchemy()

bootstrap = Bootstrap5(app)

db_name = 'cafes.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
db.init_app(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String, unique=True, nullable=False)
    img_url = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String(250), unique=False, nullable=False)
    has_sockets = db.Column(db.Integer, unique=False, nullable=False)
    has_toilet = db.Column(db.Integer, unique=False, nullable=False)
    has_wifi = db.Column(db.Integer, unique=False, nullable=False)
    can_take_calls = db.Column(db.Integer, unique=False, nullable=False)
    seats = db.Column(db.String(250), unique=False, nullable=False)
    coffee_price = db.Column(db.String(250), unique=False, nullable=False)

class AddForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    map_url = URLField("Map URL", validators=[InputRequired()])
    img_url = URLField("Image URL", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired()])
    has_sockets = StringField("Has sockets? (0 for no / 1 for yes)", validators=[InputRequired()])
    has_toilet = StringField("Has toilet? (0 for no / 1 for yes)", validators=[InputRequired()])
    has_wifi = StringField("Has wifi? (0 for no / 1 for yes)", validators=[InputRequired()])
    can_take_calls = StringField("Can take calls? (0 for no / 1 for yes)", validators=[InputRequired()])
    seats = StringField("Seats (eg: 20-30)", validators=[InputRequired()])
    coffee_price = StringField("Coffee price (eg: £2.75)", validators=[InputRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def show_cafes():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template('cafes.html', cafes=cafes)

@app.route('/add_cafe', methods=["GET", "POST"])
def add_cafe():
    form = AddForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            has_sockets = form.has_sockets.data,
            has_toilet = form.has_toilet.data,
            has_wifi = form.has_wifi.data,
            can_take_calls = form.can_take_calls.data,
            seats = form.seats.data,
            coffee_price = form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("show_cafes"))
    return render_template('add_cafe.html', form=form)

@app.route('/delete_cafe')
def delete_cafe():
    cafe_id = request.args.get("id")
    cafe = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for("show_cafes"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
