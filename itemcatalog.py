from flask import Flask, render_template, request, redirect, jsonify, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Drill

app = Flask(__name__)

engine = create_engine('sqlite:///drills.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

category0 = {'name': 'Goalie', 'id': 0}
category1 = {'name': 'Defenseman', 'id': 0}
category2 = {'name': 'Forward', 'id': 0}
categories = [category0, category1, category2]
drill0 = {'name': 'Butterfly post to post', 'id': 0, 'description': 'Step 1....Step 2...'}
drill1 = {'name': 'Three shots agles', 'id': 1, 'description': 'Step 1....Step 2...'}
drill2 = {'name': 'Five shots', 'id': 2, 'description': 'Step 1....Step 2...'}
drills = [drill0, drill1, drill2]

@app.route('/')
@app.route('/categories')
def showCategories():
    return render_template('categories.html', categories = categories)

@app.route('/category/<int:category_id>')
def showCategory(category_id):
    return render_template('category.html', category = category0, drills = drills)

@app.route('/category/<int:category_id>/<int:drill_id>')
def showDrill(category_id, drill_id):
    return render_template('showDrill.html', drill = drill0)

@app.route('/category/<int:category_id>/new')
def newDrill(category_id):
    return render_template('newDrill.html', category = category0)

@app.route('/category/<int:category_id>/<int:drill_id>/edit')
def editDrill(category_id, drill_id):
    return render_template('editDrill.html', category = category0, drill = drill0)

@app.route('/category/<int:category_id>/<int:drill_id>/delete')
def deleteDrill(category_id, drill_id):
    return render_template('deleteDrill.html', category = category0 , drill = drill0)

# @app.route('/restaurant/<int:restaurant_id>/menu/JSON')
# def restaurantMenuJSON(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
#     items = session.query(MenuItem).filter_by(
#         restaurant_id=restaurant_id).all()
#     return jsonify(MenuItems=[i.serialize for i in items])


# @app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
# def menuItemJSON(restaurant_id, menu_id):
#     Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
#     return jsonify(Menu_Item=Menu_Item.serialize)


# @app.route('/restaurant/JSON')
# def restaurantsJSON():
#     restaurants = session.query(Restaurant).all()
#     return jsonify(restaurants=[r.serialize for r in restaurants])


# # Show all restaurants
# @app.route('/')
# @app.route('/restaurant/')
# def showRestaurants():
#     restaurants = session.query(Restaurant).all()
#     # return "This page will show all my restaurants"
#     return render_template('restaurants.html', restaurants=restaurants)


# # Create a new restaurant
# @app.route('/restaurant/new/', methods=['GET', 'POST'])
# def newRestaurant():
#     if request.method == 'POST':
#         newRestaurant = Restaurant(name=request.form['name'])
#         session.add(newRestaurant)
#         session.commit()
#         return redirect(url_for('showRestaurants'))
#     else:
#         return render_template('newRestaurant.html')
#     # return "This page will be for making a new restaurant"

# # Edit a restaurant


# @app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
# def editRestaurant(restaurant_id):
#     editedRestaurant = session.query(
#         Restaurant).filter_by(id=restaurant_id).one()
#     if request.method == 'POST':
#         if request.form['name']:
#             editedRestaurant.name = request.form['name']
#             return redirect(url_for('showRestaurants'))
#     else:
#         return render_template(
#             'editRestaurant.html', restaurant=editedRestaurant)

#     # return 'This page will be for editing restaurant %s' % restaurant_id

# # Delete a restaurant


# @app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
# def deleteRestaurant(restaurant_id):
#     restaurantToDelete = session.query(
#         Restaurant).filter_by(id=restaurant_id).one()
#     if request.method == 'POST':
#         session.delete(restaurantToDelete)
#         session.commit()
#         return redirect(
#             url_for('showRestaurants', restaurant_id=restaurant_id))
#     else:
#         return render_template(
#             'deleteRestaurant.html', restaurant=restaurantToDelete)
#     # return 'This page will be for deleting restaurant %s' % restaurant_id


# # Show a restaurant menu
# @app.route('/restaurant/<int:restaurant_id>/')
# @app.route('/restaurant/<int:restaurant_id>/menu/')
# def showMenu(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
#     items = session.query(MenuItem).filter_by(
#         restaurant_id=restaurant_id).all()
#     return render_template('menu.html', items=items, restaurant=restaurant)
#     # return 'This page is the menu for restaurant %s' % restaurant_id

# # Create a new menu item


# @app.route(
#     '/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
# def newMenuItem(restaurant_id):
#     if request.method == 'POST':
#         newItem = MenuItem(name=request.form['name'], description=request.form[
#                            'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
#         session.add(newItem)
#         session.commit()

#         return redirect(url_for('showMenu', restaurant_id=restaurant_id))
#     else:
#         return render_template('newmenuitem.html', restaurant_id=restaurant_id)

#     return render_template('newMenuItem.html', restaurant=restaurant)
#     # return 'This page is for making a new menu item for restaurant %s'
#     # %restaurant_id

# # Edit a menu item


# @app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
#            methods=['GET', 'POST'])
# def editMenuItem(restaurant_id, menu_id):
#     editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
#     if request.method == 'POST':
#         if request.form['name']:
#             editedItem.name = request.form['name']
#         if request.form['description']:
#             editedItem.description = request.form['name']
#         if request.form['price']:
#             editedItem.price = request.form['price']
#         if request.form['course']:
#             editedItem.course = request.form['course']
#         session.add(editedItem)
#         session.commit()
#         return redirect(url_for('showMenu', restaurant_id=restaurant_id))
#     else:

#         return render_template(
#             'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

#     # return 'This page is for editing menu item %s' % menu_id

# # Delete a menu item


# @app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
#            methods=['GET', 'POST'])
# def deleteMenuItem(restaurant_id, menu_id):
#     itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
#     if request.method == 'POST':
#         session.delete(itemToDelete)
#         session.commit()
#         return redirect(url_for('showMenu', restaurant_id=restaurant_id))
#     else:
#         return render_template('deleteMenuItem.html', item=itemToDelete)
#     # return "This page is for deleting menu item %s" % menu_id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
