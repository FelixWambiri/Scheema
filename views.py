import os
from flask import Flask, render_template, flash, url_for, logging, request, redirect
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from flask import send_from_directory

from forms import RegisterForm, AddSchemeForm
from models.accounts import Accounts
from models.user import User

UPLOAD_FOLDER = 'C:/Users/Shadow Master/PycharmProjects/Scheema/FileUploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', "png", 'jpeg', 'jpg', 'gif'}

app = Flask(__name__)
account = Accounts()
app.secret_key = '\xcd]\x1f\x8a\xa7\xd0J\xd6\x99\x8c/\x1e\x91~hU4tgd\xe5\xa2\xab3'

login_manager = LoginManager()
login_manager.init_app(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@login_manager.user_loader
def load_user(username):
    return account.get_specific_user(username)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if account.get_specific_user(form.username.data):
            flash("The user already exists", 'warning')
        else:
            user = User(form.username.data, form.email.data, form.password.data, form.confirm_password.data)
            account.add_new_user(user)
            flash("You are now registered and can login", 'success')
            return redirect(url_for('login'))

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_c = request.form['password']
        if account.get_specific_user(username):
            if password_c == account.get_specific_user(username).password:
                app.logger.info('Password Matched')
                login_user(account.get_specific_user(username))
                flash("You have logged in successfully", 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Password'
                return render_template("login.html", error=error)

        else:
            error = 'Invalid Username, The Username does not exist'
            return render_template("login.html", error=error)
    return render_template("login.html")


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    form = AddSchemeForm()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        app.logger.info('Method actually passes this test')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    return render_template("upload1.html", form=form)


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
