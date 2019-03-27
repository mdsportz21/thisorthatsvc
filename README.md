# Run

```
$ source ./bin/activate
$ python runserver.py
```

# Deploy to Server

```
$ cd thisorthatsvc  
$ git push heroku master  
$ heroku logs --tail
```  

# Setup

## Python

### Install - Approach One

```
$ virtualenv flask  
$ flask/bin/pip install flask  
$ flask/bin/pip install flask-restful  
$ flask/bin/pip install flask_cors  
$ flask/bin/pip install Flask-PyMongo  
$ flask/bin/pip install pytest-mock  
$ flask/bin/pip install -U pytest  
```

### Install - Approach Two

```
$pip install -r requirements.txt
```

## Mongo

### Populate Teams

```
teams = scraper.get_teams_from_files()
# then, write teams to db
```   


# Test

## Unit Test

```
$ flask/bin/python -m pytest test/
```


## Mongo

```
$ mongo thisorthat
$ db.subjects.find()
```

## curl

```
$ curl http://localhost:5000/api/bracket | json_pp
$ curl http://localhost:5000/api/subjects | json_pp
$ curl http://localhost:5000/api/ranking | json_pp
$ curl http://localhost:5000/api/scrape -X POST
$ curl http://localhost:5000/api/import -X POST
```

## Get a list of brackets

```
$ curl http://localhost:5000/api/bracket | json_pp
```

## Create Bracket

```
$ curl -H "Content-Type: application/json" -X POST -d '{"seedingStrategy": "random", "bracketSize":8}' http://localhost:5000/api/bracket/5b552322d6f45f189b117fbf/demo  
$ curl -H "Content-Type: application/json" -X POST -d '{"name": "15"}' http://localhost:5000/api/bracket  
$ curl -H "Content-Type: application/json" -X POST -d '{"user": "tim", "seedingStrategy": "random", "bracketFieldId":"5b552322d6f45f189b117fbf"}' http://localhost:5000/api/bracket > bracket.json  
```

## Get Bracket

```
$ curl http://localhost:5000/api/bracket/15 | json_pp > bracket_20180317.json
```

# Links

## Sources

1. https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
2. https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
3. https://flask-cors.readthedocs.io/en/latest/
4. https://flask-pymongo.readthedocs.io/en/latest/
5. https://www.codexpedia.com/devops/mongodb-authentication-setting/
6. https://devcenter.heroku.com/articles/config-vars
7. http://api.mongodb.com/python/current/examples/authentication.html - authenticating mlab queries
8. https://github.com/auth0/auth0-python - auth0 python (might need to use this)
9. https://auth0.com/docs/api-auth/tutorials/verify-access-token - verify token on backend
10. https://auth0.com/blog/navigating-rs256-and-jwks/ - verify token example
11. https://auth0.com/learn/json-web-tokens/ - front end token format

## Troubleshooting

1. https://stackoverflow.com/questions/11150343/slow-requests-on-local-flask-server