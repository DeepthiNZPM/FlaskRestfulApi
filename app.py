from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse,fields,marshal_with,abort

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)
api=Api(app)

class Data_resource(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), unique=True, nullable=False)
    email=db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name={self.name},email={self.email})"

with app.app_context():
    db.create_all()

parser=reqparse.RequestParser()
parser.add_argument('name', type=str,required=True,help="name can't be blank")
parser.add_argument('email',type=str,required=True,help="email cant be blank")
user_fields= {
    'id':fields.Integer,
    'name': fields.String,
    'email':fields.String,
}
class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users=Data_resource.query.all()
        return users
    @marshal_with(user_fields)
    def post(self):
        args=parser.parse_args()
        user=Data_resource(name=args['name'],email=args['email'])
        db.session.add(user)
        db.session.commit()
        users=Data_resource.query.all()
        return users,201

class User(Resource):
    @marshal_with(user_fields)
    def get(self,id):
        user=Data_resource.query.filter_by(id=id).first()
        if not user:
            abort(404,"user not found")
        return user
    
    @marshal_with(user_fields)
    def patch(self,id):
        args=parser.parse_args()
        user=Data_resource.query.filter_by(id=id).first()
        if not user:
            abort(404,"user not found")
        user.name=args['name']
        user.email=args['email']
        db.session.commit()
        return user
    
    @marshal_with(user_fields)
    def delete(self,id):
        user=Data_resource.query.filter_by(id=id).first()
        if not user:
            abort(404,"user not found")
        db.session.delete(user)
        db.session.commit()
        users=Data_resource.query.all()
        return users,204

api.add_resource(Users,'/api')
api.add_resource(User,'/api/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask</h1>'
if __name__=='__main__':
    app.run(debug=True)