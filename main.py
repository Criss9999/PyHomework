# Scrieti un program python care permite monitorizarea orelor lucrate de angajatii unei companii. 
# Datele pe care le primiti ca parametru provin de la punctele de access dintr-o cladire de birouri. 
# Orice persoana, pentru a intra in cladire, sau pentru a iesi, trebuie sa valideze cardul de acces. 
# Prin validare, se obtine id-ul persoanei care detine cartela, ora validarii precum si sensul (intrare sau iesire). 

from FileAccessGate import *
from Database import Database
from Chiulangii import Chiulangii
from flask import Flask,request,jsonify
import time



app = Flask(__name__)
    

# Cerinta c)

@app.route('/user',methods = ['POST'])
def addDataBase():
    sql = request.get_json()
    user_id = sql.get('user_id')
    first_name = sql.get('first_name')
    last_name = sql.get ('last_name')
    company = sql.get ('company')
    manager_id = sql.get ('manager_id')
    user = Database()
    user.insert_user(user_id, first_name, last_name, company, manager_id)
    return jsonify (sql)

#E.g.
# {
#     "user_id":65,
#     "first_name":"Manole",
#     "last_name":"Hagi",
#     "company":"FEV",
#     "manager_id":12
# }


# Cerinta e)

@app.route('/accesTable',methods = ['POST'])
def jsonFormat():
    sql = request.get_json()
    user_id = sql.get('user_id')
    date = sql.get('date')
    gate_id = sql.get ('gate_id')
    direction = sql.get ('direction')
    user = Database()
    user.insert_access_record(user_id, date, gate_id, direction)
    return jsonify (sql)

# {
#     "user_id":65,
#     "date":"2024-03-17T17:40:28",
#     "gate_id":"2",
#     "direction":"out"
   
# }

# Cerinta f)

@app.route('/problemo',methods = ['POST'])
def inTroubleEmployees():
    info = Chiulangii()
    print (info.createChiulangii())
    time.sleep(5)
    return "Done!"



if __name__ == '__main__':
    app.run(host = "0.0.0.0",port = 4000, debug = True)







