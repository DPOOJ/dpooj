from flask import Flask, request
import random

app = Flask(__name__)

judging = False
hasInfo = False
requiredInfo = False

@app.route('/index', methods=['GET', 'POST'])
def index():
    return {
        'username': 'test',
    }

@app.route('/progress', methods=['GET', 'POST'])
def progress():
    global judging
    global hasInfo
    if not judging:
        return {
            'AC': 0,
            'WA': 0,
            'TLE': 0,
            'RE': 0,
            'tot' : 0,
            'judging': judging
        }
    judging = random.choice([True, True, True, False])
    hasInfo = True
    tot = random.randint(0, 50)
    AC = random.randint(0, tot)
    non = random.randint(0, 10)
    return {
        'AC': AC,
        'WA': tot - AC,
        'TLE': 5,
        'RE': 5,
        'tot' : tot + non,
        'judging': judging
    }

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print(request.files['file'])
    return {
        'success': 'true'
    }

@app.route('/submit', methods=['GET', 'POST'])
def submib():
    global judging
    judging = True
    return {
        'success': 'true'
    }
user = 'null'
@app.route('/user', methods=['GET', 'POST'])
def userID():
    global user
    logout = random.randint(0, 10)
    if logout == 0:
        user = 'null'
        print('log out')
    return user

@app.route('/login', methods=['POST'])
def login():
    global user
    user = 'test1'
    return 'success'

@app.route('/signup', methods=['POST'])
def signup():
    return 'success'

@app.route('/download', methods=['GET', 'POST'])
def download():
    return [
        {
        'no' : random.randint(1, 10),
        'result' : random.choice(['WA', 'AC', 'TLE', 'RE']),
        'download': '/download',
        'show': {
            'in' : 'x+1',
            'ans' : 'x+1',
            'out' : random.randint(0, 10)
            },
        },
        {
        'no' : random.randint(1, 10),
        'result' : random.choice(['WA', 'AC', 'TLE', 'RE']),
        'download': '/download',
        'show': {
            'in' : 'x+1',
            'ans' : 'x+1',
            'out' : random.randint(0, 10)
            },
        },
        {
        'no' : random.randint(1, 10),
        'result' : random.choice(['WA', 'AC', 'TLE', 'RE']),
        'download': '/download',
        'show': {
            'in' : 'x+1',
            'ans' : 'x+1',
            'out' : random.randint(0, 10)
            },
        },
        {
        'no' : random.randint(1, 10),
        'result' : random.choice(['WA', 'AC', 'TLE', 'RE']),
        'download': '/download',
        'show': {
            'in' : 'x+1',
            'ans' : 'x+1',
            'out' : random.randint(0, 10)
            },
        },
        {
        'no' : random.randint(1, 10),
        'result' : random.choice(['WA', 'AC', 'TLE', 'RE']),
        'download': '/download',
        'show': {
            'in' : 'x+1',
            'ans' : 'x+1',
            'out' : random.randint(0, 10)
            },
        },
        {
        'no' : random.randint(1, 10),
        'result' : random.choice(['WA', 'AC', 'TLE', 'RE']),
        'download': '/download',
        'show': {
            'in' : '1',
            'ans' : '2',
            'out' : '3'
            },
        },
    ]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000',debug=True)
