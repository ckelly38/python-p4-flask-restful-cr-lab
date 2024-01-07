#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        return make_response([pt.to_dict() for pt in Plant.query.all()], 200);

    def post(self):
        #get the data and create the new instance/object
        #then add this to the db
        #then return the response
        #print(request.form);
        #print(request.json);
        pt = None;
        if (len(request.form) < 1):
            pt = Plant(name=request.json.get("name"), image=request.json.get("image"),
                       price=float(request.json.get("price")));
        else:
            pt = Plant(name=request.form.get("name"), image=request.form.get("image"),
                       price=float(request.form.get("price")));
        #print(pt);
        #print(pt.to_dict());
        db.session.add(pt);
        db.session.commit();
        return make_response(pt.to_dict(), 201);
        #return make_response("NOT DONE YET 1-7-2024 1:20 AM", 406);

api.add_resource(Plants, "/plants");

class PlantByID(Resource):
    def get(self, id):
        plt = Plant.query.filter_by(id=id).first();

        if (plt == None): return make_response(f"Plant with id {id} not found!", 404);
        else: return make_response(plt.to_dict(), 200);

api.add_resource(PlantByID, "/plants/<int:id>");       

if __name__ == '__main__':
    app.run(port=5555, debug=True)
