import json
from flask import Flask, render_template, request, url_for,jsonify
from flask_json_multidict import get_json_multidict
app = Flask(__name__)

@app.route('/<user>/<repo>/<method>',methods=['POST'])
def hello_world(user,repo,method):
        print user + " " + repo + " " + method

        request.body = request.form
        if request.headers['content-type'] == 'application/json':
                request.body = get_json_multidict(request)
        #print type(request.get_data())
        body = request.body
        print "jsoned:++++++++++++++++++++"
        request_dict={key: body[key] for key in body}
        print request_dict['payload']
        print "below is form++++++++++++++++++++++++++++++++++++"
        print request.form
        print "Args is +++++++++++++++++++++++++++++++++++++++++"
        print request.args
        print "Request.data is below \n"
        print request.data
        print "request.files is below \n"
        print request.files
        return 'Hello from Flask'+ user +" " + repo

if __name__ == '__main__':
  app.run()
