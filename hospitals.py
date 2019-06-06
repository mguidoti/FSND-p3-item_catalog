from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for
from flask import flash, make_response
from flask import session as login_session

import random
import string
import httplib2
import json
import requests

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Hospital, Condition

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///themehospitals.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Defining the client secret file for the two Oauth2 providers used
# in this application - Google and Facebook
#
# Evaluator: please, add your own files here!
g_client_secret_file = 'g_client_secret.json'
fb_client_secret_file = 'fb_client_secret.json'

# Getting my client_id from the g_client_secret_file
client_id = json.loads(
    open(g_client_secret_file, 'r').read())['web']['client_id']


# Oauth2 System implementation - Google and Facebook, anti-forgery,
# adding users to the database, collecting basic information from the
# providers only (username, e-mail and picture), using only /login as
# access route
@app.route('/login/')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))  # noqa
    login_session['state'] = state

    return render_template('login.html', STATE=state)


# This look up if the user has the internal credentials to access
# specific parts of the website by looking at the e-mail address
# associated with the oauth third-party login, meaning that, if the
# user used the same email in google and facebook, he can login with
# either of these third-party oauth2 providers and it will work.

# This takes the data in a login_session and creates a new users with
# that data. Then returns a user id of the new user created.
def create_user(login_session):
    new_user = User(name=login_session['username'], gender='Who cares?', type='real', email=login_session['email'], picture=login_session['picture'])  # noqa
    session.add(new_user)
    session.commit()

    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# This function simply returns a user object from the database based on
# a user id.
def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# This returns a user id based on an e-mail address. If there is no
# user with that particular e-mail, returns None.
def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Oauth2 for Facebook - Using anti-forgery system
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Anti-forgery system. Checks if the same code is being passed back
    # by the user
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter. You''re not who you say you''re!'), 401)  # noqa
        response.headers['Content-Type'] = 'application/json'

        return response

    access_token = request.data

    # Extract and exchange the short-lived for the long-lived token
    fb_id = json.loads(open(fb_client_secret_file, 'r').read())['web']['app_id']  # noqa
    fb_secret = json.loads(open(fb_client_secret_file, 'r').read())['web']['app_secret']  # noqa

    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (fb_id, fb_secret, access_token)  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Using new token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"

    # Strip expire tag from access token, so we can use it directly into
    # the graph api calls later
    fb_token = result.split(',')[0].split(':')[1].replace('"', '')

    # Actually make the API call to the graph API to get user data
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % fb_token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Reads the returning data and populates the login_session
    data = json.loads(result)

    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token is stored in the login_session in order to
    # properly logout if requested by the user
    login_session['access_token'] = fb_token

    # Facebook uses a different API call to get a profile picture. Here
    # it' is:
    url = 'https://graph.facebook.com/me/picture?redirect&access_token=%s&height=200&width=200' % fb_token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]['url']

    # Check if the user already exists in the database. If not, creates
    # a new user in the database
    user_id = get_user_id(login_session['email'])

    if not user_id:
        user_id = create_user(login_session)

    # Add the defintiely user_id to the login_session
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' "style = "width: 250px;'
    output += 'height: 250px;'
    output += 'border-radius: 150px;'
    output += '-webkit-border-radius: 150px;'
    output += '-moz-border-radius: 150px;">'

    flash("You are now logged in as %s" % login_session['username'])

    return output


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Anti-forgery system. Checks if the same code is being passed back
    # by the user
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Receive and collect the one-time code sent by the website after
    # login
    auth_code = request.data

    try:
        # Upgrade the authorization or one-time code into a credentials
        # object
        oauth_flow = flow_from_clientsecrets(g_client_secret_file, scope='')
        # Define as 'postmessage' that this is the one-time code being
        # sent to the server
        oauth_flow.redirect_uri = 'postmessage'
        # Initiate the exchange passing the one-time code, if it goes
        # well, it creates the object, if goes bad, raises the
        # following exception
        credentials = oauth_flow.step2_exchange(auth_code)

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Check that the access token is valid
    # Store the access token inside a variable
    access_token = credentials.access_token

    # Checks if the token is valid by making an API call using the
    # access token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort mission bt
    # sending an error message.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Verify if the access token is from the intended user. If not,
    # send error message
    google_id = credentials.id_token['sub']

    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Verify if the access token is valid for this app. If not,
    # send error message
    if result['issued_to'] != client_id:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Check to see if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')

    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(json.dumps('Current user is connected'), 200)
        response.headers['Content-Type'] = 'application/json'

        return response

    # If everything is fine until now, store the access token in the
    # session for later use
    login_session['provider'] = 'google'
    login_session['access_token'] = access_token
    login_session['google_id'] = google_id

    # Get User Info using the access token, but only the data allowed
    # by my token scope which is defined in the button setup
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Checks if the user already exists in the database. If not creates
    # a new user into the database.
    user_id = get_user_id(login_session['email'])

    if not user_id:
        user_id = create_user(login_session)

    # Add the defintiely user_id to the login_session
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' "style = "width: 250px;'
    output += 'height: 250px;'
    output += 'border-radius: 150px;'
    output += '-webkit-border-radius: 150px;'
    output += '-moz-border-radius: 150px;">'

    flash("You are now logged in as %s" % login_session['username'])

    return output


