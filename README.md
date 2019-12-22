
heroku addons:create heroku-postgresql:hobby-dev --app appname
heroku config --app appname
heroku run python
--some magic in heroku settings--
git commit -am "message"
git push heroku master
