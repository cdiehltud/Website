from app import app
from flask import session,request,render_template,redirect,url_for

import couchdb, base64, time, config

from werkzeug.utils import secure_filename
from flask_wtf.file import FileField

couchserver = couchdb.Server(config.COUCHDB_URL)
dbname ="einfach_ambulant"
db = couchserver[dbname]

@app.route('/')
def login_html():
    if session.get('logged')==True:
        if session.get('user_type')=='Wundschwester':
            return render_template('w_home.html')
        if session.get('user_type')== 'PDL':
            return render_template('dashboard.html')
        if session.get('user_type')== 'Logo':
            return redirect(url_for("t_dashboard"))
        if session.get('user_type')== 'Ang':
            return redirect(url_for("a_home"))
        else:
            print('wrong')

    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    get_username = request.form['username']
    get_password = request.form['password']
    for doc in db:
        if db[doc].get("subject_Type") == "user":
            if get_username in db[doc]["username"]:
                id =db[doc].id
                if get_password ==db[id]["password"]:
                    session['logged'] = True
                    session['user_type'] = db[id]["user_type"]
                    session['username'] = request.form["username"]

    return login_html()

@app.route('/t_dashboard.html')
def t_dashboard():
    return render_template('t_dashboard.html')

@app.route('/a_home.html')
def a_home():
    return render_template('a_home.html')

@app.route('/a_home_patient.html')
def a_home_patient():
    return render_template('a_home_patient.html')

@app.route('/t_gesundheitszustand.html')
def t_gesundheitszustand():
    return render_template('t_gesundheitszustand.html')

@app.route('/t_patient.html')
def t_patient():
    return render_template('t_patient.html')

@app.route('/t_dashboard_patient.html')
def t_dashboard_patient():
    return render_template('t_dashboard_patient.html')

@app.route('/wund_kommunikation.html')
def wund_kommunikation():
    return render_template('wund_kommunikation.html')

@app.route('/ang_gesendet.html')
def ang_gesendet():
    return render_template('ang_gesendet.html')

@app.route('/w_gesundheitszustand.html')
def w_gesundheitszustand():
    return render_template('w_gesundheitszustand.html')

@app.route('/w_patient.html')
def w_patient():
    return render_template('w_patient.html')

@app.route('/w_dashboard_patient.html')
def w_dashboard_patient():
    return render_template('w_dashboard_patient.html')

@app.route('/ang_kommunikation.html')
def ang_kommunikation():
    return render_template('ang_kommunikation.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/a_dashboard.html')
def a_dashboard():
    return render_template('a_dashboard.html')

@app.route('/w_dokumentation.html')
def w_dokumentation():
    return render_template('w_dokumentation.html')

@app.route('/handle_patient', methods=['POST'])
def handle_patient():
    session.pop('patient_name', None)
    get_pat_name= request.form['patient_name']

    for doc in db:
        if db[doc].get("subject_Type") == "patient":
            print(db[doc]['patient_name'],"ok")
            print(get_pat_name)
            if get_pat_name == db[doc]['patient_name']:
                print("in patientname")
                print(db[doc]['patient_name'])
                session['patient_name']=get_pat_name
                id = db[doc].id
                pat_id = db[id]["pat_id"]
                for doc in db:
                    if db[doc]["subject_Type"] == "document":
                        if db[doc]["doc_type"] == "gesundheitszustand":
                            patient_id = db[doc]["pat_id"]
                            if patient_id == pat_id:
                                content = db[doc]["content"]
                                return render_template('Gesundheitszustand.html',patient_name=session['patient_name'],
                                                       content=content)
        else:
            print("in")
            return render_template('Gesundheitszustand.html', patient_name="wrong name",content=None)

@app.route('/handle_dashboard_patient/<name>')
def handle_dashboard_patient(name):
    session.pop('patient_name', None)
    session['patient_name'] = name
    '''for doc in db:
        if db[doc].get("subject_Type") == "patient":
            print(db[doc]['patient_name'],"ok")
            print(name)
            if name == db[doc]['patient_name']:
                session['patient_name']=name
                id = db[doc].id
                pat_id = db[id]["pat_id"]
                for doc in db:
                    if db[doc]["subject_Type"] == "document":
                        if db[doc]["doc_type"] == "gesundheitszustand":
                            patient_id = db[doc]["pat_id"]
                            if patient_id == pat_id:
                                content = db[doc]["content"]
                                return render_template('Gesundheitszustand.html',patient_name=session['patient_name'],
                                                       content=content)'''
    return redirect(url_for('gesundheitszustand'))


