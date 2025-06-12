from flask import Flask, request, jsonify
from main import role_manager, DeepSeekAPI

app = Flask(__name__)
api = DeepSeekAPI()


@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    user_input = data.get('message')
    role_name = data.get('role', 'catgirl')

    role_manager.set_role(role_name)
    current_role = role_manager.get_current_role()
    response = api.generate_response(current_role, user_input)

    return jsonify({
        'role': current_role['name'],
        'response': response
    })


@app.route('/api/roles', methods=['GET'])
def roles_api():
    return jsonify(role_manager.list_roles())


@app.route('/')
def index():
    return app.send_static_file('index.html')