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


@app.route("/issues", methods=['GET', 'POST'])
def issues():
    # If method was POST, a form was submitted
    if request.method == 'POST':

        # If the form was Login, perform log in steps
        if request.form.get('issues') == 'Login':
            username = request.form['username']
            password = request.form['password']

            # pass username and password from form to our login logic
            result = login_user(username, password)

            # If login was successful, create a session for the user, and load data, show data onpage
            if result:
                session['user_id'] = result
                records = get_records()
                # print(records)

            # login was not sucessful, show error message
            else:
                error = 'Invalid Username or Password'

        # if form was logout button, end user session
        elif request.form.get('issues') == 'Logout':
            session.pop('user_id')

    # if user is logged in previously, show data. If no session, data is not retireved
    if 'user_id' in session:
        records = get_records()

    # return the issues page, showing any message or data that we may have
    return render_template('issues.html', error=error, records=records)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    error = ''
    records = ''
    print(request)

    # If method was POST, a form was submitted
    if request.method == 'POST':

        # If the form was Login, perform log in steps
        if request.form.get('admin') == 'Login':
            username = request.form['username']
            password = request.form['password']

            # pass username and password from form to our login logic
            result = login_user(username, password)

            # If login was successful, create a session for the user, and load data, show data onpage
            if result:
                session['user_id'] = result
                records = get_records()
                # print(records)

            # login was not sucessful, show error message
            else:
                error = 'Invalid Username or Password'

        # if form was logout button, end user session
        elif request.form.get('admin') == 'Logout':
            session.pop('user_id')

    # if user is logged in previously, show data. If no session, data is not retireved
    if 'user_id' in session:
        records = get_records()

    # return the admin page, showing any message or data that we may have
    return render_template('admin.html', error=error, records=records)


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
            return render_template('admin.html', error=error)
        else:
            error = f"Username {username} is not available."

    return render_template('register.html', error=error, id=new_id)