@app.route('/abmelden.html')
def abmelden():
    session.pop('username', None)
    session.pop('logged', None)
    return redirect(url_for('login_html'))

@app.route('/webchat.html')
def webchat():
    print("webchat")
    return render_template("webchat.html")

@app.route('/w_home.html')
def w_home():
    return render_template("w_home.html")

@app.route('/dokumentation.html')
def dokumentation():
    return render_template("dokumentation.html")

@app.route('/handle_modal_news',methods = ['GET', 'POST'])
def handle_modal_news():

    pat_name=request.form["select"]
    sender =session.get("username")
    receiver = request.form.get("checkbox1")
    topic= request.form["thema"]
    text= request.form.get("text")
    file =request.files.get("file").read()
    time_local= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    content={
        "doc_type": "news",
        "subject_Type": "document",
        "pat_name":pat_name,
        "sender":sender,
        "receiver":receiver,
        "topic":topic,
        "time":time_local,
        "text":text,
    }

    doc_id, doch_rev = db.save(content)
    doc = db.get(doc_id)
    db.put_attachment(doc, file, "file")

    if session.get('user_type')== 'Logo':
        return redirect(url_for("t_therapie_gesendet"))
    if session.get('user_type')== 'PDL':
        if receiver =="Frau Wolf":
            return redirect(url_for("therapie_kommunikation"))
        if receiver =="Frau Sommer":
            return redirect(url_for('kommunikation_main'))
        if receiver =="Tochter Regina":
            return redirect(url_for('ang_kommunikation'))
        else:
            return redirect(url_for("login"))
    if session.get('user_type') == 'Wundschwester':
        return redirect(url_for("w_kommunikation"))

    else:
        return redirect(url_for("login"))

@app.route('/handle_hochladen',methods = ['GET', 'POST'])
def handle_hochladen():
    print("hoch")
    pat_name = request.form["select"]
    file=request.files.get("file")
    k=file.read()
    content={
  "doc_type": "wundanamnese",
  "pat_name": pat_name,
  "user_name": session.get("username"),
  "time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
  "subject_Type": "document",
    "status":"new"}
    doc_id,doch_rev=db.save(content)
    doc=db.get(doc_id)
    db.put_attachment(doc,k,"wundanamnese")
    #######################################
    return redirect(url_for("meine_doku"))

@app.route('/Gesundheitszustand.html')
def gesundheitszustand():
    patient_name =session.get("patient_name")
    print(patient_name)
    for doc in db:
        if db[doc].get("subject_Type") == "patient":
            if patient_name in db[doc]["patient_name"]:
                id = db[doc].id
                pat_id = db[id]["pat_id"]
    for doc in db:
        if db[doc].get("subject_Type") == "document":
            if db[doc]["doc_type"]=="gesundheitszustand":
                patient_id =db[doc]["pat_id"]
                if patient_id ==pat_id:
                    content=db[doc]["content"]
    return render_template('Gesundheitszustand.html',patient_name=session.get("patient_name"),content=content)


@app.route('/w_kommunikation')
def w_kommunikation():
    news_array = []
    for doc in db:
        if db[doc].get("subject_Type") == "document":
            if db[doc]["doc_type"] == "news":
                # k = {}
                id = db[doc].id
                pat_name = db.get(id)["pat_name"]
                sender = db.get(id)["sender"]
                time = db.get(id)["time"]
                topic = db.get(id)["topic"]
                user = session.get("username")
                print(user)
                receiver = db.get(id)["receiver"]
                k = {"pat_name": pat_name, "sender": sender, "time": time, "topic": topic, "id": id,
                     "user": user, "receiver": receiver}
                news_array.append(k)
    return render_template('w_kommunikation.html',array=news_array)


@app.route('/kommunikation.html')
def kommunikation():
    return render_template('kommunikation.html')

@app.route('/a_kalender.html')
def a_kalender():
    return render_template('a_kalender.html')

