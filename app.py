from flask import Flask, render_template, jsonify
import random
from data import words

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/words')
def get_words():
    random_words = random.sample(words, 50)
    return jsonify(random_words)

if __name__ == '__main__':
    app.run(debug=True)
