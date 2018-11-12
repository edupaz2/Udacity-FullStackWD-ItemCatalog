# Udacity-FullStackWD-ItemCatalog
Repository for Item Catalog project for Udacity's Full Stack Web Developer Nanodegree

# Hockey Drill DB App:
Our app will be a database for ice hockey drills. Drills are grouped by categories and by skills.

The drills categories will be:
- Goalie drills.
- Defenseman drills.
- Forward drills.
- Offensive drills.
- Defensive drills.
- Power Play drills.
- Penalty killing drills.
- Fun games drills.
- Conditioning drills.
- Warm up drills.

Also every drill will make the players emphasize on one or several basic skills, which are:
- Forward skating.
- Backward skating.
- Stickhandling.
- Agility.
- Balance.
- Passing.
- Shooting.

# How to use TODO:
- Install vagrant.
- Use vagrantfile.
- Connect to localhost:8000.

# Design of the site:
## Pages:
The pages are:
- /categories and /: Show all categories.
- /category/<int:category_id>/drills: Show a category's drills.
- /category/<int:category_id>/drills/new: Creates a new drill.
- /category/<int:category_id>/drills/<int:drill_id>/edit: Edits an existing drill.
- /category/<int:category_id>/drills/<int:drill_id>/delete: Deletes an existing drill.

## Routing:
Connection between URL -> method - Message:
- /categories and / 										-> showCategories() -> "Main page showing all my categories"
- /category/<int:category_id>/drills 						-> showCategory()	-> "This page shows drills from category %s" category_id
- /category/<int:category_id>/drills/new					-> newDrill()		-> "This page creates a new drill for category %s" category_id
- /category/<int:category_id>/drills/<int:drill_id>/edit 	-> editDrill()		-> "This page edits drill %s" drill_id
- /category/<int:category_id>/drills/<int:drill_id>/delete	-> deletesDrill()	-> "This page edits deletes %s" drill_id

## Templates and Forms:


 