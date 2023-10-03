from flask import Flask, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cbddbdsbvvdkjfbvuvbfdu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.instance_path = 'C:/Users/HP/PycharmProjects/100-days-of-code/add-product/instance'
Bootstrap5(app)

db = SQLAlchemy()
db.init_app(app)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)


with app.app_context():
    db.create_all()


class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    descr = StringField('Product Description', validators=[DataRequired()])
    image = FileField('Product Image', validators=[DataRequired(),
                                                   FileAllowed(upload_set=['jpg', 'png', 'jpeg', 'svg', 'gif'],
                                                               message='Only images are allowed')])
    submit = SubmitField('Add Product')


@app.route('/', methods=['GET', 'POST'])
def add():
    form = AddProductForm()
    if form.validate_on_submit():
        product = db.session.query(Product).filter_by(name=form.name.data).first()
        if not product:
            product = Product(name=form.name.data,
                              description=form.descr.data,
                              image=form.image.data.read())
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', category='success')
            return redirect(url_for('add'))
        flash('A product on that name already exists', category='error')
        return redirect(url_for('add'))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
