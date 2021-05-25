from flask import render_template,Flask,request
import requests
import string
import random
import re

from twilio.rest import Client
app = Flask(__name__)
#account_sid="AC2f7622e3ccb65c200792bb96e2a137a0"
#auth_token="21a824e80ecc7d0b9954394cfd620ad1"
#client=Client(account_sid,auth_token)
d = {"Andaman and Nicobar" : "AN", "Andhra Pradesh" : "AP","Arunachal Pradesh":"AR","Assam":"AS","Bihar":"BR","Chandigarh":"CH","Chhattisgarh":"CT","Daman and Diu":"DN","Delhi":"DL","Goa":"GA","Gujarat":"GJ","Himachal Pradesh":"HP","Haryana":"HR","Jharkhand":"JH","Jammu and Kashmir":"JK","Karnataka":"KA","Lakshadweep":"LD","Kerala":"KL","Maharashtra":"MH","Meghalaya":"ML","Madhya Pradesh":"MP","Manipur":"MN","Mizoram":"MZ","Nagaland":"NL","Odisha":"OR","Punjab":"PB","Puducherry":"PY","Rajasthan":"RJ","Sikkim":"SK","Telangana":"TG","Tamil Nadu":"TN","Tripura":"TR","Uttar Pradesh":"UP","Uttarakhand":"UT","West Bengal":"WB"}
states=["Andaman and Nicobar", "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Daman and Diu","Delhi","Goa","Gujarat","Himachal Pradesh","Haryana","Jharkhand","Jammu and Kashmir","Karnataka","Lakshadweep","Kerala","Maharashtra","Meghalaya","Madhya Pradesh","Manipur","Mizoram","Nagaland","Odisha","Punjab","Puducherry","Rajasthan","Sikkim","Telangana","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"]
    
@app.route('/')
def index():
    return render_template('index.html',states=states,error="",fname="",lname="",email="",aadhar="",contact="",people="",frm="",to="",date="")

@app.route('/login',methods=['POST','GET'])
def login():
    if(request.method=='POST'):
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        aadhar=request.form['aadhar']
        contact=request.form['contact']
        people=request.form['people']
        frm=request.form['from']
        to=request.form['to']
        date=request.form['date']
        name_pat=re.compile("^[A-Za-z.]+$")
        con_pat=re.compile("^[6-9][0-9]{9}$")
        email_pat=re.compile("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$")
        aadhar_pat=re.compile("^[0-9]{12}")
        people_pat=re.compile("^[0-9]+$")
        if(not name_pat.search(fname)):
            return render_template('index.html',states=states,error="first name",fname=fname,lname=lname,email=email,aadhar=aadhar,contact=contact,people=people,frm=frm,to=to,date=date)
        elif(not name_pat.search(lname)):
            return render_template('index.html',states=states,error="last name",fname=fname,lname=lname,email=email,aadhar=aadhar,contact=contact,people=people,frm=frm,to=to,date=date)
        elif(not email_pat.search(email)):
            return render_template('index.html',states=states,error="email",fname=fname,lname=lname,email=email,aadhar=aadhar,contact=contact,people=people,frm=frm,to=to,date=date)
        elif(not aadhar_pat.search(aadhar)):
            return render_template('index.html',states=states,error="aadhar number",fname=fname,lname=lname,email=email,aadhar=aadhar,contact=contact,people=people,frm=frm,to=to,date=date)
        elif(not con_pat.search(contact)):
            return render_template('index.html',states=states,error="contact",fname=fname,lname=lname,email=email,aadhar=aadhar,contact=contact,people=people,frm=frm,to=to,date=date)
        elif(not people_pat.search(people)):
            return render_template('index.html',states=states,error="number of people",fname=fname,lname=lname,email=email,aadhar=aadhar,contact=contact,people=people,frm=frm,to=to,date=date)
        else:
            r=requests.get('https://api.covid19india.org/v4/data.json')
            json_data=r.json()
            if(to=="Andaman and Nicobar"):to=to+" Islands"
            cnt = json_data[d[to]]["total"]["confirmed"] - json_data[d[to]]["total"]["recovered"]
            pop = json_data[d[to]]["meta"]["population"]
            limit = (cnt/pop)*100
            print(limit)
            key=""
            #url="https://api.chat-api.com/instance274184/sendMessage?token=q3es5la26k4qekdj"
            bdy=""

            if limit*100<30 and request.method=='POST':
                status = "CONFIRMED"
                key=str(''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits,k=10)))
                bdy='HELLO! '+fname+" "+lname+" your travel booking from "+frm+" to "+to+" is confirmed, your one time travel passcode is: "+key
                data={"body":"hello "+fname+" "+lname+" your travel status from "+frm+" to "+to+" is confirmed, your one time travel passcode is: "+key,"phone":"91"+str(contact)}
            else:
                status = "NOT CONFIRMED"
                bdy='HELLO! '+fname+" "+lname+" your travel booking from "+frm+" to "+to+" is NOT confirmed"
                data={"body":"hello "+fname+" "+lname+" your travel status from "+frm+" to "+to+" is NOT confirmed","phone":"91"+str(contact)}
            #To have whatsapp services a post request must be sent to chat-api provided if a valid subscription is there
            #r=requests.post(url,data)
            #k=client.messages.create(to="whatsapp:+918328180760",from_="whatsapp:+14155238886",body=bdy)
            #print(k.sid)
            return render_template('login.html',otp=key,fname=fname,lname=lname,email=email,aadhar=aadhar,contact=contact,people=people,frm=frm,to=to,date=date,status=status,key=key)
    else:
        print("INSIDE GET")


if __name__ == '__main__':
    app.run()
