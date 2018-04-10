from app import app
from flask import session,request,render_template,flash,redirect,url_for
from test import UserTest

user = UserTest()
#user.create_table()
patient = [{"name":"Max Müller um 6:00 Uhr",},{"name":"Thomas Muster um 7:00 Uhr",}]
neu_patient = [{"name":"marie1",},{"name":"marie2",}]

@app.route('/document/list')
def doc_list():
   return "TODO list"

@app.route('/')
def login_html():
    if session.get('logged')==True:
        return render_template('logged.html')


@app.route('/login', methods=['POST'])
def login():
    print('in')
    print(request.args)
    get_username = request.form['username']
    get_password = request.form['password']
    password = user.query_table(get_username)
    print(get_password)
    print(password)
    if get_password == password:
        session['logged'] = True
        session['username'] = request.form["username"]
    else:
        session['logged'] = False
        flash('wrong password')

    return login_html()


def getUserParameter():
    return {
        "username": session["username"],
    }

@app.route('/test', methods=['POST'])
def test1():
    session["patient_name"] = request.form["myText"]

    return render_template('main_page.html', patient_name=session["patient_name"], **getUserParameter())

@app.route('/test1', methods=['GET','POST'])
def hello_world_test1():
    return render_template('logged.html',**getUserParameter())


@app.route('/test2', methods=['GET','POST'])
def hello_world_test2():
    select= 2
    print(select)
    return render_template('main_page.html',select=select,patient_name=session["patient_name"], **getUserParameter())

@app.route('/test3', methods=['GET','POST'])
def hello_world_test3():
    select= 3
    print(select)
    return render_template('main_page.html',select=select,patient_name=session["patient_name"], **getUserParameter())

@app.route('/test4', methods=['GET','POST'])
def hello_world_test4():
    select= 4
    print(select)
    return render_template('main_page.html',select=select,patient_name=session["patient_name"], **getUserParameter())

@app.route('/test5', methods=['GET','POST'])
def hello_world_test5():
    select= 5
    print(select)
    return render_template('main_page.html',select=select,patient_name=session["patient_name"], **getUserParameter())


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('logged', None)
    print(session)
    print('inlogout')
    return redirect(url_for('login_html'))