# Udacity-FullStackWD-ItemCatalog
Repository for Item Catalog project for Udacity's Full Stack Web Developer Nanodegree

# Hockey Drill DB App:
Our app will be a database for ice hockey drills. Drills are grouped by categories and by skills.

Users will be able to login using Google Authentication system and:
- Navigate through Categories.
- View all drills created by other users and themselves.
- Edit and delete drills created by them.

The drills categories will be:
- Offensive drills.
- Defensive drills.
- Forward drills.
- Defenseman drills.
- Goalie drills.
- Warm-up drills.
- Shooting drills.
- Passing drills.
- Power Play drills.
- Penalty killing drills.
- Fun games drills.
- Conditioning drills.

# To run this project:

1. Install Vagrant and VirtualBox
2. Clone the project: git clone https://github.com/edupaz2/Udacity-FullStackWD-ItemCatalog.git
3. Launch the Vagrant VM (vagrant up)
4. Connect to Vagrant VM (vagrant ssh)
5. Run your application within the VM (python /vagrant/itemcatalog.py)
6. Access and test your application by visiting http://localhost:5000 locally


# Design of the site:
## Pages:
The pages are:
- /login: For login purposes with Google Authentication. (login.html)
- / and /index: Landing page after login. (index.html)
- /categories: Show all categories. (categories.html)
- /category/<int:category_id>: Show a category information. (category.html)
- /category/<int:category_id>/new: For creating a new drill. (newDrill.html)
- /drill/<int:drill_id>: Show a drill information. (drill.html)
- /drill/<int:drill_id>/edit: For editing a drill. (editDrill.html)
- /drill/<int:drill_id>/delete: For deleting a drill. (deleteDrill.html)


 