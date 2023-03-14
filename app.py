from flask import request
import main as ms
# import main Flask class and request object
from flask import Flask, request
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

# create the Flask app
app = Flask(__name__)

@app.route('/')
def query_example():
    return 'email : trumxuquang@gmail.com'

@app.route('/', methods=['POST'])
def query_examples():
    return 'email : trumxuquang@gmail.com'

# GET requests will be blocked
@app.route('/evnscp', methods=['POST'])
def json_evnscp():
    
    request_data = request.get_json() #get all request
    
    username = request_data['username']
    password = request_data['password']
    fromMonth = request_data['fromMonth']
    fromYear = request_data['fromYear']
    isxml = False


    json = ms.get_hoa_don(username, password, fromMonth, fromYear)
    if isxml:
        json = dicttoxml(json)
        dom = parseString(json)
        '''
        with open('xml1.xml', 'w') as ofh:
            print(dom.toprettyxml(), file=ofh)
        '''
        json = dom.toprettyxml()

    return json


# GET requests will be blocked
@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = None
    framework = None
    python_version = None
    example = None
    boolean_test = None

    if request_data:
        if 'language' in request_data:
            language = request_data['language']

        if 'framework' in request_data:
            framework = request_data['framework']

        if 'version_info' in request_data:
            if 'python' in request_data['version_info']:
                python_version = request_data['version_info']['python']

        if 'examples' in request_data:
            if (type(request_data['examples']) == list) and (len(request_data['examples']) > 0):
                example = request_data['examples'][0]

        if 'boolean_test' in request_data:
            boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, host="0.0.0.0", port=50000)