@app.route('/a_gesundheitszustand.html')
def a_gesundheitszustand():
    return render_template('a_gesundheitszustand.html')

@app.route('/a_dokumentation.html')
def a_dokumentation():
    return render_template('a_dokumentation.html')

@app.route('/kommunikation_main.html')
def kommunikation_main():
    news_array = []
    for doc in db:
        if db[doc].get("subject_Type") == "document":
            if db[doc]["doc_type"] == "news":
                #k = {}
                id = db[doc].id
                pat_name = db.get(id)["pat_name"]
                sender = db.get(id)["sender"]
                time = db.get(id)["time"]
                topic=db.get(id)["topic"]
                user = session.get("username")

                receiver = db.get(id)["receiver"]
                k = {"pat_name": pat_name, "sender": sender, "time": time, "topic":topic,"id": id,
                     "user":user,"receiver":receiver}
                news_array.append(k)

    return render_template('kommunikation_main.html', array=news_array)

@app.route('/meine_doku.html')
def meine_doku():
    wundanamnese_array=[]
    k={}
    for doc in db:
        if db[doc].get("subject_Type") == "document":
            if db[doc]["doc_type"] == "wundanamnese":
                k={}
                id = db[doc].id
                pat_name=db.get(id)["pat_name"]
                user_name = db.get(id)["user_name"]
                time = db.get(id)["time"]
                #user = session.get("user_name")
                #receiver = db.get(id)["receiver"]
                k={"pat_name":pat_name,"user_name":user_name,"time":time,"id":id}
                wundanamnese_array.append(k)
    #print(wundanamnese_array)

    return render_template('meine_doku.html', array=wundanamnese_array)

@app.route('/nachricht.html/<id>/')
def nachricht(id):
    topic = db.get(id)["topic"]
    sender = db.get(id)["sender"]
    text = db.get(id)["text"]
    info = {"topic": topic, "sender": sender, "text": text}
    return render_template('nachricht.html',info=info)

@app.route('/patient.html')
def patient():
    return render_template('patient.html')

@app.route('/t_pflegekommunikation.html')
def t_pflegekommunikation():
    news_array = []
    for doc in db:
        if db[doc].get("subject_Type") == "document":
            if db[doc]["doc_type"] == "news":
                # k = {}
                id = db[doc].id
                pat_name = db.get(id)["pat_name"]
                sender = db.get(id)["sender"]
                receiver = db.get(id)["receiver"]
                time = db.get(id)["time"]
                topic = db.get(id)["topic"]
                user=session.get("username")

                k = {"pat_name": pat_name, "sender": sender, "time": time, "topic": topic,
                     "id": id,"receiver":receiver, "user":user}
                news_array.append(k)
    return render_template('t_pflegekommunikation.html', array=news_array)

@app.route('/t_nachricht.html/<id>/')
def t_nachricht(id):
    topic = db.get(id)["topic"]
    sender = db.get(id)["sender"]
    text =db.get(id)["text"]
    info ={"topic":topic,"sender":sender,"text":text}
    return render_template('t_nachricht.html',info=info, id=id)

@app.route('/gesendet')
def gesendet():

    return render_template('gesendet.html')

@app.route('/therapie_gesendet')
def therapie_gesendet():
    news_array = []
    for doc in db:
        if db[doc].get("subject_Type") == "document":
            if db[doc]["doc_type"] == "news":
                if db[doc]["sender"] == "Frau Pfleger":
                    id = db[doc].id
                    time = db.get(id)["time"]
                    pat_name = db.get(id)["pat_name"]
                    receiver = db.get(id)["receiver"]
                    topic = db.get(id)["topic"]
                    content={"id":id, "time":time,"pat_name":pat_name,"receiver":receiver,"topic":topic}
                    news_array.append(content)
    return render_template('therapie_gesendet.html',array=news_array)

@app.route('/therapie_kommunikation.html')
def therapie_kommunikation():
    news_array = []
    for doc in db:
        if db[doc].get("subject_Type") == "document":
            if db[doc]["doc_type"] == "news":
                # k = {}
                id = db[doc].id
                pat_name = db.get(id)["pat_name"]
                sender = db.get(id)["sender"]
                receiver = db.get(id)["receiver"]
                time = db.get(id)["time"]
                topic = db.get(id)["topic"]
                user = session.get("username")

                k = {"id":id,"pat_name": pat_name, "sender": sender, "time": time, "topic": topic,
                     "id": id, "receiver": receiver, "user": user}
                news_array.append(k)
    return render_template('therapie_kommunikation.html', array=news_array)

