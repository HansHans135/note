import json
from datetime import datetime, timezone, timedelta
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def get_now():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    now = dt2.strftime('%Y-%m-%d')
    # %H:%M:%S
    return now


@app.route('/')
def web_home():
    with open('data.json', 'r', encoding='utf-8')as f:
        data = json.load(f)
    return render_template('index.html', data=data, now=get_now(), edit=False)


@app.route('/edit')
def web_edit():
    with open('data.json', 'r', encoding='utf-8')as f:
        data = json.load(f)
    return render_template('index.html', data=data, now=get_now(), edit=True)


@app.route('/add', methods=['GET', 'POST'])
def web_add():
    if request.method == 'POST':
        with open('data.json', 'r', encoding='utf-8')as f:
            data = json.load(f)
        data[request.form['tp']].append(
            {'date': request.form['date'], 'text': request.form['text'], 'cl': request.form['cl']})
        with open('data.json', 'w+', encoding='utf-8')as f:
            json.dump(data, f)
        return redirect(f'/')
    return render_template('add.html')


@app.route('/del/<tp>/<page>')
def web_del(tp, page):
    with open('data.json', 'r', encoding='utf-8')as f:
        data = json.load(f)
    new=[]
    for i in data[tp]:
        if not i["text"]==page:
            new.append(i)
    data[tp]=new
    with open('data.json', 'w+', encoding='utf-8')as f:
        json.dump(data, f)
    return redirect(f'/')


app.run(host='0.0.0.0', port=25565, debug=True)
