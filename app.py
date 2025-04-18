from flask import Flask,request,render_template,session,redirect,url_for
from flask_cors import CORS
from pymongo import MongoClient
import os
from cryptography.fernet import Fernet
const_key=b'1AZvA_UuJ2ih3Zz0FxTxAV0qH7ZZWhZybQ3UhVE2ekU='
client=MongoClient("mongodb+srv://janardhanarajesh2:6zWj8qTLoAfgqU9t@cluster0.2g0kyvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client["db"]
collection=db["user"]
app=Flask(__name__)
app.secret_key="jklsdjklf"
CORS(app)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/register")
def reg():
    return render_template("register.html",msg="register with your details")
@app.route("/submit" ,methods=["post"])
def submit():
    name=request.form["name"]
    unam=request.form["username"]
    pas=request.form["pass"]
    mail=request.form["email"]
    user=collection.find_one({"username":unam})
    doc={
         "name":name,
         "username":unam,
         "password":pas,
         "email":mail,

    }
 
    if user:
            return render_template("register.html",msg="user already found")
         
    else:
        user=collection.insert_one(doc)
        return render_template("login.html",msg="sucessfully registered")
            

    # print(name+"\n"+unam+"\n"+pas+"\n"+mail)
@app.route("/forgot")
def forgot():
     return render_template("forgot.html")
@app.route("/login")
def login():
    if session.get("name"):
        session.pop("name")
    return render_template("login.html",msg="login wit our details") 
@app.route("/check",methods=["post"])
def chec():
    name=request.form["uname"]
    session["name"]=name
    pas=request.form["pass"]
    dat=collection.find_one({"username":name,"password":pas})
    if dat:
        return (render_template("user.html",name=name,msg=f"hello ,{name}"))
    else:
        return render_template("login.html",msg="invalid username or password")
@app.route("/user",methods=["post"])
def user():
    name=session.get("name")
    if name:
        wn=request.form["wb"]
        ur=request.form["url"]
        pas=request.form["password"]
        dis=request.form["disc"]
        collection=db["info"]  
        chiper=Fernet(const_key)
        # text="rajesh".encode()
        ctext=chiper.encrypt(pas.encode())
        text=chiper.decrypt(ctext)
        print(ctext)
        print(text)
        doc={
            "user":name,
            "website":wn,
            "url":ur,
            "password":ctext,
            "discription":dis,
                    }
        ret=collection.find_one({"website":wn,"user":name})
        if ret:
            return render_template("user.html",msg="password already found")
        else:

            dat=collection.insert_one(doc)
            if dat:
                return render_template("user.html",msg="submited")
            else:
                return render_template("user.html",msg="try again")
    else:
        return render_template("login.html",msg="you have to login")

@app.route("/passes")
def passes():
    try:
        const_key = b'1AZvA_UuJ2ih3Zz0FxTxAV0qH7ZZWhZybQ3UhVE2ekU='
        chiper = Fernet(const_key)
        
        user = session.get("name")
        if not user:
            return render_template("login.html", msg="You have to login")

        collection = db["info"]
        user_data_cursor = collection.find({"user": user})
        user_data_list = list(user_data_cursor)

        if user_data_list:
            for item in user_data_list:
                try:
                    item["password"] = chiper.decrypt(item["password"]).decode()
                except Exception as decryption_error:
                    item["password"] = "Decryption failed"
                    print(f"Password decryption error: {decryption_error}")
            return render_template("password.html", words=user_data_list, user=user, msg="Browse your passwords")
        else:
            return render_template("password.html", msg="No passwords found", user=user)

    except Exception as e:
        print(f"Error in /passes route: {e}")
        return render_template("password.html", msg="An unexpected error occurred")

@app.route("/updat",methods=["post"])
def update():
    try:
        
        user=session["name"]
        website=request.form["wb"]
        url=request.form["url"]
        discription=request.form["dis"]
        password=request.form["pas"]
        collection=db["info"]
        chiper=Fernet(const_key)
        cp=chiper.encrypt(password.encode())
        print(website,url,discription,password)
    except Exception as e:
        return render_template("update.html",msg="try again")
    dat=collection.find_one_and_update({"user":user,"website":website},{"$set":{"website":website,"url":url,"discription":discription,"password":cp}})
    
    if dat:
        return redirect(url_for("ter"))
    else:
        return render_template("update.html",msg="try again")
@app.route("/update",methods=["post"])
def updat():
    user=session["name"]
    website=request.form["wb"]
    session["website"]=website
    url=request.form["url"]
    session["url"]=url
    discription=request.form["dis"]
    session["website"]=discription
    password=request.form["pas"]
    session["website"]=password
    # dat=collection.find_one_and_update({"name":user,"website":website},{"$set":{"website":website,"url":url,"discription":discription,"password":password}})
    
    # if dat:
    #     return render_template("update.html",msg="updated")
    # else:
    return render_template("update.html",website=website,url=url,password=password,discription=discription,msg="update your passwords")
@app.route("/logout")
def logout():
    try:
        if session.get("name"):
            session.pop("name")
        return render_template("login.html")
    except Exception as e:
        return render_template("login.html")
@app.route("/password")
def ter():
    return redirect(url_for("passes"))

if __name__=="__main__":
    app.run(debug=True)
