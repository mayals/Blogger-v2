

Getting Started
---------------

To run the API locally, follow these steps:

1.  Clone the repository: `git clone https://github.com/yourusername/Blogger.git`
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the virtual environment: `source venv/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Go to .settings.DATABASES section, deactivate #PRODUCTION mode and activate #Development mode, add PostgreSQL configuration to connect to your database to be the default database.
6.  Change `.env.templates` to .env and setup you environment variables. 
7.  Set up the database: `python manage.py migrate`
8.  Create a superuser account: `python manage.py createsuperuser`
9.  Start the development server: `python manage.py runserver`

I have deploy this project to render :

https://bloggerwebservice.onrender.com


