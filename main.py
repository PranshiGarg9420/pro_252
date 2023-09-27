# importing flask modules
from flask import Flask , request , render_template , jsonify

# importing firebase_admin module
import firebase_admin

# importing firestore.py module to create firestore client
from firebase_admin import firestore

# importing credentials.py module from firebase_admin folder
from firebase_admin import credentials

# creating authentication file
cred = credentials.Certificate("potentiometer-9e07c-firebase-adminsdk-p3dyz-cc8f975108.json")

# connect this python script/app with firebase using the authentication credentials
firebase_admin.initialize_app(cred)

# creating firestore client
db_client= firestore.client()

# creating flask object
app = Flask(__name__)

# first api : index page, only GET requests allowed at this API 
@app.route('/', methods=['GET'])
def index():
    try:
        
        # getting values from firebase document
        # convert it to python dictionary format
        pot= db_client.collection('Pro_252').document('potentiometer values').get.todict()


        # extracting value from dictionary
        val= pot['pot val']

        # rendering index.html template and pass the extracted value
        return render_template('index.html', value= val)
 
     except Exception as e:
        print(e)
        return jsonify({'status':'failed'})


# second api : adding data , only POST request allowed at this API
@app.route('/add', methods=['POST'])
def add():
    try:

        # getting potentiometer value from esp32
        pot_val= request.json.get('potentiometer values')

        # sending potentiometer value on firebase
        db_client.collection('Pro_252').document('potentiometer values').set({'pot val':pot_val})

        # return status is json format
        return jsonify({'status':'success'})

    except Exception as e:
        print(e)
        return jsonify({'status':'failed'})


# start the server
if __name__  ==  "__main__":
    app.run(host = '0.0.0.0' , debug = True)

