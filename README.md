# Share_Connect

This is a web app created using <a href="https://www.djangoproject.com/">Django</a> , Bootstrap, Jquery,HTML,CSS,JS.
SQLite is used during development ,but migrated to Pogresql, while deploying with the help of <a href="https://pypi.org/project/django-heroku/">django-heroku</a> utility.
<hr>

## About Share_Connect
A simple blog app for posting Blogs, it supports upvoting,downvoting on the blogs and maintains a rating of the user
based on the upvotes and downvotes.One can also send <i>friend requests</i> and connect with other users.As such the app
has the support of setting the <i>visibility</i> of the blogs ,namely, <i>Public,Friends and Only_me</i>.Friendships
are maintained using many to many relationships in the dbms.

## Steps to run the development server

- In blog_backend/settings.py set the Secret key for development (any large random value),set DEBUG to True ,and set the EMAIL_HOST_USER and EMAIL_HOST_PASSWORD,to the gmail account from which you wish to send the reset password mails
  
- Run the following the start the server    
`python manage.py runserver`


## Deployment
The app has been deployed to heroku at : https://share-connect.herokuapp.com/users/
