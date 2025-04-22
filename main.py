from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/learning')
def learning():
    return render_template('learning.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/table_position')
def table_position():
    return render_template('table_position.html')

@app.route('/basic_game_flow')
def basic_game_flow():
    return render_template('basic_game_flow.html')

@app.route('/hand_ranking')
def hand_ranking():
    return render_template('hand_ranking.html')

@app.route('/betting_rules')
def betting_rules():
    return render_template('betting_rules.html')

if __name__ == '__main__':
    app.run(debug=True)

