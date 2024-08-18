# 필요한 라이브러리 임포트
from flask import Flask, render_template, request, redirect, url_for, session
import os

# Flask 애플리케이션을 생성합니다.
app = Flask(__name__, static_folder='static', template_folder='templates')
# 세션 데이터를 암호화하고 복호화하는 키
app.secret_key = os.urandom(24)

# 리드 정보를 저장하는 전역 변수
lead_info = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lead_report', methods=['GET', 'POST'])
def lead_report():
    global lead_info  # 전역 변수로 선언

    if request.method == 'POST':
        lead_info = {
            'name': request.form['name'],
            'job': request.form['job'],
            'source': request.form['source'],
            'date': request.form['date'],
            'Party': request.form['Party'],
            'Unit': request.form['Unit'],
            'Territory': request.form['Territory'],
            'note': request.form['note']
        }
        return render_template('lead_report.html', lead_information=lead_info)
    else:
        return render_template('lead_report.html', lead_information=lead_info)

@app.route('/submit', methods=['POST'])
def submit():
    global lead_info

    if request.method == 'POST':
        lead_info = {
            'name': request.form['name'],
            'job': request.form['job'],
            'source': request.form['source'],
            'country': request.form['date'],
            'Party': request.form['Party'],
            'Unit': request.form['Unit'],
            'Territory': request.form['Territory'],
            'note': request.form['note']
        }
        return render_template('lead_report.html', lead_information=lead_info)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
