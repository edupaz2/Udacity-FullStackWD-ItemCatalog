from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash)
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# IMPORTS for Google Auth
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from database_setup import Base, Category, Drill, User

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']

engine = create_engine('sqlite:///drills.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
        return redirect('/login')
    return decorated_function

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html',
                           STATE=state, client_id=CLIENT_ID)


@login_required
@app.route('/about')
def showAbout():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('about.html',
                           STATE=state,
                           user=getCurrentUserInfo())


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')),
                                 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."),
            401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                    json.dumps('Current user is already connected.'),
                    200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data.get('name', '')
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h3>Welcome, '
    output += login_session['username']
    output += '!</h3>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/login')
    else:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
                                'Failed to revoke token for given user.'),
                                 400)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showLogin'))


@login_required
@app.route('/')
@app.route('/index')
def showIndex():
    print('login_session:', login_session)
    categories = session.query(Category).all()
    random_categories = random.sample(categories, min(4, len(categories)))
    drills = session.query(Drill).all()
    random_drills = random.sample(drills, min(2, len(drills)))
    return render_template('index.html',
                           user=getCurrentUserInfo(),
                           categories=random_categories,
                           random_drills=random_drills)


@login_required
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).all()
    return render_template('categories.html',
                           categories=categories,
                           user=getCurrentUserInfo())


@login_required
@app.route('/category/<int:category_id>')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    drills = session.query(Drill).filter_by(category_id=category_id).all()
    return render_template('category.html',
                           category=category,
                           drills=drills,
                           user=getCurrentUserInfo())


@login_required
@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newDrill(category_id):
    if request.method == 'POST':
        toCreate = Drill(name=request.form['name'],
                         description=request.form['description'],
                         category_id=category_id,
                         user_id=getUserID(login_session['email']))
        session.add(toCreate)
        session.commit()
        return redirect(url_for('showCategory',
                                category_id=category_id))
    else:
        category = session.query(Category).filter_by(id=category_id).one_or_none()
        return render_template('newDrill.html',
                               category=category,
                               user=getCurrentUserInfo())


@login_required
@app.route('/drill/<int:drill_id>')
def showDrill(drill_id):
    toView = session.query(Drill).filter_by(id=drill_id).one_or_none()
    return render_template('drill.html',
                           drill=toView,
                           user=getCurrentUserInfo())


@login_required
@app.route('/drill/<int:drill_id>/edit', methods=['GET', 'POST'])
def editDrill(drill_id):
    toEdit = session.query(Drill).filter_by(id=drill_id).one_or_none()
    if (request.method == 'POST' and
            toEdit.user_id == getUserID(login_session['email'])):
        if request.form['name']:
            toEdit.name = request.form['name']
        if request.form['description']:
            toEdit.description = request.form['description']
        session.add(toEdit)
        session.commit()
        category_id = toEdit.category_id
        return redirect(url_for('showCategory',
                                category_id=category_id))
    else:
        return render_template('editDrill.html',
                               drill=toEdit,
                               user=getCurrentUserInfo())


@login_required
@app.route('/drill/<int:drill_id>/delete', methods=['GET', 'POST'])
def deleteDrill(drill_id):
    toDelete = session.query(Drill).filter_by(id=drill_id).one_or_none()
    if (request.method == 'POST' and
            toDelete.user_id == getUserID(login_session['email'])):
        category_id = toDelete.category_id
        session.delete(toDelete)
        session.commit()
        return redirect(url_for('showCategory',
                                category_id=category_id))
    else:
        return render_template('deleteDrill.html',
                               drill=toDelete,
                               user=getCurrentUserInfo())


@login_required
@app.route('/drill/<int:drill_id>/JSON')
def drillJSON(drill_id):
    drill = session.query(Drill).filter_by(id=drill_id).one_or_none()
    return jsonify(drill=drill.serialize)


@login_required
@app.route('/category/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    drills = session.query(Drill).filter_by(category_id=category_id).all()
    return jsonify(category=category.serialize,
                   drills=[d.serialize for d in drills])


@login_required
@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# Helper functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one_or_none()
    return user.id


def getUserInfo(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one_or_none()
        return user
    except:
        return None


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except:
        return None


def getCurrentUserInfo():
    return getUserInfo(login_session['user_id'])

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
