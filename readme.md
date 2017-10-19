# Newgen File Storage

### Available REST APIs as per the spec:
	
    Upload files - /store [POST]
	Show a list of files - /store [GET]
	Download files - /store/<filename> [GET]
	Delete files - /store/<filename> [DELETE]
	Change storage type - /admin/update-backend [POST]

- Prerequisites:
    - python2.7
    - pip
    - virtualenv and virtualenvwrapper
    - awsebcli

- Setup:
	- clone the repo at https://github.com/ankit-kathuria/newgen-store
	- create/enable virtualenv
 	- install requirements: `pip install -r requirements.txt`
 	- run server: `python api.py`

- Test:
	- import the postman collection from `tests` directory
	- run the entire collection or run individual requests to see the results
	- sample files used during collection setup are included, they may need to be attached manually where required

- Deployment:
	- currently hosted at: http://flask-env.pgkt2cpjq4.ap-southeast-1.elasticbeanstalk.com/store
	- deploy code using awsebcli: `eb deploy`
