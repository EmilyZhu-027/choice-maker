from flask import Flask, render_template, request, redirect, url_for, flash, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 用于会话管理

# 存储房间数据
rooms = {}

@app.route('/')
def home():
    return render_template('index.html')

# 随机数生成
@app.route('/random_number', methods=['POST'])
def random_number():
    min_value = int(request.form['min_value'])
    max_value = int(request.form['max_value'])
    random_num = random.randint(min_value, max_value)
    return render_template('index.html', random_number=random_num)

# 随机选项生成
@app.route('/random_option', methods=['POST'])
def random_option():
    options = request.form.getlist('option')
    if options:
        random_choice = random.choice(options)
        return render_template('index.html', random_choice=random_choice)
    else:
        flash("Please provide at least one option", 'error')
        return render_template('index.html')

# 创建房间
@app.route('/createroom', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        room_name = request.form['room_name']
        password = request.form['password']
        
        # 确保密码是四位数
        if len(password) != 4 or not password.isdigit():
            flash('The password must be 4 digits!', 'error')
            return redirect(url_for('create_room'))

        # 如果房间已存在
        if room_name in rooms:
            flash('Room already exists!', 'error')
            return redirect(url_for('create_room'))

        # 创建房间并保存
        rooms[room_name] = {
            'password': password, 
            'votes': {'agree': 0, 'disagree': 0}
        }
        flash(f'Room "{room_name}" successfully created!', 'success')
        return redirect(url_for('enter_room', room_name=room_name))

    return render_template('createroom.html')

# 输入密码进入房间
@app.route('/enter_room/<room_name>', methods=['GET', 'POST'])
def enter_room(room_name):
    if room_name not in rooms:
        flash('Invalid room name!', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        password = request.form['password']
        if password == rooms[room_name]['password']:
            session['room'] = room_name  # 保存房间信息在会话中
            return redirect(url_for('vote', room_name=room_name))
        else:
            flash('Wrong password, please try again', 'error')

    return render_template('enter_room.html', room_name=room_name)

# 投票功能
@app.route('/vote/<room_name>', methods=['GET', 'POST'])
def vote(room_name):
    if 'room' not in session or session['room'] != room_name:
        flash('Please enter the room first', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        vote = request.form['vote']
        if vote in rooms[room_name]['votes']:
            rooms[room_name]['votes'][vote] += 1
        flash('Vote submitted successfully!', 'success')

    return render_template('vote.html', room_name=room_name, votes=rooms[room_name]['votes'])

if __name__ == '__main__':
    app.run(debug=True)
