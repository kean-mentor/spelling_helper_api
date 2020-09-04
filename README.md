Deployment:
-----------
Get the source: git clone https://github.com/kean-mentor/spelling_helper_api.git  
Install requirements: pip/pip3 install -r requirements.txt


Starting API:
-------------
`export FLASK_DEBUG=True/False` (This step is optional)

using the flask development server:  
`export FLASK_APP=spelling_api`  
`flask run` (use -p to set port)

or using gunicorn:  
`gunicorn -b HOST:PORT spelling_api:app`


Starting WEB:
-------------
`export SPELLING_API_HOST=HOST` (This step is optional, default: localhost)  
`export SPELLING_API_PORT=PORT` (This step is optional, default: 5000)  

using the flask development server:  
`export FLASK_APP=spelling_web`  
`flask run` (use -p to set port something differenct than API's port)

or using gunicorn:  
`gunicorn -b HOST:PORT spelling_web:app`


FYI: You can install gunicorn inside a virtualenv and use from there
https://docs.gunicorn.org/en/stable/deploy.html#using-virtualenv


Sample requests:
----------------
Get the list of words
`curl http://localhost:5000/words -X GET`

Add a new word
`curl -i -H "Content-Type: application/json" http://localhost:5000/words -X POST -d '{"word": "bagoly"}'`

Delete a word
`curl -i http://localhost:5000/words/24 -X DELETE`

Request an exam
`curl "http://localhost:5000/exam?name=andras&total=3" -X GET`

Answer an exam (FYI: You have to provide a previously requested exam's id)  
`curl -i -H "Content-Type: application/json" http://localhost:5000/exam/7 -X PUT -d '{"answers": ["ly", "yes"]}'`
