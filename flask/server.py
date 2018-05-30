from flask import *
import json
app = Flask(__name__)

IP = '0.0.0.0'
PORT = 8080

##############
#### HTML ####
##############

@app.route('/')
def view_root_list():
    return render_template('template.html')

@app.route('/<string:key>')
def view_root(key):
    return render_template('template.html')



##################
#### REST API ####
##################

# GET    : read
# POST   : write new
# PUT    : write new or update
# DELETE : delete

# RESPONSE CODE
# - 200 : OK
# - 201 : Created
# - 204 : No Content (Update, Delete success).
#         Unable to have return body. Will use 200 instead.
# - 400 : Bad Request
# - 404 : Not Found
# - 409 : Conflict

@app.route('/api/v1/<string:key>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_root(key):
    if request.method == 'GET':
        # check does key exist. return 404 if it doesn't.
        keys = ['test']
        if key not in keys:
            result = {
                'result':False,
                'error':"bad GET request. key '{}' doesn\'t exist.".format(key)
            }
            return make_response(jsonify(result), 404)

        #
        # READ THE ENTITY
        #

        result = {
            'result':True,
            'data':{
                'hello':'world'
            }
        }
        return make_response(jsonify(result), 200)

    elif request.method == 'POST':
        # check does key already exist. post doesn't update.
        keys = ['test']
        if key in keys:
            result = {
                'result':False,
                'error':"bad POST request. key '{}' already exists.".format(key)
            }
            return make_response(jsonify(result), 409)

        # parse request body
        try:
            print(request.data)
            body = json.loads(request.data)
        except:
            result = {
                'result':False,
                'error':'bad POST request. unable to parse json body.'
            }
            return make_response(jsonify(result), 400)

        #
        # WRITE THE ENTITY
        #

        result = {
            'result':True,
            'data':{
                'hello':'world'
            }
        }
        return make_response(jsonify(result), 201)


    elif request.method == 'PUT':
        # parse request body
        try:
            print(request.data)
            body = json.loads(request.data)
        except:
            result = {
                'result':False,
                'error':'bad PUT request. unable to parse json body.'
            }
            return make_response(jsonify(result), 400)

        keys = ['test']
        response_code = 200 if key in keys else 201
        #
        # WRITE OR UPDATE THE ENTITY
        #

        result = {
            'result':True,
            'data':{
                'hello':'world'
            }
        }
        return make_response(jsonify(result), response_code)


    elif request.method == 'DELETE':
        # check does key exist. return 404 if it doesn't.
        keys = ['test']
        if key not in keys:
            result = {
                'result':False,
                'error':"bad DELETE request. key '{}' doesn\'t exist.".format(key)
            }
            return make_response(jsonify(result), 404)

        #
        # DELETE THE ENTITY
        #

        result = {
            'result':True,
            'data':{
                'hello':'world'
            }
        }
        return make_response(jsonify(result), 200)



if __name__ == '__main__':
    app.debug = True
    app.run(host=IP, port=PORT)
