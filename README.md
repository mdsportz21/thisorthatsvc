**TODO**  
1. ~~Display rankings on right-half of the screen!~~  
a. Extra credit: On mobile, it should show rankings below  
b. ~~Extra credit: show in table names and small thumbnails~~
1. ~~Create ranking object with the following attributes:~~  
a. ~~my subject number rank~~  
b. ~~list of subjects I beat,~~  
c. each subject is a link that pulls up the two hats for a comparison or navigate to that hat in the rankings  
d. ~~win-loss record~~  
1. ~~Show percentage completed  
a. len(comparisons) / sum(i for i in range(1,len(subjects)))~~  
1. ~~Write scraper for hatz.squarespace.com~~  
1. ~~Insert scraper data~~  
1. Export to csv on demand  
a. Create util for copying and appending to CSV  
b. Write subjects to csv using Squarespace product csv template  
c. Verify that CSV can be uploaded to Squarespace Commerce
1. Create milb importer  
a. Deprecate squarespace importer  
b. Create csv? form for importing new hats (page link, hat url?)  
c. Bonus: create wikipedia scraper to get (city, state, origin year, etc)  
1. Create a way to choose which hat to compare to the others  
a. Maybe change alg to compare one hat a time and be done with it  
1. Figure out how to get python server to start and stop mongod


**Setup**  
_$ virtualenv flask_  
_$ flask/bin/pip install flask_  
_$ flask/bin/pip install flask-restful_  
_$ flask/bin/pip install flask_cors_  
_$ flask/bin/pip install Flask-PyMongo_  
_$ flask/bin/pip install pytest-mock_  
_$ flask/bin/pip install -U pytest_  

**Run**  
_$ ./app.py_  

**Unit Test**  
_$ flask/bin/python -m pytest test/_  

**Test**  
_$ mongo thisorthat_  
_$ db.subjects.find()_  

_$ curl http://localhost:5000/api/subjects | json_pp_

_$ curl http://localhost:5000/api/ranking | json_pp_  

_$ curl http://localhost:5000/api/scrape -X POST_  

_$ curl -H "Content-Type: application/json" -X POST -d '{  
  "subjects": [
    {
      "description": "C-Town River Dogs",
      "id": 1,
      "imgDesc": "Charleston River Dogs",
      "imgLink": "https://static1.squarespace.com/static/594061048419c282ed731d4a/5949b25b86e6c05c7d5cf26d/5949b27f6b8f5bfb66cee7e1/1498002048239/thumb+%2814%29.jpeg?format=1500w",
      "selected": true
    },  
    {
      "description": "Augusta Greenjackets",
      "id": 2,
      "imgDesc": "Augusta Greenjackets",
      "imgLink": "https://static1.squarespace.com/static/594061048419c282ed731d4a/59420b38893fc0f697291aa6/59420c2cb3db2bab436210dc/1497500717718/thumb.jpeg?format=1500w",
      "selected": false
    }
  ]
}' http://localhost:5000/api/subjects_  
  
  
**Sources**
1. https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
2. https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
3. https://flask-cors.readthedocs.io/en/latest/
4. https://flask-pymongo.readthedocs.io/en/latest/
