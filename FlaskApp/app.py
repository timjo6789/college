from flask import Flask, render_template, json, request
from werkzeug.security import generate_password_hash, check_password_hash
import external

CURRENT_WEEK = 'W02'


def pretty_time(seconds):
    minute, seconds = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)

    minute = f'{minute}m' if hour > 0 or minute > 0 else ''
    hour = f'{hour}h' if hour > 0 else ''
    return f'{hour}{minute}{seconds}s'


app = Flask(__name__)

app.jinja_env.globals.update(zip=zip)
app.jinja_env.globals.update(len=len)
app.jinja_env.globals.update(all=all)
app.jinja_env.globals.update(pretty_time=pretty_time)


@app.route('/<start_week>_<end_week>')
def show_weeks(start_week, end_week):
    print('showing weeks')
    output = external.get_multiple_assignment_tasks([start_week, end_week])
    return render_template('index.html', output=output)

@app.route('/')
def hay():
    return render_template('quick_access.html')


@app.route('/previous_task_viewer')
def previously():
    # return render_template('index.html', output=external.get_assignment_tasks(week_number))
    return render_template('index.html', output=external.get_assignment_tasks(CURRENT_WEEK))


@app.route('/<week>')
def a_week(week):
    return render_template('index.html', output=external.get_assignment_tasks(week))

@app.route('/done_<week>')
def a_done_week(week):
    return render_template('index.html', output=external.get_assignment_tasks(week, 1))


# @app.route('/task_viewer/<week_number>')
# def main(week_number):
@app.route('/task_viewer')
def main():
    # return render_template('index.html', output=external.get_assignment_tasks(week_number))
    return render_template('index.html', output=external.get_assignment_tasks(CURRENT_WEEK))


@app.route('/task_viewer_done')
def task_viewer_done():
    # return render_template('index.html', output=external.get_assignment_tasks(week_number))
    return render_template('index.html', output=external.get_assignment_tasks(CURRENT_WEEK, 1))


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/show_queries')
def show_queries():
    return 'ok ok fine.'

@app.route('/mark_done_duration', methods=['POST'])
def mark_done_duration():
    external.mark_done(request.form['assignment_id'], request.form['task_number'], request.form['time'], request.form['date'])
    print(request.form['time'], request.form['assignment_id'], request.form['task_number'])
    return 'ok ok fine.'

@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        print(request.form['actions'])
        if request.form['actions'] == 'See all':
            return render_template('test.html', keys=['assignment_id', 'class', 'week', 'title', 'deadline'], query_1=class_specific('W01', 'WDD 230'))
            # return 'AS YOU WISH'
        elif request.form['actions'] == 'saab':
            return render_template('test.html')
        return 'welp.'
    else:
        return render_template('test.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    return json.dumps({'html':'<span>return details</span>'})


if __name__ == "__main__":
    # app.run(host='172.24.96.1', port=5000)
    app.run(host='0.0.0.0', port=5000) # , port=5000)
