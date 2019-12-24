ssh -T git@github.com
heroku login
heroku git:remote -a lecturesbot-micro-service-main
git push heroku master
heroku open
