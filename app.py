from flask import Flask, render_template, request, session, redirect, url_for, flash
app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD" # 사용자 지정 비밀번호인데, session과 flash를 사용하기 위해서는 반드시 필요합니다.

from pymongo import MongoClient
client = MongoClient('')
db = client.dbsparta # 자신의 몽고DB의 주소 등을 기입해 주세요.

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/sign_up', methods=['POST']) # 절차생략을 위해 Sign up과 동시에 회원가입 되도록 자동화 시켜 뒀습니다.
def sign_up():
   user_data = list(db.all_user_data.find({}, {'_id': False}))
   doc = {'idIndex': len(user_data) + 1, 'userID': 'test' + str(len(user_data) + 1), 'pwd': '1234', 'loginFlag': False}
   db.all_user_data.insert_one(doc)
   flash('userID: test'+ str(len(user_data) + 1) +', password: 1234 으로 가입완료!')
   return redirect(url_for('home'))

@app.route('/login', methods=['POST', 'GET']) # 일단은 POST와 GET 요청을 모두 받을 수 있도록 만들어 둡니다.
def login():
   if request.method == 'POST':
      id_receive = request.form['id']
      password_receive = request.form['password']
      if id_receive == '' or password_receive == '':
         flash('아이디와 비밀번호를 입력해 주세요.') # flash는 flask에서 html로 팝업 메시지를 전송하는 역할을 합니다. html에서 코드를 임포트해야합니다.(index.html 참조)
         return redirect(url_for('home'))
      else:
         user_data = db.all_user_data.find_one({'userID': id_receive}) # 이용자의 비밀번호가 DB의 정보와 일치하는지 체크합니다.
         if user_data['pwd'] == password_receive:
            session['idIndex'] = user_data['idIndex']
            session['logFlag'] = True
            session['userID'] = id_receive
            flash('일치!')
         else:
            flash('불일치!')
         return redirect(url_for('home'))
   else:
      flash('잘못된 접근입니다.') # POST 요청으로 접근하지 않고 GET 요청으로 접근했을 시 접근 거부를 하기 위한 코드입니다.
      return redirect(url_for('home'))

@app.route('/logout', methods=['POST', 'GET'])
def logout():
   if request.method == 'POST':
      session.clear()
      flash('로그아웃 되었습니다.')
      return redirect(url_for('home'))
   else:
      flash('비정상적인 접근입니다.')
      return redirect(url_for('home'))

@app.route('/member', methods=['GET']) # 세션값으로 주었던 logFlag==True를 비교해 회원가입을 진행하신 분들만 정상적인 팝업창이 출력되도록 합니다.
def member():
   if session.get('logFlag') != True:
      flash('회원만 접근가능합니다.')
      return redirect(url_for('home'))
   else:
      flash('코딩클럽에 오신 것을 환영합니다!')
      return redirect(url_for('home'))

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)