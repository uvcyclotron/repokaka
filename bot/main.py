import json
from flask import Flask, render_template, request, url_for,jsonify
from flask_json_multidict import get_json_multidict
app = Flask(__name__)

@app.route('/<user>/<repo>/<method>',methods=['POST'])
def hello_world(user,repo,method):
        #Extracting the information from the request object
        request.body = request.form
        if request.headers['content-type'] == 'application/json':
                request.body = get_json_multidict(request)
        body = request.body

        # Formatting it as a dictionary
        request_dict={key: body[key] for key in body}
        print request_dict['payload']
        return "Obtained data"

if __name__ == '__main__':
  app.run()
