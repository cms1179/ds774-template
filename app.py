from crypt import methods
from flask import Flask, redirect, render_template, request, url_for

from templates.admin import add_user, delete_record, edit_record, get_single_record, get_user

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/events")
def events():
    return render_template("events.html")


@app.route("/announcements")
def announcements():
    return render_template("announcements.html")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    msg_id = request.arg['id']
    if request.method == 'POST':
        if request.form.get('edit') == 'save':
            fname = request.form['fname']
            lname = request.form['lname']
            eaddress = request.form['eaddress']
            message = request.form['message']
            print(fname, lname, eaddress, message)
            edit_record(msg_id, fname, lname, eaddress, message)
            return redirect('/admin')

        elif request.form.get('edit') == 'cancel':
            return redirect('/admin')

        elif request.form.get('admin') == 'Delete':
            delete_record(msg_id)
            return redirect('/admin')

    entry = get_single_record(msg_id)

    return render_template('edit.html', record=entry)


@app.route("/documents")
def documents():
    return render_template("documents.html")


@app.route("/directory")
def directory():
    return render_template("directory.html")


@app.route("/issues")
def issues():
    return render_template("issues.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    error = False
    new_id = False

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if get_user(username):
            new_id = add_user(username, password)
            error = 'Registration successful. Please login.'
            return render_template ('admin.html', error = error)
        else:    
            error = "Username {username} is not available."

    return render_template('register.html', error = error, id = new_id)
    
