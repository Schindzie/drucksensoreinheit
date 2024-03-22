from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import subprocess

app = Flask(__name__)
api = Api(app) 

speicherwerte = {"datenpunkt": 0.0}
running = {"up and running" : 1}
taraErfolg = False


class PostData(Resource):
    def post(self):
        print("\nposted: ")
        print(request.json)
        speicherwerte['datenpunkt'] = request.json['datenpunkt']
        return jsonify(speicherwerte)
        
class GetData(Resource):
    def get(self):
        print("\nrequested: ")
        print(speicherwerte)
        return jsonify(speicherwerte)

class Tara(Resource):
    def get(self):
        try:
            cmd = "tara.exe"
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=True)#, creationflags=0x08000000)
            taraErfolg = True
        except:
            taraErfolg = False

        return jsonify({"Tara erfolgreich":taraErfolg})

class Control(Resource):
    def get(self):
        return(jsonify(running))


api.add_resource(GetData, "/Data")
api.add_resource(PostData, "/Data/Update")
api.add_resource(Tara, "/Tara")
api.add_resource(Control, "/Control")


if __name__ == "__main__":
    app.run(port = 5000)