# Disconnects a user by deleting all information stored in the
# login_session only after revoking its token with the Oauth2 providers
@app.route('/disconnect')
def disconnect():
    # Check if the user is actually connected by the presence of the
    # access token in the login_session
    access_token = login_session.get('access_token')

    if access_token is None:
        flash("Can't logout. User not connected.")

        return redirect(url_for('show_hospitals'))

    # Check which is the provider used, and call the right function
    if 'provider' in login_session:
        if login_session['provider'] == 'google':

            # Execute HTTP GET request to revoke current token
            url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token  # noqa
            h = httplib2.Http()
            result = h.request(url, 'GET')[0]

            if result['status'] == '200':
                del login_session['google_id']

            else:
                # For whatever reason, the given token was invalid
                flash("Failed to revoke token for your user. No idea why. Sorry.")  # noqa

                return redirect(url_for('show_hospitals'))

        elif login_session['provider'] == 'facebook':

            # Get facebook id from the login_session
            facebook_id = login_session.get('facebook_id')

            # Execute HTTP DELETE request to revoke current token
            url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)  # noqa
            h = httplib2.Http()
            result = h.request(url, 'DELETE')[1]

            del login_session['facebook_id']

        # Delete common information among the providers
        del login_session['provider']
        del login_session['user_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        # Also delete the access_token from the login_session
        del login_session['access_token']

        # Flash a confirmation message to the user
        flash("You have successfully been logged out.")

        return redirect(url_for('show_hospitals'))

    # In case of an unconnected user trying to logout, flash error
    # message and redirects to the hospitals page
    else:
        flash("You were not logged.")

        return redirect(url_for('show_hospitals'))


# Show all the hospitals
@app.route('/')
@app.route('/hospitals/')
@app.route('/hospital/')
def show_hospitals():
    # Gets all hospitals in the database, ordering alphabetically
    hospitals = session.query(Hospital).order_by(asc(Hospital.name))

    # Check if the user is logged in and redirects accordingly
    if 'username' not in login_session:
        return render_template('public_hospitals.html',
                               hospitals=hospitals)

    else:
        return render_template('hospitals.html', hospitals=hospitals)


# Create a new hospital
@app.route('/hospital/new/', methods=['GET', 'POST'])
def new_hospital():
    # Check if the user is logged in and redirects accordingly
    if 'username' not in login_session:
        return redirect('/login')

    # If the user is logged in, then proceed
    if request.method == 'POST':
        # Actually create the new hospital
        new_hospital = Hospital(name=request.form['name'], user_id=login_session['user_id'], accepted_insurance=request.form['insurance'], address=request.form['address'], phone=request.form['phone'])  # noqa

        # Add to the database and flash a confirmation message
        session.add(new_hospital)
        flash('New hospital %s successfully created' % new_hospital.name)
        session.commit()

        return redirect(url_for('show_hospitals'))

    else:
        return render_template('new_hospital.html')


# Edit a hospital
@app.route('/hospital/<int:hospital_id>/edit/', methods=['GET', 'POST'])
def edit_hospital(hospital_id):
    # Check if the user is logged in and redirects accordingly
    if 'username' not in login_session:
        return redirect('/login')

    # Retrieves the hospital to edit
    edited_hospital = session.query(Hospital).filter_by(id=hospital_id).one()

    # Check if the user has the access to edit the hospital
    if edited_hospital.user_id != login_session['user_id']:
        return "<script>function myFunction() { alert('You are not authorized to edit this hospital. Please create your own hospital in order to edit.')}</script><body onload='myFunction()'>"  # noqa

    # Control variable to check if any changed happened or not
    changes = False

    # Make the actual changes, if they were made by the user
    if request.method == 'POST':
        if request.form['name'] != edited_hospital.name:
            edited_hospital.name = request.form['name']
            changes = True

        if request.form['insurance'] != edited_hospital.accepted_insurance:
            edited_hospital.accepted_insurance = request.form['insurance']
            changes = True

        if request.form['address'] != edited_hospital.address:
            edited_hospital.address = request.form['address']
            changes = True

        if request.form['phone'] != edited_hospital.phone:
            edited_hospital.phone = request.form['phone']
            changes = True

        # Check if there was any changes to flash the right message
        if changes:
            session.add(edited_hospital)
            flash('Hospital %s successfully modified!' % edited_hospital.name)
            session.commit()

        else:
            flash('Nothing changed for hospital %s!' % edited_hospital.name)

        return redirect(url_for('show_conditions', hospital_id=edited_hospital.id))  # noqa

    else:
        return render_template('edit_hospital.html', hospital=edited_hospital)


# Delete a hospital
@app.route('/hospital/<int:hospital_id>/delete/', methods=['GET', 'POST'])
def delete_hospital(hospital_id):
    # Check if the user is logged in and redirects accordingly
    if 'username' not in login_session:
        return redirect('/login')

    # Retrieves the hospital to delete
    hospital_to_delete = session.query(Hospital).filter_by(id=hospital_id).one()  # noqa

    # Check if the user has the access to delete the hospital
    if hospital_to_delete.user_id != login_session['user_id']:
        return "<script>function myFunction() { alert('You are not authorized to delete this hospital. Please create your own hospital if you want to delete something.')}</script><body onload='myFunction()'>"  # noqa

    # Delete the hospital as required
    if request.method == 'POST':
        session.delete(hospital_to_delete)
        flash('Hospital %s successfully deleted ;(' % hospital_to_delete.name)
        session.commit()

        return redirect(url_for('show_hospitals', hospital_id=hospital_id))

    else:
        return render_template('delete_hospital.html', hospital=hospital_to_delete)  # noqa


# Show the list of conditions treated in a given hospital
@app.route('/hospital/<int:hospital_id>/')
@app.route('/hospital/<int:hospital_id>/treatments/')
@app.route('/hospital/<int:hospital_id>/conditions/')
def show_conditions(hospital_id):
    # Retrieves the hospital and then, the list of conditions associated
    # with that hospital
    hospital = session.query(Hospital).filter_by(id=hospital_id).one()
    conditions = session.query(Condition).filter_by(hospital_id=hospital_id).all()  # noqa

    # Checks if the hospital's creator user is on my database
    creator = get_user_info(hospital.user_id)

    # Compares to the current user id, if it's logged
    if 'username' not in login_session or creator.id != login_session['user_id']:  # noqa
        return render_template('public_conditions.html', conditions=conditions, hospital=hospital, creator=creator)  # noqa

    else:
        return render_template('conditions.html', conditions=conditions, hospital=hospital, creator=creator)  # noqa


# Add a new condition to a given hospital
@app.route('/hospital/<int:hospital_id>/condition/new/', methods=['GET', 'POST'])  # noqa
def new_condition(hospital_id):
    # Check if the user is logged in and redirects accordingly
    if 'username' not in login_session:
        return redirect('/login')

    # Retrieves the hospital
    hospital = session.query(Hospital).filter_by(id=hospital_id).one()

    # Compares the current user id with the hospital users id
    if hospital.user_id != login_session['user_id']:
        return "<script>function myFunction() { alert('You are not authorized to add a condition in this hospital. Please create your own hospital in order to proceed.')}</script><body onload='myFunction()'>"  # noqa

    if request.method == 'POST':
        # Actually create the new condition
        new_condition = Condition(name=request.form['name'], cause=request.form['cause'], sympton=request.form['sympton'], cure=request.form['cure'], cost=request.form['cost'], type=request.form['type'], hospital_id=hospital_id, user_id=login_session['user_id'])  # noqa

        session.add(new_condition)
        flash('Condition %s added successfully!' % (new_condition.name))
        session.commit()

        return redirect(url_for('show_conditions', hospital_id=hospital_id))

    else:
        return render_template('new_condition.html', hospital_id=hospital_id)


# Edit a condition in a given hospital
@app.route('/hospital/<int:hospital_id>/condition/<int:condition_id>/edit/', methods=['GET', 'POST'])  # noqa
def edit_condition(hospital_id, condition_id):
    # Check if the user is logged in and redirects accordingly
    if 'username' not in login_session:
        return redirect('/login')

    # Retrieves the hospital, and the condition to be editted hospital
    hospital = session.query(Hospital).filter_by(id=hospital_id).one()
    edited_condition = session.query(Condition).filter_by(id=condition_id).one()  # noqa

    # Compares the current user id with the hospital users id
    if hospital.user_id != login_session['user_id']:
        return "<script>function myFunction() { alert('You are not authorized to edit a condition in this hospital. Please create your own hospital in order to proceed.')}</script><body onload='myFunction()'>"  # noqa

    # Control variable to check if any changed happened or not
    changes = False

    # Make the actual changes, if they were made by the user
    if request.method == 'POST':
        if request.form['name'] != edited_condition.name:
            edited_condition.name = request.form['name']
            changes = True

        if request.form['cause'] != edited_condition.cause:
            edited_condition.cause = request.form['cause']
            changes = True

        if request.form['sympton'] != edited_condition.sympton:
            edited_condition.sympton = request.form['sympton']
            changes = True

        if request.form['cure'] != edited_condition.cure:
            edited_condition.cure = request.form['cure']
            changes = True

        if request.form['cost'] != edited_condition.cost:
            edited_condition.cost = request.form['cost']
            changes = True

        if request.form['type'] != edited_condition.type:

            edited_condition.type = request.form['type']
            changes = True

        # Check if there was any changes to flash the right message
        if changes:
            print('why?')
            session.add(edited_condition)
            flash('Condition %s successfully modified!' % edited_condition.name)  # noqa
            session.commit()

        else:
            flash('Nothing changed for condition %s!' % edited_condition.name)

        return redirect(url_for('show_conditions', hospital_id=hospital_id))

    else:
        return render_template('edit_condition.html', hospital_id=hospital_id, condition_id=condition_id, condition=edited_condition)  # noqa


# Delete a condition in a given hospital
@app.route('/hospital/<int:hospital_id>/condition/<int:condition_id>/delete/', methods=['GET', 'POST'])  # noqa
def delete_condition(hospital_id, condition_id):
    if 'username' not in login_session:
        return redirect('/login')

    # Retrieves the hospital, and the condition to be editted hospital
    hospital = session.query(Hospital).filter_by(id=hospital_id).one()
    condition_to_delete = session.query(Condition).filter_by(id=condition_id).one()  # noqa

    # Compares the current user id with the hospital users id
    if hospital.user_id != login_session['user_id']:
        return "<script>function myFunction() { alert('You are not authorized to delete a condition in this hospital. Please create your own hospital in order to proceed.')}</script><body onload='myFunction()'>"  # noqa

    if request.method == 'POST':
        # Actually delete the condition
        session.delete(condition_to_delete)
        flash('Condition %s successfully deleted ;(' % (condition_to_delete.name))  # noqa
        session.commit()

        return redirect(url_for('show_conditions', hospital_id=hospital_id))

    else:
        return render_template('delete_condition.html', hospital=hospital, condition=condition_to_delete)  # noqa


# API Endoints returning JSON
#
# This first endpoint returns all the data available for all hospitals
# in the database
@app.route('/hospital/JSON')
@app.route('/hospitals/JSON')
def hospitals_JSON():
    hospitals = session.query(Hospital).all()

    return jsonify(hospitals=[hospital.serialize for
                              hospital in hospitals])


# This second endpoint returns all conditions available for treatment
# in one given hospital
@app.route('/hospital/<int:hospital_id>/JSON')
@app.route('/hospital/<int:hospital_id>/conditions/JSON')
@app.route('/hospital/<int:hospital_id>/treatments/JSON')
def hospital_treatments_JSON(hospital_id):
    hospital = session.query(Hospital).filter_by(id=hospital_id).one()
    conditions = session.query(Condition).filter_by(hospital_id=hospital.id).all()  # noqa

    return jsonify(
        Hospital=hospital.serialize,
        Conditions=[condition.serialize for condition in conditions])


# This third and final endpoint returns all information available for
# one given condition, from one given hospital only. This means that,
# if one or more hospitals treat the same condition, the data on the
# prices won't be included here - you would have to find them one by
# one
@app.route('/hospital/<int:hospital_id>/condition/<int:condition_id>/JSON')
def condition_JSON(hospital_id, condition_id):
    condition = session.query(Condition).filter_by(id=condition_id).one()

    return jsonify(condition=condition.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
