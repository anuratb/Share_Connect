# Share_Connect

This is a web app created using <a href="https://www.djangoproject.com/">Django</a> , Bootstrap, Jquery,HTML,CSS,JS.
SQLite is used during development ,but migrated to PostgreSQL, while deploying with the help of <a href="https://pypi.org/project/django-heroku/">django-heroku</a> utility.
<hr>

## About Share_Connect
A simple blog app for posting Blogs, it supports upvoting,downvoting on the blogs and maintains a rating of the user
based on the upvotes and downvotes.One can also send <i>friend requests</i> and connect with other users.As such the app
has the support of setting the <i>visibility</i> of the blogs ,namely, <i>Public,Friends and Only_me</i>.Friendships
are maintained using many to many relationships in the dbms.

## Deployment
The app has been deployed to heroku at : https://share-connect.herokuapp.com/users/
