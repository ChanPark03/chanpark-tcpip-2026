# ex14_flask_jinja 폴더 
     # main.py
     # static/
         #css/style.css
         # js/script.js
         # images/logo.jpg
     # templates/
         # base.html
         # index.html
         
from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def index():
    user_info = {"usernane": "iot반", "level": "bootcamp"} # 파이썬: 딕셔너리, 데이터/웹: JSON
    # 파이썬: 리스트, c/java: 배열, 데이터/웹: JSON
    items = ["Flask 배우기", "Jinja 이해", "예쁜 웹앱 만들기"]
    return render_template('index.html', user = user_info, tasks = items)

if __name__ == "__main__":
    app.run(host="163.152.213.114", port = 5000)