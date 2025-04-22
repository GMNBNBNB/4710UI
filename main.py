from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'

with open('quiz_data.json') as f:
    quiz_data = json.load(f)['quizzes']

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/learning')
def learning():
    return render_template('learning.html')

@app.route('/quiz')
def quiz_home():
    return render_template('quiz_home.html')

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    if 'answers' not in session:
        session['answers'] = {}

    if quiz_id < 1 or quiz_id > len(quiz_data):
        return "Invalid quiz ID", 404

    quiz = quiz_data[quiz_id - 1]

    # Handle submission → show feedback
    if request.method == 'POST':
        # record answer
        if 'options' in quiz:
            sel = request.form.get('option')
            session['answers'][str(quiz_id - 1)] = int(sel) if sel is not None else None
        elif 'cards' in quiz:
            sel_cards = request.form.getlist('selected_cards')
            session['answers'][str(quiz_id - 1)] = sel_cards

        session.modified = True

        # determine correctness
        correct = False
        if 'answer_index' in quiz:
            correct = (session['answers'][str(quiz_id - 1)] == quiz['answer_index'])
        elif 'correct_cards' in quiz:
            correct = (set(session['answers'][str(quiz_id - 1)]) == set(quiz['correct_cards']))

        # build explanation
        explanation = quiz.get('explanation')
        if not explanation and 'answer_index' in quiz:
            correct_opt = quiz['options'][quiz['answer_index']]
            if isinstance(correct_opt, list):
                # options like ['6♣', '8♦', ...]
                explanation = "Correct answer: " + " ".join(correct_opt)
            else:
                # simple string options
                explanation = "Correct answer: " + correct_opt

        # decide where "Next" goes
        if quiz_id < len(quiz_data):
            next_url = url_for('quiz', quiz_id=quiz_id + 1)
        else:
            next_url = url_for('results')

        return render_template(
            'quiz.html',
            quiz=quiz,
            quiz_id=quiz_id,
            feedback={'correct': correct, 'explanation': explanation},
            next_url=next_url
        )

    # initial GET → no feedback
    return render_template('quiz.html', quiz=quiz, quiz_id=quiz_id)

@app.route('/results')
def results():
    answers = session.get('answers', {})
    correct = 0

    for i, quiz in enumerate(quiz_data):
        key = str(i)
        if key not in answers:
            continue

        # 单选题评分
        if 'answer_index' in quiz:
            if answers[key] == quiz['answer_index']:
                correct += 1

        # 选牌题评分
        elif 'correct_cards' in quiz:
            if set(answers[key]) == set(quiz['correct_cards']):
                correct += 1

    total = len(quiz_data)
    score = f"{correct}/{total}"
    passed = (correct == total)
    return render_template('results.html',
                           correct=correct,
                           total=total,
                           score=score,
                           passed=passed)

@app.route('/table_position')
def table_position():
    return render_template('table_position.html')

@app.route('/basic_game_flow')
def basic_game_flow():
    return render_template('basic_game_flow.html')

if __name__ == '__main__':
    app.run(debug=True)


