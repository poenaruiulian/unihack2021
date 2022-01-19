import json
import os
import sys

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
import bcrypt
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from manager.JsonManager import JsonManager
from manager.db import db_init, db
from model.CollectingPoints import CollectingPoints
from model.JsonDump import JsonDump
from model.models import Users, Contact, Container
from datetime import timedelta

load_dotenv()
app = Flask(__name__)

app.permanent_session_lifetime = timedelta(days=5)
app.secret_key = "gameover"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)


@app.route("/", methods=['POST', 'GET'])
def home():
    json_data = get_points()
    # User session for feed back, the 0 and 1 will be replaced
    if "userInSession" in session:
        style = "block"
        styleM = "none"
    else:
        style = "none"
        styleM = "block"

    if request.method == "POST":
        name = request.form['name']
        mail = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        saveInDB = Contact(
            name=name,
            mail=mail,
            subject=subject,
            message=message
        )
        db.session.add(saveInDB)
        db.session.commit()

    return render_template("home.html", json_data=json_data, styleOf=style, styleM=styleM)


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        mail = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        saveInDB = Contact(
            name=name,
            mail=mail,
            subject=subject,
            message=message
        )
        db.session.add(saveInDB)
        db.session.commit()
    return render_template("contact.html")


@app.route("/materials")
def materials():
    return render_template("materials.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    message = None

    if request.method == "POST":

        session.permanent = True

        username = request.form['username']
        mail = request.form['mail']
        password = request.form['password']
        retypedPassword = request.form['retypedPassword']

        selectAllUsers = Users.query.filter_by(username=username).first()

        if not selectAllUsers:

            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            if password == retypedPassword:
                addUserInDB = Users(
                    username=username,
                    password=hashed,
                    mail=mail
                )

                db.session.add(addUserInDB)
                db.session.commit()

                session['userInSession'] = username
                message = "Welcome"
            else:
                message = "The passwords don't match,Try again."
        else:
            message = "The username already exists."

    if message != None:
        flash(message)
    return render_template("signup.html")


@app.route("/signin", methods=['POST', 'GET'])
def signin():
    message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        selectUserFromDB = Users.query.filter_by(username=username).first()

        if selectUserFromDB:
            if bcrypt.checkpw(password.encode('utf-8'), selectUserFromDB.password):
                session["userInSession"] = username
                message = "Now you are signed in!"
                session.permanent = True
            else:
                message = "Password incorrect!"

    if message != None:
        flash(message)
    return render_template("signin.html")


@app.route("/signout")
def signout():
    if "userInSession" in session:
        session.pop("userInSession", None)
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/emptyCont" , methods=['POST','GET'])
def empty():
    style = 1
    if 'userInSession' in session:
        if request.method == 'POST':
            nameOfEmptyCan = request.form['name']
            percentOfCan = request.form['percent']
            latOfCan = request.form['lat']
            longOfCan = request.form['long']
            percentOfCan ="perc_" + percentOfCan[:len(percentOfCan)-1]

            selectContainerFromDB =  Container.query.filter_by(name=nameOfEmptyCan).first()

            if selectContainerFromDB:
                percents = ['perc_50' , 'perc_70' , 'perc_100']

                for i in range(len(percents)):
                    if percents[i] == percentOfCan:
                        x = i
                        break
                if x == 0:
                    selectContainerFromDB.perc_50 = selectContainerFromDB.perc_50 + 1
                    db.session.commit()
                elif x == 1:
                    selectContainerFromDB.perc_70 = selectContainerFromDB.perc_70 + 1
                    db.session.commit()
                elif x == 2:
                    selectContainerFromDB.perc_100 = selectContainerFromDB.perc_100 + 1
                    db.session.commit()
            else:
                saveInDB = Container(
                    name=nameOfEmptyCan,
                    perc_50 = 0, 
                    perc_70 = 0,
                    perc_100 = 0,
                    latit = latOfCan,
                    long = longOfCan
                )

                db.session.add(saveInDB)
                db.session.commit()

                
                selectContainerFromDB =  Container.query.filter_by(name=nameOfEmptyCan).first()

                percents = ['perc_50' , 'perc_70' , 'perc_100']

                for i in range(len(percents)):
                    if percents[i] == percentOfCan:
                        x = i
                        break
                if x == 0:
                    selectContainerFromDB.perc_50 = selectContainerFromDB.perc_50 + 1
                    db.session.commit()
                elif x == 1:
                    selectContainerFromDB.perc_70 = selectContainerFromDB.perc_70 + 1
                    db.session.commit()
                elif x == 2:
                    selectContainerFromDB.perc_100 = selectContainerFromDB.perc_100 + 1
                    db.session.commit()

    return render_template("home.html")


@app.route("/cityhall")
def cityhall():
    session["staff"] ="staff"
    if "staff" in session:
        key50 = 0
        allAt50 = {}
        fromDB50 = Container.query.with_entities(Container.name, Container.perc_50).all()
        for i in range(len(fromDB50)):
            if int(fromDB50[i][1]) >= 10:
                selectContainer = Container.query.filter_by(name=fromDB50[i][0]).first()
                allAt50[key50] = [selectContainer.name,selectContainer.latit,selectContainer.long] 
                key50+=1
        
        key70 = 0
        allAt70 = {}
        fromDB70 = Container.query.with_entities(Container.name, Container.perc_70).all()
        for i in range(len(fromDB70)):
            if int(fromDB70[i][1] >= 10):
                selectContainer = Container.query.filter_by(name=fromDB70[i][0]).first()
                allAt70[key70] = [selectContainer.name, selectContainer.latit, selectContainer.long]
                key70+=1
                

        key100 = 0
        allAt100 = {}
        fromDB100 = Container.query.with_entities(Container.name, Container.perc_100).all()
        for i in range(len(fromDB100)):
            if int(fromDB100[i][1] >= 10):
                selectContainer = Container.query.filter_by(name=fromDB100[i][0]).first()
                allAt100[key100] = [selectContainer.name, selectContainer.latit, selectContainer.long]
                key100+=1
                print(key100)
               

        return render_template("cityhallmap.html",env_key=os.getenv("GOOGLE_CLOUD_KEY"), 
            allAt50=allAt50, numberOf50=key50, 
            allAt70=allAt70, numberOf70=key70, 
            allAt100=allAt100, numberOf100=key100)

@app.route("/get_points", methods=['POST', 'GET'])
def get_points():
    json_manager = JsonManager(
        'https://data.primariatm.ro/api/3/action/datastore_search?resource_id=d0134630-84d9-40b8-9bcb-dfdc926d66ab'
        '&limit=500')
    jd = JsonDump.from_json(json_manager.connect())
    collecting_list = []
    for item in jd.return_records():
        cp = CollectingPoints(item["_id"], item["id"], item["tip colectare"], item['adresa'], item['companie'],
                              item['website'], item['latitudine'], item['longitudine'])
        cp_string = json.dumps(cp.__dict__)
        cp_json = json.loads(cp_string)
        collecting_list.append(cp_json)
    return json.dumps(collecting_list)


if __name__ == "__main__":
    app.run(debug=True)
