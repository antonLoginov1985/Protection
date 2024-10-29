from flask import render_template, request, redirect, url_for, flash, jsonify, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
from app import app, db
from model import User, Training, Employees, Department, Positions, Place, Program, Bloсktraining, Typetraining, Typedocument, questions
import report
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)


UPLOAD_FOLDER = 'uploads'
folder_name = "static"
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.template_filter('formatdatetime')
def format_datetime(value, format='%d %B %Y'):

    if value is None:
        return ""
    return value.strftime(format)


@app.template_filter('formatresult')
def format_result(value):

    if value is None:
        return 'Не сдано'
    elif value == 'False':
        return 'Не сдано'
    else:
        return 'Cдано'


@app.route('/', methods=['GET'])
def hello_user():
    return render_template('index.html')



@app.route('/test')
def test():
    session['result'] = ""
    subList = questions.query.with_entities(questions.subject).distinct()
    return render_template('test.html',  subList=subList)


@app.route('/arm', methods=['GET', 'POST'])
def arm():

    departments = db.session.query(Department).all()
    return render_template('arm.html', departments=departments)


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    return render_template('admin.html')


@app.route('/import_from_1c', methods=['GET', 'POST'])
def import_from_1c():

    return render_template('import_from_1c.html')


@app.route('/information', methods=['GET', 'POST'])
def information():
    return render_template('information.html')


# @app.route("/training/", defaults={'page': 1}, methods=["GET", "POST"])
@app.route('/training', methods=["GET", "POST"])
def training():

    training = Training.query.order_by(
        Training.timestamp)

    return render_template('training.html', training=training)


@app.route('/add_training/new/', methods=['GET', 'POST'])
def add_training():

    if request.method == 'POST':

        place = request.form['place']
        employee_select = request.form.get('employee')
        block_training = request.form.get('block_training')
        program = request.form.get('program')
        typetraining = request.form.get('typetraining')
        typedocument = request.form.get('typedocument')
        result = request.form.get('result')
        next_date = request.form['next_date']
        date_document = request.form['date_document']
        number_document = request.form['number_document']
        file_path = request.form['file_path']

        newTraining = Training(employees_id=employee_select,
                               training_date=date_document,
                               block_training_id=block_training,
                               program_id=program,
                               type_training_id=typetraining,
                               place_id=place,
                               type_document_id=typedocument,
                               date_document=date_document,
                               number_document=number_document,
                               result=result,
                               next_date=next_date,
                               file_path=file_path)

        db.session.add(newTraining)
        db.session.commit()
        return redirect(url_for('training'))
    else:
        places = Place.query.order_by(Place.name)
        programs = Program.query.order_by(Program.name)
        blockTrainings = Bloсktraining.query.order_by(Bloсktraining.name)
        typetrainings = Typetraining.query.order_by(Typetraining.name)
        typedocuments = Typedocument.query.order_by(Typedocument.name)
        return render_template('add_training.html',  places=places, programs=programs, blockTrainings=blockTrainings, typedocuments=typedocuments, typetrainings=typetrainings)


@app.route("/training/<int:training_id>/edit/", methods=['GET', 'POST'])
def edit_training(training_id):
    # editedMarket = db.sesssion.query(Market).filter_by(id=markets_id).one
    editedTraining = Training.query.filter_by(id=training_id).one()
    typedocuments = Typedocument.query.order_by(Typedocument.name)
    if request.method == 'POST':
        if request.form['next_date']:
            editedTraining.next_date = request.form['next_date']
            db.session.commit()
            return redirect(url_for('training'))
    else:

        print(editedTraining.next_date)
        return render_template('edit_training.html', training=editedTraining, typedocuments=typedocuments)


@app.route('/training/<int:training_id>/delete/', methods=['GET', 'POST'])
def delete_training(training_id):
    # marketToDelete = db.sesssion.query(Market).filter_by(id=markets_id).one()
    trainingToDelete = Training.query.filter_by(id=training_id).one()
    if request.method == 'POST':
        db.session.delete(trainingToDelete)
        db.session.commit()
        return redirect(url_for('training', training_id=training_id))
    else:
        return render_template('delete_training.html', training=trainingToDelete)


