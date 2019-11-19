from myproject import app, db
from flask import Flask, render_template, flash, request, session, url_for, redirect, abort
from flask_login import login_user, login_required, logout_user
from myproject.models import User, Product
from myproject.forms import LoginForm, RegiForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'Insert_random_string_here'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/logout')
@login_required
def logout():

    logout_user()
    flash('You are logged out!')
    return redirect(url_for('home'))


def create_example_data():

    state_model = Product(pname="Veg Shammie Kebab Sub(6 inch)", price=250)
    db.session.add(state_model)
    state_model = Product(pname="Chicken Teriyaki Sub (6 inch)", price=300)
    db.session.add(state_model)
    state_model = Product(pname="Corn and Peas Sub (6 inch)", price=150)
    db.session.add(state_model)
    state_model = Product(pname="Paneer Tikka Sub (6 inch)", price=350)
    db.session.add(state_model)
    state_model = Product(pname="Cheese, Egg and Ham Sub (6 inch)", price=200)
    db.session.add(state_model)
    state_model = Product(pname="Turkey and Ham Sub (6 inch)", price=200)
    db.session.add(state_model)

    try:
        db.session.commit()
    except IntegrityError as e:
        print("attempted to push data to database. Not first run. continuing\
                as normal")


@app.route('/addToCart')
def addToCart():
	productId = int(request.args.get('productId'))

    return


def populate_form_choices(registration_form):
    users = User.query.all()
    products = Product.query.all()
    user_names = []
    for u in users:
        user_names.append(User.username)

    state_choices = list(enumerate(user_names))
    product_names = []
    for p in products:
        product_names.append(Product.pname)
    country_choices = list(enumerate(product_names))
    # now that we've built our choices, we need to set them.
    registration_form.user_select_field.choices = state_choices
    registration_form.product_select_field.choices = country_choices


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in Successfully!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('home')

            return redirect(next)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegiForm()
    populate_form_choices(form)
    if form.validate_on_submit():

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/subs')
def subs():
    return render_template('subs.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


if __name__ == '__main__':
    app.run(debug=True)
