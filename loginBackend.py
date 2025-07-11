from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os
import random
from score_predictor import predict_score


app = Flask(__name__, template_folder='LoginbackendFolder')

csv_path = os.path.join(os.path.dirname(__file__), 'loginUsers.csv')
questions_path = os.path.join(os.path.dirname(__file__), 'Apquestions.csv')
com_questions_path = os.path.join(os.path.dirname(__file__), 'CommunicationAssess.csv')
tech_questions_path = os.path.join(os.path.dirname(__file__), 'TechnicalQuestions.csv')

apt_questions = []
com_questions = []
tech_questions = []

@app.route('/', methods=['GET', 'POST'])
def login_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        action = request.form['action']
        email = request.form.get('email', '')

        if action == 'signup':
            if os.path.exists(csv_path):
                with open(csv_path, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row[0] == username:
                            return "User already exists. Please login."
            with open(csv_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([username, email, password])
            return redirect(url_for('Apassessment'))

        elif action == 'login':
            if os.path.exists(csv_path):
                with open(csv_path, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row[0] == username and row[2] == password:
                            return redirect(url_for('Apassessment'))
            return "Invalid credentials. Please try again."

    return render_template('navLogin.html')


@app.route('/home')
def home():
    return render_template('proHome.html')

@app.route('/navContact')
def navContact():
    return render_template('navcontact.html')


@app.route('/navFeatures')
def navFeatures():
    return render_template('navFeatures.html')

@app.route('/navAbout')
def navAbout():
    return render_template('navigateAbout.html')

@app.route('/dashboard')
def dashboard():
    return render_template('proHome.html')


@app.route('/Apassessment')
def Apassessment():
    return render_template('Aptitude.html')


@app.route('/Comassessment')
def Comassessment():
    aptitude_score = request.args.get('aptitude', '')
    print("Aptitude score in received com section",aptitude_score)
    if not aptitude_score:
        return redirect(url_for('Apassessment'))
    return render_template('Communication.html', aptitude=aptitude_score)


@app.route('/Techassessment')
def Techassessment():
    aptitude_score = request.args.get('aptitude', '')
    communication_score = request.args.get('communication', '')
    if not aptitude_score or not communication_score:
        return redirect(url_for('Comassessment', aptitude=aptitude_score or 0))
    return render_template('Technical.html', aptitude=aptitude_score, communication=communication_score)


@app.route('/form')
def form_page():
    aptitude_score = request.args.get('aptitude_score')
    communication_score = request.args.get('communication_score')
    technical_score = request.args.get('technical_score')
    return render_template('formPage.html', 
                           aptitude_score=aptitude_score,
                           communication_score=communication_score,
                           technical_score=technical_score)


@app.route('/get-questions')
def get_questions():
    questions= []
    if os.path.exists(questions_path):
        with open(questions_path, 'r') as f:
            reader = list(csv.DictReader(f, delimiter=';'))
            questions = random.sample(reader, min(10, len(reader)))
        for q in questions:
            apt_questions.append(q['index'])
        print(apt_questions)
    return jsonify(questions)


@app.route('/get-com-questions')
def get_com_questions():
    questions = []
    if os.path.exists(com_questions_path):
        with open(com_questions_path, 'r') as f:
            reader = list(csv.DictReader(f))
            questions = random.sample(reader, min(10, len(reader)))
        for q in questions:
            com_questions.append(q['index'])
        print(com_questions)
    return jsonify(questions)


@app.route('/get-tech-questions')
def get_tech_questions():
    questions = []
    if os.path.exists(tech_questions_path):
        with open(tech_questions_path, 'r') as f:
            reader = list(csv.DictReader(f))
            for row in reader:
                if all(row.get(k) for k in ['index','Question', 'Option A', 'Option B', 'Option C', 'Option D', 'Answer']):
                    questions.append(row)
            questions = random.sample(questions, min(20, len(questions)))
            for q in questions:
                tech_questions.append(q['index'])
            print(tech_questions)
    return jsonify(questions)


@app.route('/submit-aptitude-answers', methods=['POST'])
def submit_aptitude_answers():
    user_answers = request.json['userAnswers']
    correct_count = 0

    if os.path.exists(questions_path):
        with open(questions_path, 'r') as f:
            reader = list(csv.DictReader(f, delimiter=';'))
            total = min(len(reader), len(user_answers))
            print(apt_questions)
            for i in range(total):
                correct = reader[int(apt_questions[i])-1]['Answer'].strip().upper()
                given = (user_answers[i] or "").strip().upper()
                if correct == given:
                    correct_count += 1
            percentage = round((correct_count / total) * 100, 2) if total > 0 else 0
    else:
        percentage = 0

    return jsonify({"redirect": url_for('Comassessment', aptitude=percentage)})


@app.route('/submit-com-answers', methods=['POST'])
def submit_com_answers():
    user_answers = request.json['userAnswers']
    aptitude = request.args.get('aptitude', '0')
    correct_count = 0

    if os.path.exists(com_questions_path):
        with open(com_questions_path, 'r') as f:
            reader = list(csv.DictReader(f))
            total = min(len(reader), len(user_answers))
            for i in range(total):
                correct = reader[int(com_questions[i])-1]['Answer'].strip().upper()
                given = (user_answers[i] or "").strip().upper()
                if correct == given:
                    correct_count += 1
            percentage = round((correct_count / total) * 100, 2) if total > 0 else 0
    else:
        percentage = 0

    return jsonify({"redirect": url_for('Techassessment', aptitude=aptitude, communication=percentage)})


@app.route('/submit-tech-answers', methods=['POST'])
def submit_tech_answers():
    user_answers = request.json['userAnswers']
    aptitude_score = request.args.get('aptitude', '0')
    communication_score = request.args.get('communication', '0')
    correct_count = 0

    if os.path.exists(tech_questions_path):
        with open(tech_questions_path, 'r') as f:
            reader = list(csv.DictReader(f))
            total = min(len(reader), len(user_answers))
            for i in range(total):

                correct = reader[int(tech_questions[i])-1]['Answer'].strip().upper()
                given = (user_answers[i] or "").strip().upper()
                print(correct , given)
                if correct == given:
                    correct_count += 1
            technical_score = round((correct_count / total) * 100, 2) if total > 0 else 0
    else:
        technical_score = 0

    return jsonify({
        "redirect": url_for('form_page',
                            aptitude_score=aptitude_score,
                            communication_score=communication_score,
                            technical_score=technical_score)
    })


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Extract form data
        # cgpa,backlogs,certifications,aptitude,coding,communication,projects,hackathon,resume,branch,placement_readiness,company_fit
        data = {
            "cgpa": float(request.form['cgpa']),
            "backlogs": int(request.form['backlogs']),
            "certifications": int(request.form['certifications']),
            "aptitude": float(request.form['aptitude_score']),
            "coding": float(request.form['technical_score']),
            "communication": float(request.form['communication_score']),
            "projects": int(request.form['projects']),
            "resume": float(request.form['resume_score']),
            "hackathon":  1 if request.form['hackathons'] == 'Yes' else 0,
            "branch": int(request.form['branch'])
        }

        # Save to CSV
        with open('final_data.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

        # Make prediction
        result = predict_score(data)
        placement_readiness = result["placement_readiness"]
        if placement_readiness == 1:
            placement_readiness = "Ready"
        else:
            placement_readiness = "Not Ready"

        company_fit = result["company_fit"]
        suggestion = get_suggestion(company_fit,placement_readiness)

        return render_template('result.html', placement_readiness=placement_readiness, company_fit=company_fit,suggestion=suggestion)
def get_suggestion(company_fit, placement_readiness):
    
    if company_fit == "Tier 1" and placement_readiness == "Ready" :
        return ("💡 Excellent job! You are well-prepared for Tier-1 companies. "
                "Focus on refining soft skills, speed, and keep practicing mock interviews.")
    elif company_fit == "Tier 2" and placement_readiness == "Ready" :
        return ("💼 You're on the right path! Focus on strengthening technical basics and communication. "
                "Practice aptitude and work on projects.")
    else:  # Not Ready
        return ("🚧 You're not quite ready yet for placements. Build your basics, practice daily, and seek mentorship. "
                "With consistent effort, you'll improve!")


if __name__ == '__main__':
    app.run(debug=True)
