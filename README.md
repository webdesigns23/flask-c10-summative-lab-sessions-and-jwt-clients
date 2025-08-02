
Installation instructions (i.e. pipenv install, migrating and seeding the database, etc)
Run instructions (i.e. flask run or python app.py)
List with descriptions of all endpoints the API has

Wine Journal Summative Lab
=======

# Description:
A wine journal app for keeping records of your wine cellar.

# Features:
1. Users are able to create an account to personally manage their wine collection.
	- User can Sign up by creating a username, password, and providing an image_url
	- Users are able to Login/Logout
	- Session cookies are used to remember login
2. Once logged in, they are able to view, update, create, or delete their wine bottles logged in their Cellar Records. 
3. Users are able to store the following information about their wines in their Cellar Record:
	- Wine (Name of the Wine)
	- Grape (Name of the Grape)
	- Country (Wine Origin)
	- Vintage (Year wine was harvested, YYYY)
	- Quantity (How many bottles they have in their Cellar, UPDATABLE)
	- Tasting Notes (Wine Flavors UPDATABLE)

# Tools and Resources Featured in this Project:
- [GitHub Repo](https://github.com/webdesigns23/flask-c10-summative-lab-sessions-and-jwt-clients.git)
- Python 3.8.13+
- Text Editor or IDE (e.g., VS Code)
- Git + GitHub
- Virtualenv
- Python Packages listed in requirements.txt
- React
- Node.js

# Set Up and Installation:
1. Fork and clone the GitHub Repo
```bash
git clone <repo_url>

```
2. Set up your virtual environment of choice (virtualenv prefered)
```bash
virtualenv env1
source env1/bin/activate
```
3. Install PyPi dependencies using requiements.txt
```bash
pip install -r requirements.txt
```
4. Navigate into the server/ directory and set environment variables:
```bash
cd server
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
```
5. Create a migrations folder, run initial migration and update
```bash
cd server
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```
6. Populate database with initial data
```bash
python seed.py
```
# Running Back-end of Application:
Should run on port 5555 to match proxy in package.json
You can run the Flask server with:
```bash
python app.py
```

# Running Front-end of Application:
To run the React application
1. Install dependencies
```bash
npm install
```
2. Start the application
```bash
npm start
```

# API Endpoints and Functionality:
## Authorization/ Authentication:
`POST /signup`
* Registers a new user and logs them in by setting the session

`GET /check_session`
* Verifies if a user session is active.

`POST /login`
* Authenticates an existing user and sets the session cookie

`DELETE /logout`
* Ends the session by removing user_id from the session store.

## Cellar Record Index Class:
`GET /cellar_record – paginated`
* Returns all wines
Includes Pagination:
* Uses page and per_page query parameters
* Returns only the requested chunk of data
* Includes metadata like the total number of pages

`POST /cellar_record`
* Adds a New wine to cellar with the following info:
	- Wine (Name of the Wine)
	- Grape (Name of the Grape)
	- Country (Wine Origin)
	- Vintage (Year wine was harvested, YYYY)
	- Quantity (How many bottles they have in their Cellar, UPDATABLE)
	- Tasting Notes (Wine Flavors UPDATABLE)

## Cellar Record Id Class:
`PATCH /cellar_record/<id>`
* Search by id
* Update a quantity or tasting notes of a wine in cellar record

`DELETE /cellar_record/<id>`
* Delete a wine from cellar record

# Testing: 
- Does not contain test files.
- Test in Postman or by using application in browser and inspect

# Commit and Push Git History if any adjustments to this code are made
1. Add your changes to the staging area by executing
2. Create a commit by executing 
3. Push your commits to GitHub by executing 
4. If you created a separate feature branch, remember to open a PR on main and merge.
```bash
git add .
git commit -m "Your commit message"
git push origin main
```