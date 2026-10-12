from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    student_id = request.form['student_id']
    email = request.form['email']
    year = request.form['year']
    
    return render_template('Successful.html', name=name, student_id=student_id, email=email, year=year)

if __name__ == '__main__':
    app.run(debug=True)