# GitHub user visualization

This app is formed by two parts:
1. Python script that extracts users information from the [GitHub API][1] and inserts it to an SQLite database table
2. Flask app that displays the data saved in the database

## Script

### How to execute

Move to the folder: `app/code/`.

The script can receive none or 1 argument as follows:
```
python seed.py arg1
```
or
```
python seed.py
```
Where `arg1` is the number of users to be extracted from the API. If no argument is passed, the first 150 users will be extracted. Maximum of 600 for unauthenticated users. No authentication is implemented here.

### Database 

Name:
- github

Table name:
- users

### Test Database 

Name:
- test_github

Table name:
- users

Columns:
- USERNAME
- ID (PRIMARY KEY)
- IMAGE_URL
- TYPE 
- URL   

## Web App

The web app is located at the following location deployed on Heroku:

[Github App][2]

And it displays the users from the database at a maximum of 25 records per page inside a table with the id, username, type and thumbnail information. The username opens a new browser window with the user's GitHub profile.

## API

The API has defined the following endpoints:

1. `GET` /api/profiles

    Returns all the existing users in the database

2. `GET` /api/profiles?user=***username***

    Returns data from a specific user

## Backend

- Data is extracted in a specific format from the GitHub API that needs to be converted to the data structure required by the database methods
- GitHub allows a maximum of 100 records per page on request, so a logic had to be implemented to display the requested 150 instead of 100
- A GithubDatabase class was implemented to connect, create tables and insert and retrieve data

## Caching

Both, the web app and the API have cache implementation through Flask-Caching with a caching timeout of 24 hours, as data is not considered to change frecuently.



[1]: https://docs.github.com/en/free-pro-team@latest/rest/reference
[2]: https://github-user-extraction.herokuapp.com/