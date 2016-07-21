from app import BattleField
from flask import Flask, render_template, url_for, request, redirect

#Tanya Boychenko

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    return render_template("index.html", title='Battle')


@app.route('/index', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        soldiers = int(request.form['soldiers'])
        vehicles = int(request.form['vehicles'])
        squads_number_ = int(request.form['squads_number'])
        armies_number_ = int(request.form['armies_number'])
        strategy_ = str(request.form['strategy'])

        if 5 <= soldiers + vehicles <= 10 and squads_number_ >= 2 \
                and armies_number_ >= 2:
            battle = BattleField.BattleField(armies_number=armies_number_,
                                             strategy=strategy_,
                                             squads_number=squads_number_,
                                             soldiers_number=soldiers,
                                             vehicles_number=vehicles)

            try:
                win = battle.start()
                print(win)
            except Exception:
                win = 'error'
        else:
            win = 0
        return redirect(url_for('result', win=win), code=302)


@app.route('/result/<win>', methods=['GET', 'POST'])
def result(win):
    return render_template("result.html", title='Result Battle', win=win)


if __name__ == "__main__":

    app.run(debug=True)
