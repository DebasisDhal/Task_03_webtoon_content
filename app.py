import os

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'xdfjdfkl'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///webtoon.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize db and jwt
db = SQLAlchemy(app)


class Webtoon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image_path = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Webtoon {self.title}>'

# Create all tables
with app.app_context():
    db.create_all()

# @app.route("/")
# def home():
#     return render_template("home.html")

@app.route('/add', methods=['GET'])
def add_webtoon_form():
    return render_template('add.html')


## Route to add a new webtoon without requiring a JWT token
@app.route('/webtoons', methods=['POST'])
def add_webtoon():
    data = request.form
    image_file = request.files['image']

    # Save the image to the upload folder
    if image_file:
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)
    else:
        image_path = None

    # Create a new Webtoon entry without the characters field
    new_webtoon = Webtoon(
        title=data['title'],
        description=data['description'],
        image_path=image_path
    )

    db.session.add(new_webtoon)
    db.session.commit()

    flash('Webtoon added successfully!', 'success')
    return redirect(url_for('add_webtoon_form'))  # Redirect to the form page after adding

# Route to display all webtoons with their images
@app.route('/', methods=['GET'])
def webtoon_list():
    webtoons = Webtoon.query.all()  # Fetch all webtoons from the database
    return render_template('home.html', webtoons=webtoons)


if __name__ == "__main__":
    app.run(debug = True)