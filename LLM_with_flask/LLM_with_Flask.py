# reference = https://github.com/MuhammadMoinFaisal/LargeLanguageModelsProjects/blob/main/Flask_LangChain_Recording/part3.py
############################################################################################################################
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return "AI Summary"

@app.route('/summary', methods=['GET', 'POST'])
def AI_summary():
    results = request.args.get('url')
    return results

if __name__ == '__main__':
    app.run(debug=True) ### debug=True allows modification without restart