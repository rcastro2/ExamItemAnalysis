import os,urllib, sqlite3
from flask import Flask,url_for,render_template,request, g, redirect

app = Flask(__name__)
app.secret_key = 'c\xbao\xa3a\xa1E\xc1:\x0f\x9cX\\K\xee\x1f\xab\xa8\xc9\x98\xddI)\x81'

@app.before_request
def before_request():
        g.db = sqlite3.connect('mockexam.db')
        g.db.row_factory = sqlite3.Row

@app.teardown_request
def teardown_request(exception):
        if getattr(g, 'db'):
                g.db.close()				
				
@app.route('/')
def index():
    return render_template('main.htm')

@app.route('/responsesEntered')
def responsesEntered():
        questions = [{"a":0,"b":0,"c":0,"d":0,"e":0} for i in range(40)]
        studentsindata = list(g.db.execute('select * from exam where answers not null'))
        studentsnotindata = list(g.db.execute('select * from exam where answers is null'))
        for student in studentsindata:
                responses = student["answers"].split(',')
                for index in range(len(responses)-1):
                        if responses[index] != '':
                                questions[index][responses[index]] += 1
        return render_template('responses.htm',studentsin = studentsindata,studentsnotin = studentsnotindata, results = questions)

@app.route('/enter',methods=['GET','POST'])
def enter():
        msg = "StudentID not found"
        if request.method == "POST":
                studentid = request.form['studentid']
                data = g.db.execute('select * from exam where studentid=?',(studentid,)).fetchone()
                if data != None:
                        response = ""
                        for i in range(1,41):
                                response = response + request.form['Q' + str(i)] + ","
                        g.db.execute('update exam set answers = ? where studentid = ?', (response,studentid))
                        g.db.commit()
                        msg = " Responses recorded"
                        print(studentid,response)
   
        return render_template('main.htm',message=msg,osis = studentid, answers = response.split(','))
        
if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)
