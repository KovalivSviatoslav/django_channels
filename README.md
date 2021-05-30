Populate db:
 - ./manage.py migrate
 - ./manage.py loaddata data.json --app=posts
 - ./manage.py loaddata data.json --app=comments

Create few superusers to test sending comments.