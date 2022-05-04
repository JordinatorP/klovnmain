import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import random
import string
import os
import traceback
import requests



#Start
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'whitelist.db')
app.config['SQLALCHEMY_BINDS'] = {'key': 'sqlite:///' + os.path.join(basedir, 'key.db'),}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init DataBases
db = SQLAlchemy(app)


#Init ma
ma = Marshmallow(app)


#DataBase Key
class key(db.Model):
  __bind_key__ = 'key'
  wlkey = db.Column(db.String(10000), primary_key=True)
  useridkey = db.Column(db.String(10000))
  placeidkey = db.Column(db.String(10000))
  discordid = db.Column(db.String(10000))

  def __init__(self, wlkey, useridkey, placeidkey, discordid):
    self.wlkey = wlkey
    self.useridkey = useridkey
    self.placeidkey = placeidkey
    self.discordid = discordid

#KeySchema
class keyschema(ma.Schema):
  class Meta:
    fields = ('wlkey', 'useridkey', 'placeidkey', 'discordid')

#Init Key schema
key_schema = keyschema(strict=True)
keys_schema = keyschema(many=True, strict=True)


@app.route('/addkey', methods=['POST'])
def addkey():
  wlkey = request.json['wlkey']
  useridkey = request.json['useridkey']
  placeidkey = request.json['placeidkey']
  discordid = request.json['discordid']
  accescode = request.json['accescode']
  if accescode=='5lgSyQm7KuKDtwM':
    new_key = key(wlkey, useridkey, placeidkey, discordid)

    db.session.add(new_key)
    db.session.commit()

    return key_schema.jsonify(new_key)
  else:
    return 'Request could not be verified, security check failed'

@app.route('/getkeysindb', methods=['GET'])
def getkeys():
  all_keys = key.query.all()
  results = keys_schema.dump(all_keys)
  
  return jsonify({'Keys': results.data})

@app.route('/getkeysindb/<wlkey>', methods=['DELETE'])
def delete_product(wlkey):
  whitelistkey = key.query.get(wlkey)
  db.session.delete(whitelistkey)
  db.session.commit()

  return key_schema.jsonify(whitelistkey)


      

#DataBase whitelist
class whitelist(db.Model):
    placeid = db.Column(db.String(10000), primary_key=True)
    userid = db.Column(db.String(10000))
    tijd = db.Column(db.String(10000))
  

    def __init__(self, placeid, userid, tijd):
        self.placeid = placeid
        self.userid = userid
        self.tijd = tijd
        

#WhitelistSchema
class whitelistschema(ma.Schema):
    class Meta:
        fields = ('placeid', 'userid', 'tijd')


#Init Schema
whitelist_schema = whitelistschema(strict=True)
whitelists_schema = whitelistschema(many=True, strict=True)


#Delete wl
@app.route('/getwhitelistdelete/<placeid>', methods=['DELETE'])
def delete_whitelist(placeid):
  code = request.json["password"]
  whitelist_delete = whitelist.query.get(placeid)
  db.session.delete(whitelist_delete)
  db.session.commit()
  if code=="yFMrSBBEGArHmtilxOYx": 
    return whitelist_schema.jsonify(whitelist_delete)
  else:
    return "Request could not be verified, security check failed"

#Voeg nieuwe whitelist toe
@app.route('/addwhitelist', methods=['POST'])
def addwhitelist():
    placeid = request.json['placeid']
    userid = request.json['userid']
    code = request.json['password']
    tijd = request.json['tijd']
    if code=="8XPrTeH06vCfob92pXVcSl16tBV50d":
    
        nieuw_whitelist = whitelist(placeid, userid, tijd)

        db.session.add(nieuw_whitelist)
        db.session.commit()

        return whitelist_schema.jsonify(nieuw_whitelist)
    else:
        return 'Request could not be verified, security check failed'

@app.route('/updatewhitelist/<placeid>', methods=['PUT'])
def update_placeid(placeid):
  placeidupdate = whitelist.query.get(placeid)

  placeidd = request.json['placeid']
  userid = request.json['userid']
  code = request.json['password']
  if code=="G@7vDa!JwPI1wVS3LO8Nuy*E49$R00":

      placeidupdate.placeid = placeidd
      placeidupdate.userid = userid
 
      db.session.commit()

      return whitelist_schema.jsonify(placeidupdate)
  else:
      return 'Request could not be verified, security check failed'


#Pak alle whitelists
@app.route('/getwhitelists', methods=['GET'])
def getallwitelists():
  alle_whitelists = whitelist.query.all()
  results = whitelists_schema.dump(alle_whitelists)
  return jsonify({'PlaceIDS': results.data})


@app.route('/getwhitelists/<placeid>', methods=['GET'])
def getsinglewhitelist(placeid):
  lisence = whitelist.query.get(placeid)
  return whitelist_schema.jsonify(lisence)


@app.route('/getinternaldata', methods=['GET'])
def getinternaldata():
  
  return jsonify({'InterneData': [{'9048793860': '????L$}$L~?>#}&'}, {'2990452798': '????#}#<L?##$?#%$&'}, {'4562734855': '????L$}$L~?>#}&'}, {'3592590228': '???%~L}>L>$%<}&'}, {'8146175991': '~%?#&%&~$&?&'}, {'1509048004': '????}L}~<?~~L?~$&'}, {'8314568654': '???$#>&~$><<$<%$&'}, {'9160941823': '???%%<$&&~%&$#L#<'}]})


@app.route('/getkeysindbupdate/<wlkey>', methods=['PUT'])
def update_connect(wlkey):
  connectionupdate = key.query.get(wlkey)

  wlkey = request.json['wlkey']
  useridkey = request.json['useridkey']
  placeidkey = request.json['placeidkey']
  discordid = request.json['discordid']

  connectionupdate.wlkey = wlkey
  connectionupdate.useridkey = useridkey
  connectionupdate.placeidkey = placeidkey
  connectionupdate.discordid = discordid

  db.session.commit()

  return key_schema.jsonify(connectionupdate)

@app.route('/getkey', methods=['GET'])
def getkey():
  
  url = 'http://168.119.82.94:80/getkeysindb'

  jsondata = requests.get(url).json()

  length = 36
  letters = string.ascii_letters
  result_str = "".join(random.choice(letters) for i in range(length))

  samebool = False
  for wlkey in jsondata['Keys']:
    
    if result_str == wlkey['wlkey']:
      samebool = True       
    
  
  if samebool == True:
    return jsonify({'Key': 'Error'})
  elif samebool == False:
    return jsonify({'Key': result_str})
    
        

    
    

  
 
      
      
      
      






@app.route('/helloworld', methods=['GET'])
def lolboy():
  return jsonify({'Colors': [{'Rood': 'Red'}, {'Groen': 'Green'}, {'Blauw': 'Blue'}]})


  



#Server aan zetten
if __name__ == '__main__':
  app.run(host='0.0.0.0')
