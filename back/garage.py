from enum import Enum
import json
import os 
from flask import Flask,render_template,request
from icecream import ic 

def clear_screen(): 
    os.system("cls")
app = Flask(__name__)
loged_user = "" 
users = []
@app.route("/")
def home_page():
    return render_template("home_page.html", loged_user = loged_user)

@app.route("/login", methods = ["GET","POST"])

def login():
    global loged_user
    if request.method == "POST" :
        username = request.form["username"]
        pwd = request.form["password"]
        try:
            with open("my_users.json","r") as file:
                users = json.load(file)
        except:
            msg = "there are no current users please sign up first"
            return render_template("signup.html", msg =msg)        
        for user in users:
            if username == user["username"] and pwd == user["pwd"]:
                loged_user = username
                return render_template("home_page.html",loged_user= loged_user,user = user)
        msg = "the username or password are not correct"
        ic(msg)
        return render_template("login.html", msg = msg)
    ic("sumthing went wrong")
    return render_template("login.html")
    

@app.route("/signup", methods =["POST","GET"])
def signup():
    global loged_user
    if request.method == "POST":
        username = ic(request.form["username"])
        email = ic(request.form["email"])
        phone_num = request.form["phone_num"]
        pwd = ic(request.form["password"])
        if len(username) > 3 and len(pwd) > 5: 
            for user in users:
                if user["username"] == username:
                    msg = "username already in use please choose a different one"
                    return render_template("signup.html", msg = msg)  
            users.append({"cars":[],"phone_num":phone_num,"email":email,"pwd":pwd,"username":username})
            ic(users)
            loged_user = username
            with open("my_users.json","w") as file:
                json.dump(users,file) 
            return render_template("home_page.html",loged_user = loged_user)
        else:
            msg = "the username must be at least 4 charecters long and the password at least 6"
            return render_template("signup.html", msg = msg)
    return render_template("signup.html")

@app.route("/add_car", methods =["POST","GET"])
def about_us():
    if request.method == "POST":
        username = ic(request.form["username"])
        car_number = ic(request.form["car_number"])
        car_model = ic(request.form["car_model"])
        with open("my_users.json" , "r") as file:
            users = json.load(file)
        ic(users)
        for user in users:
            if username == user["username"]:
                user["cars"].append({"car_number": car_number, "car_model":car_model}) 
                with open("my_users.json" , "w") as file:
                    json.dump(users,file)
    return render_template("about.html")







if __name__ == "__main__":
    app.run(debug=True,port=5000)