@app.route('/therapie_nachricht.html/<id>/')
def therapie_nachricht(id):
    topic = db.get(id)["topic"]
    sender = db.get(id)["sender"]
    text = db.get(id)["text"]
    info = {"topic": topic, "sender": sender, "text": text}
    return render_template('therapie_nachricht.html',info=info, id=id)


@app.route('/t_therapie_gesendet')
def t_therapie_gesendet():
    news_array = []
    for doc in db:
        if db[doc].get("subject_Type") == "document":
            if db[doc]["doc_type"] == "news":
                if db[doc]["sender"] == "Frau Wolf":
                    id = db[doc].id
                    time = db.get(id)["time"]
                    pat_name = db.get(id)["pat_name"]
                    receiver = db.get(id)["receiver"]
                    topic = db.get(id)["topic"]
                    content = {"id": id, "time": time, "pat_name": pat_name, "receiver": receiver, "topic": topic}
                    news_array.append(content)

    return render_template('t_therapie_gesendet.html',array=news_array)

@app.route('/w_dashboard.html')
def w_dashboard():
    return render_template('w_dashboard.html')

@app.route('/dashboard_patient.html')
def dashboard_patient():
    patient_name = []
    for doc in db:
        if db[doc].get("subject_Type") == "patient":
            id = db[doc].id
            pat_name = db.get(id)["patient_name"]

            patient_name.append(pat_name)
    print(patient_name)

    return render_template('dashboard_patient.html',pat_name=patient_name)

@app.route('/a_ang_gesendet.html')
def a_ang_gesendet():
    return render_template('a_ang_gesendet.html')

@app.route('/wund_doku.html')
def wund_doku():
    wundprotokoll_array = []
    k = {}
    for doc in db:
        if db[doc].get("subject_Type") == "document":
            if db[doc]["doc_type"] == "wundprotokoll":
                k = {}
                id = db[doc].id
                pat_name = db.get(id)["pat_name"]
                user_name = db.get(id)["user_name"]
                time = db.get(id)["time"]
                # user = session.get("user_name")
                # receiver = db.get(id)["receiver"]
                k = {"pat_name": pat_name, "user_name": user_name, "time": time, "id": id}
                wundprotokoll_array.append(k)

    return render_template('wund_doku.html', array=wundprotokoll_array)

@app.route('/w_nachricht.html/<id>/')
def w_nachricht(id):
    topic = db.get(id)["topic"]
    sender = db.get(id)["sender"]
    text =db.get(id)["text"]
    info ={"topic":topic,"sender":sender,"text":text}
    return render_template('w_nachricht.html',info=info)

@app.route('/wundanamnese.html/<id>/')
def wundanamnese(id):
    pat_name=db[id]["pat_name"]
    time = db[id]["time"]
    url="http://127.0.0.1:5984/einfach_ambulant/"+id+"/wundanamnese"
    return render_template('wundanamnese.html',url = url, pat_name=pat_name,time=time, id=id)

@app.route('/wundprotokoll.html/<id>/')
def wundprotokoll(id):
    pat_name = db[id]["pat_name"]
    time = db[id]["time"]
    url = "http://127.0.0.1:5984/einfach_ambulant/"+id +"/wundprotokoll"

    return render_template('wundprotokoll.html',url = url, pat_name=pat_name,time=time, id=id)

@app.route('/handle_delete/<id>/')
def handle_delete(id):
    db.delete(db.get(id))
    return redirect(url_for("meine_doku"))

@app.route('/handle_delete_news/<id>/')
def handle_delete_news(id):
    db.delete(db.get(id))
    return redirect(url_for("therapie_kommunikation"))

@app.route('/handle_delete_t_news/<id>/')
def handle_delete_t_news(id):
    db.delete(db.get(id))
    return redirect(url_for("t_pflegekommunikation"))




######### testcode ####################
@app.route('/test.html')
def test():
    return render_template('test.html')
#
########################################

def getUserParameter():
    return {
        "username": session["username"],
    }
