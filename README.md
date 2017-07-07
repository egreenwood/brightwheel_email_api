### How to install, and run
```
$ git clone git@github.com:egreenwood/brighwheel_email_api.git
$ cd brightwheel_email_api
$ pip install virtualenvwrapper
$ mkvirtualenv email_api
$ pip install -r requirements.txt
```

put Api keys for the mailservers into a .env file in the email_api/ directory, with the format:
```
MAILGUN_API_KEY=exampleApiKey
SENDGRID_API_KEY=exampleApiKey
```

migrate the db, run the server
```
$ python manage.py migrate
$ python manage.py runserver
```
the app should be running at localhost:8000
POST requests can be made to localhost:8000/email

### Mail Server Config
configure which mail server is used with the MAIL_SERVER param in email_api/setting.py

### Running tests
```
$ python manage.py test
```

### Language, framework, and libraries you chose, and why.
- *virtualenv*: dev environment setup - virtualenv isolates python version and packages from the system, to help minimize requirement/config conflicts when running in different environments
- *django, django rest framework*: Django is the web framework I am most familiar/comfortable with, it provides quick web app setup
and DRF viewsets and serializers provide a convenient way to expose a create endpoint and built-in validators for requests, email fields etc.
- *sqlite3*: minimal db setup to get a working app
- *beautifulsoup*: a python package that provides convenient html parsing

### Tradeoffs, considerations, next steps, in no particular order
- 'from' is a reserved word in python, it's probably not great to design code around language specific restrictions,
but in the case of an internal api where we control input params, using a non-reserved word, eg. 'sender', would simplify the code a bit.

- 'from' in the payload is mapped to 'from' in the db for users who wouldn't look at the code, but might need to validate that requests are successfully being handled, eg. QA
This is potentially confusing in understanding the code, and might be worth omitting if there are few people in the above roles

- beautifulsoup provides a really convenient way to parse the html in the incoming request, and maintains some paragraph structure in the form of newlines when printing.
This could be extended/customized so that mail server requests send similarly styled content.

- Adding data to the db to track responses from the mail server would be good for monitoring successful mail server requests and staging retries when necessary

- Passing mail server requests to worker, eg. Celery, would free up the application to process incoming requests

- Handle for multiple recipients

- Moving the api keys to environmental variables or putting them in the database would be a good idea.
Assuming that the source code is maintained in version control, and managed somewhere like Github, there's a risk of publicly exposing keys
Moving them out of the source code decreases that risk.