@app.route('/place', methods=["GET"])
def place():

    if request.method == 'GET':
        places_training = Place.query.filter(Place.is_training == True)
        places_certification = Place.query.filter(Place.is_certification == True)

        return render_template('place.html', places_training=places_training, places_certification=places_certification)


@app.route('/place/new/', methods=['GET', 'POST'])
def add_place():

    if request.method == 'POST' :
       if len(request.form['name']) > 0:
            newPlace = Place(
               name=request.form['name'], address=request.form['address'], is_training=True, is_certification=False)

            db.session.add(newPlace)
            db.session.commit()
            return redirect(url_for('place'))
       else:
            # response = make_response()
            # response.status_code = 400
            # response.data = jsonify({"error": "Place name is required"})
            return jsonify({"error": "Place name is required"}), 400
    else:
     return render_template('add_place.html')


@app.route("/place/<int:place_id>/edit/", methods=['GET', 'POST'])
def edit_place(place_id):
    # editedMarket = db.sesssion.query(Market).filter_by(id=markets_id).one
    edit_place = Place.query.filter_by(id=place_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edit_place.name = request.form['name']
            edit_place.address = request.form['address']
            db.session.commit()
            return redirect(url_for('place'))
    else:

        return render_template('edit_place.html', place=edit_place)


@app.route('/place/<int:place_id>/delete/', methods=['GET', 'POST'])
def delete_place(place_id):
    # marketToDelete = db.sesssion.query(Market).filter_by(id=markets_id).one()
    placeToDelete = Place.query.filter_by(id=place_id).one()
    if request.method == 'POST':
        db.session.delete(placeToDelete)
        db.session.commit()
        return redirect(url_for('place'))
    else:
        return render_template('delete_place.html', place=placeToDelete)


@app.route('/program/', methods=["GET", "POST"])
def program():

    programs = db.session.query(Program, Bloсktraining).join(
        Bloсktraining, Program.bloсk_id == Bloсktraining.id).all()

    if request.method == 'POST':
        return render_template('program.html', programs=programs)
    else:
        return render_template('program.html', programs=programs)


@app.route('/program/new/', methods=['GET', 'POST'])
def add_program():

    if request.method == 'POST':
        bloсk_id = request.form['block_training']
        newProgram = Program(

            name=request.form['name'], bloсk_id=bloсk_id)
        print(bloсk_id)
        db.session.add(newProgram)
        db.session.commit()
        return redirect(url_for('program'))
    else:
        blockTrainings = Bloсktraining.query.order_by(Bloсktraining.name)

        return render_template('add_program.html', blockTrainings=blockTrainings)


@app.route("/program/<int:program_id>/edit/", methods=['GET', 'POST'])
def edit_program(program_id):

    edit_program = Program.query.filter_by(id=program_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edit_program.name = request.form['name']
            db.session.commit()
            return redirect(url_for('program'))
    else:
        return render_template('edit_program.html', program=edit_program)


@app.route('/program/<int:program_id>/delete/', methods=['GET', 'POST'])
def delete_program(program_id):

    programToDelete = Program.query.filter_by(id=program_id).one()
    if request.method == 'POST':
        db.session.delete(programToDelete)
        db.session.commit()
        return redirect(url_for('program'))
    else:
        return render_template('delete_program.html', program=programToDelete)


@app.route('/view_report', methods=['GET', 'POST'])
def view_report():

    places = Place.query.order_by(Place.name)
    blockTrainings = Bloсktraining.query.order_by(Bloсktraining.name)

    if request.method == 'POST':
        place_id = request.form['place']
        block_id = request.form.get('block_training')
        reports = report.report_training(block_id, place_id)
        block = Bloсktraining.query.filter_by(id=block_id).first()
        return render_template('view_report.html', reports=reports, places=places, blockTrainings=blockTrainings, place_id=place_id, block_id=block_id, block=block)
    return render_template('view_report.html', places=places, blockTrainings=blockTrainings)


@app.route('/view_employees', methods=['GET', 'POST'])
def view_employees():

    # if request.method == 'GET':
        employees = report.report_employees()      
        return render_template('view_employees.html', employees=employees)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('psw')

    if login and password:
        user = User.query.filter_by(login=login).first()
        # user = db.sesssion.query(User).filter_by(login=login).first()
        if user and check_password_hash(user.psw, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page or url_for('hello_user'))
            # return redirect(url_for('showMarkets'))
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    email = request.form.get('email')
    password = request.form.get('psw')
    password2 = request.form.get('psw2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, email=email, psw=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_user'))


@app.after_request
def redirect_to_signin(response):

    if response.status_code == 401:
        print('login_page')
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response

@app.route('/employees', methods=['GET'])
def get_employees():

    employees = [{'last_name': row.last_name,
                  'id': row.id,
                  'first_name': row.first_name,
                  'middle_name': row.middle_name,
                  'snils': row.snils,
                  'position': row.position_id}
                 for row in Employees.query.all()]
    return jsonify(employees)

# Маршрут для получение информации о конкретном сотруднике


@app.route('/employees/<snils>', methods=['GET'])
def get_employee(snils):

    # employee = Employees.query.filter(Employees.snils == snils).one()
    res = db.session.query(Employees, Positions).join(
        Positions, Employees.position_id == Positions.id).filter(Employees.id == snils).one()
    # c.execute('SELECT snils, position FROM employees WHERE snils = ?', (snils,))
    #   employee = c.fetchone()
    if res:
        return jsonify({'snils': res.Employees.snils,
                        'id': res.Employees.id,
                        'last_name': res.Employees.last_name,
                        'first_name': res.Employees.first_name,
                        'position': res.Positions.name})
    else:
        return jsonify({'error': 'Employee not found'}), 404


@app.route('/programs/<block_id>', methods=['GET'])
def get_program(block_id):

    print(block_id)
    res = db.session.query(Program, Bloсktraining).join(
        Bloсktraining, Program.bloсk_id == Bloсktraining.id).filter(Bloсktraining.id == block_id).all()

    programs = [{'name': row.Program.name,
                 'id': row.Program.id
                 }
                for row in res]
    return jsonify(programs)


# Тестирование

def setStatus(qlist):
    qAttempt = []
    strval = session['result'].strip()
    print(strval)
    ans = strval.split(',')
    print(ans)
    for i in range(int(len(ans)/2)):
        qAttempt.append(int(ans[2*i]))
    print(qlist)
    for rw in qlist:
        if rw.qid in qAttempt:
            rw.bcol = 'green'   # set color
            rw.status = 'disabled'  # disable


@app.route('/quiz', methods=["POST"])
def quiz():
    subject = request.form.get('sub')
    questList = questions.query.filter_by(subject=subject).all()
    quest = questions.query.filter_by(subject=subject).first()

    return render_template("dashboard.html", questList=questList, quest=quest)


@app.route("/showQuest/<string:subject>,<int:qid>", methods=["POST"])
def showQuest(subject, qid):
    questList = questions.query.filter_by(subject=subject).all()
    next_qid = qid + 1
    quest = questions.query.filter_by(qid=next_qid).first()
    last_quest = questions.query.filter_by(is_last =True).first()
    ans = request.form.get('answer')
    # print(ans)
    if len(ans) > 0:
        res = session['result']
        res = res+str(qid)+','+ans+','
        session['result'] = res
    setStatus(questList)
    if last_quest.qid == qid:
        return redirect(url_for('logout_test'))
    else:
       return render_template("dashboard.html", questList=questList, quest=quest)


@app.route("/logout_test")
def logout_test():
    # calculate result
    count = 0
    txt = ""
    strval = session['result'].strip()
    print(strval) 
    # split result string by ','
    ans = strval.split(',')
    for i in range(int(len(ans)/2)):
        qd = ans[2*i]  # get question id
        qn = ans[2*i+1]  # get the sorresponding answer
        tt = int(qd)
        quest = questions.query.filter_by(qid=tt).first()
        actans = quest.answer
        # compare correct answer in questions table with answer chosen by user
        if actans == int(qn):
            count = count+1  # increment counter
    txt = txt+'У вас ' + str(count) + ' правильных ответов из ' + str(
        int(len(ans)/2)) + ' вопросов '  # set the result statement
    return render_template("result.html", txt=txt)


def create_app():

    return app

if __name__ == '__main__':
    # app.debug = True
    app.run(port=4996)
