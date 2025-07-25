from flask import Flask, render_template, request, jsonify
from agents.main_agent import main_agent

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    user_query = data.get('query')
    response = main_agent(user_query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
