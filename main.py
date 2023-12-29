from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)
CORS(app)


def load_users():
  with open('db.json', 'r') as file:
    users_data = json.load(file)
  return users_data['users']


users = load_users()


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  email = data.get('email')
  password = generate_password_hash(data.get('password'),
                                    method='pbkdf2:sha256',
                                    salt_length=8)

  if any(user['email'] == email for user in users):
    return jsonify(message='User already exists'), 400

  new_user = {
      'email': email,
      'password_hash': password,
      'access_level': 'user'
  }
  users.append(new_user)

  with open('db.json', 'w') as file:
    json.dump({'users': users}, file)

  return jsonify(message='Registration successful'), 201


@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  user = next((user for user in users if user['email'] == email), None)

  if user and check_password_hash(user['password_hash'], password):
    access_token = create_access_token(identity={
        'email': email,
        'access_level': user['access_level']
    })

    if user['access_level'] == 'admin':
      user_list = [{
          'email': user['email'],
          'access_level': user['access_level']
      } for user in users]
      return jsonify(access_token=access_token, users=user_list), 200

    return jsonify(access_token=access_token), 200
  else:
    return jsonify(message='Invalid email or password'), 401


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
  current_user = get_jwt_identity()

  if current_user['access_level'] == 'admin':

    users_data = load_users()
    return jsonify(users=users_data['users'])

  return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
