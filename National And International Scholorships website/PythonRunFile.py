from flask import Flask, redirect,render_template, request
import os
import sqlite3
import json

currentlocation=os.path.dirname(os.path.abspath(__file__))
app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    return render_template("Login.html")

@app.route('/Options',methods=['POST','GET'])
def Options():
    return render_template("Options.html")

@app.route('/Register',methods=['POST','GET'])
def Register():
    return render_template("Register.html")

@app.route('/UserHistory',methods=['POST','GET'])
def UserHistory():
    sqlconnection=sqlite3.Connection(currentlocation+ "\DataDB.db")
    cursor=sqlconnection.cursor()
    cursor.execute("select * from {us}".format(us=currUser)) 
    data = cursor.fetchall() 
    return render_template("History.html",value=data)

@app.route('/International',methods=['POST','GET'])
def International():
    sqlconnection=sqlite3.Connection(currentlocation+ "\DataDB.db")
    cursor=sqlconnection.cursor()
    cursor.execute("select * from international") 
    data = cursor.fetchall() 
    return render_template("International.html",value=data)

@app.route('/array2python',methods=['POST','GET'])
def array2python():
    sqlconnection=sqlite3.Connection(currentlocation+ "\DataDB.db")
    cursor=sqlconnection.cursor()
    wordlist = json.loads(request.args.get('wordlist'))
    ln=len(wordlist)
    print(ln)
    print(currUser)
    for i in range(ln):
         checkrow="SELECT Name,Description FROM {t} WHERE Name='{LN}' and Description='{LP}'".format(t=currUser,LN=wordlist[i]['col1'],LP=wordlist[i]['col2'])
         rows=cursor.execute(checkrow)
         rows=rows.fetchall()
         if(len(rows)==0):
            Applieds="insert into {t} values('{e}','{u}')".format(t=currUser,e=wordlist[i]['col1'],u=wordlist[i]['col2'])
            cursor.execute(Applieds) 
    sqlconnection.commit()
    return render_template("Options.html")


@app.route('/National',methods=['POST','GET'])
def National():
    sqlconnection=sqlite3.Connection(currentlocation+ "\DataDB.db")
    cursor=sqlconnection.cursor()
    cursor.execute("select * from National") 
    data = cursor.fetchall() 
    return render_template("National.html",value=data)

@app.route('/Sports',methods=['POST','GET'])
def Sports():
    sqlconnection=sqlite3.Connection(currentlocation+ "\DataDB.db")
    cursor=sqlconnection.cursor()
    cursor.execute("select * from Sports") 
    data = cursor.fetchall() 
    return render_template("Sports.html",value=data)

@app.route('/LoginValidate',methods=['POST'])
def LoginValidate():
        LName=request.form.get('LgName')
        Lpassword=request.form.get('LgPassword')
        sqlconnection=sqlite3.Connection(currentlocation+ "\DataDB.db")
        global currUser
        currUser=LName
        cursor=sqlconnection.cursor()
        query1="SELECT Username,Password FROM Users WHERE Username='{LN}' and Password='{LP}'".format(LN=LName,LP=Lpassword)
        rows=cursor.execute(query1)
        rows=rows.fetchall()
        if(len(rows)==1):
             return render_template("Options.html")
        
        return render_template("Register.html")



@app.route('/RegisterValidate',methods=['GET','POST'])
def RegisterValidate():
    if request.method=="POST":
        RName=request.form.get('RName')
        REmail=request.form.get('REmail')
        RPassword=request.form.get('RPassword')
        sqlconnection=sqlite3.Connection(currentlocation+"\DataDB.db")
        cursor=sqlconnection.cursor()
        query2="SELECT Username,Password FROM Users WHERE Username='{LN}' and Password='{LP}'".format(LN=RName,LP=RPassword)
        rows=cursor.execute(query2)
        rows=rows.fetchall()
        if(len(rows)==1):
             return render_template("Register.html")
        query1="insert into Users values('{e}','{u}','{p}')".format(e=REmail,u=RName,p=RPassword)
        cursor.execute(query1)
        table2 = "create table if not exists '{t}'(Name text,Description text)".format(t=RName)
        cursor.execute(table2)
        
        sqlconnection.commit()
        return redirect("/")
    return render_template("Login.html")

if __name__=="__main__":
           app.run(debug=True)