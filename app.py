
#***************************************************************
# Peer to Peer chat program:

#peer-to-peer chat communication between users using Rest API has been implemented.
#When a user sends message (URL end point /sendmessage), this is stored in msgbox (which is a dictionary where key is the receiver id and value is list of message items. 
#Each message item has sender ID and message info). 
#User Receives message (URL end point /receivemsg ) by pooling the msbox dictionary with its userid as key.


#***************************************************************


import requests
import json
from bottle import Bottle, run, static_file, request, response

app = Bottle()
msgbox = {}

@app.route('/')
@app.route('/index.html')
def index():
    return static_file('index.html',root='./') 


@app.route('/login', method='POST')
def do_login():
    creds = json.loads(request.body.read());
    print(creds['username']);
    print(creds['password']);
    if checkcreds(creds)==True:
       with open('users.json') as json_data:
          d = json.load(json_data)
          id = d[creds['username']]['id'];
          print("login successful");
          return str(id);
    else:
       response.status = 400
       print("login failed");
       return 'invalid creds'


@app.route('/news')
def getnews():
  url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=dba988d4aa5b4ba3b9b6b087651246ce')
  response = requests.get(url)
  return response.json()

@app.route('/users', method='GET')
def getuser():
   with open('users.json') as json_data:
      d = json.load(json_data)
      user = request.query['username'];
      if user in d:
          del d[user]
      print(d);
      return d;
  

@app.route('/sendmessage', method='POST')
def receivemessage():
   msgbody = json.loads(request.body.read());
   temp={msgbody['from']:msgbody['msg']}
   if msgbody['to'] in msgbox:
       msgbox[msgbody['to']].append(temp);
   else:
       msgbox[msgbody['to']]=[temp];
   print(msgbox);


@app.route('/receivemsg', method='GET')
def sendmessages():
   print(msgbox);
   userid = request.query['userid'];
   print(userid);
   if (userid == ""):
      print("empty userid");
      response.status=400;
      return "invalid userid"
   else:
      print("*******************");
      if int(userid) in msgbox:
          msglist = msgbox[int(userid)]
          del msgbox[int(userid)]  
          return {'data': msglist};
      else:
          response.status=400
          return "no messages"

#utils
def checkcreds(creds):
   print("called check creds");
   #creds = {'username': 'jan', 'password': '1234'}
   with open('users.json') as json_data:
      d = json.load(json_data)
      if creds['username'] in d :
         temp = {};
         temp = d[creds['username']];
         if temp['password'] == creds['password']:
            return True;
         else:
            return False;
      else:
         return False;



run(app,host='localhost', port=8080, debug=True)
