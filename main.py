from flask import Flask, render_template, request, jsonify, session
from role_manager import RoleManager
from deepseek_api import DeepSeekAPI
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于会话安全

# 初始化角色管理器和API
role_manager = RoleManager()
api = DeepSeekAPI()


@app.before_request
def before_request():
    """确保每个会话有唯一的ID和角色状态"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['chat_history'] = []
        session['current_role'] = role_manager.get_current_role_name()

        # 添加初始问候
        current_role = role_manager.get_current_role()
        session['chat_history'].append({
            'sender': current_role['name'],
            'message': current_role['greeting'],
            'is_user': False
        })


@app.route('/')
def index():
    """主页面"""
    current_role = role_manager.get_role(session['current_role'])
    roles = role_manager.list_roles()
    return render_template(
        'index.html',
        roles=roles,
        current_role=session['current_role'],
        chat_history=session['chat_history'],
        role_name=current_role['name']
    )


@app.route('/send_message', methods=['POST'])
def send_message():
    """处理用户消息并获取AI回复"""
    data = request.json
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': '消息不能为空'}), 400

    # 添加到聊天历史
    session['chat_history'].append({
        'sender': '你',
        'message': user_message,
        'is_user': True
    })

    # 获取当前角色
    current_role = role_manager.get_role(session['current_role'])

    # 获取AI回复
    ai_response = api.generate_response(current_role, user_message)

    # 添加AI回复到聊天历史
    session['chat_history'].append({
        'sender': current_role['name'],
        'message': ai_response,
        'is_user': False
    })

    # 保存会话状态
    session.modified = True

    return jsonify({
        'response': ai_response,
        'sender': current_role['name']
    })


@app.route('/switch_role', methods=['POST'])
def switch_role():
    """切换角色"""
    data = request.json
    role_name = data.get('role_name', '')

    if not role_name:
        return jsonify({'error': '未指定角色'}), 400

    if role_manager.set_role(role_name):
        session['current_role'] = role_name
        current_role = role_manager.get_current_role()

        # 添加角色切换消息
        session['chat_history'].append({
            'sender': '系统',
            'message': f'已切换到角色: {role_name}',
            'is_user': False,
            'is_system': True
        })

        # 添加新角色的问候
        session['chat_history'].append({
            'sender': current_role['name'],
            'message': current_role['greeting'],
            'is_user': False
        })

        session.modified = True

        return jsonify({
            'success': True,
            'role_name': role_name,
            'greeting': current_role['greeting']
        })
    else:
        return jsonify({
            'success': False,
            'error': f'角色 {role_name} 不存在'
        }), 400


@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    """清空聊天历史"""
    current_role = role_manager.get_role(session['current_role'])

    # 重置聊天历史，只保留问候
    session['chat_history'] = [{
        'sender': current_role['name'],
        'message': current_role['greeting'],
        'is_user': False
    }]

    session.modified = True

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, port=5000)