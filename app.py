from flask import Flask, request, render_template, redirect, session, flash, jsonify
from models import db, connect_db, User, Favorite
from forms import SignUpForm, LoginForm
from api import SECRET_API_KEY
import requests 
import os

from datetime import date
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql:///video_games_DB")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "keyboardwarrior4")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


# homepage route
app.route('/')
def homepage():
    """Redirect to home page"""
    return redirect('/games')

@app.route('/titles')
def titles_page():
    """Home of the List of video games"""
    # iterates over all the keys in the session, and for each key that is not 'username' removes that key from the session. this effectiviely clears the session while presererving the 'username'
    # useful for clearing out old or unnesessary session data while keeping the user's logged-in status
    [session.pop(key) for key in list(session.keys()) if key != "username"]
    # call and store today's date using the datetime package installed by pip
    todays_date = date.today()
    # using the dateutil package installed with pip take today's date along with 3 months prior to show all the most recent games
    # "(relativedelta(months=-3))" means subtract 9 months from the current date
    nine_months_prior = todays_date + relativedelta(months=-9)
    # prepares the API to make a request to "RAWG" to retrieve all the games added in the last 9 months
    BASE_URL =  f"https://rawg.io/api/games?dates={todays_date},{nine_months_prior}&ordering=-added&page_size=40"

    # send a GET request to the RAWG API to get the data about the games which is then stored in the variable "response"
    response = requests.get(BASE_URL, params={"key": SECRET_API_KEY})

    # Holds parsed JSON data, allowing us to easily access specific parts of the reponse
    json_data = response.json()
    # in many API's the 'results' key will hold the main data. Now data_results will hold that information
    data_results = json_data["results"]
    # contains a URL or identifier for the next page of results. Otherwise it will be "none" if you are on the last page
    next_page = data_results["next"]
    # usually contains a URL or identifier for the previous page
    previous_page = data_results["previous"]
    # these lines of code is designed to handle paginated API responses, making it easy to navigate through multiple pages of results

    # returns the data inside title.html
    return render_template('titles.html', data_results=data_results, next_page=next_page, previous_page=previous_page)


@app.route('/titles/upcoming')
# most comments are re-written to make sure i have an understanding/grasp at my work.
def titles_upcoming_page():
    """Homepage for presenting a list of most anticipated games"""
    # iterates over all the keys in the session, and for each key that is not 'username' removes that key from the session. this effectiviely clears the session while presererving the 'username'
    # useful for clearing out old or unnesessary session data while keeping the user's logged-in status
    [session.pop(key) for key in list(session.keys()) if key != "username"]
    # call and store today's date using the datetime package installed by pip
    todays_date = date.today()
    # using the dateutil package installed with pip take today's date along with 9 months ahead to show all the most upcoming games
    # "(relativedelta(months=+3))" means add 3 from the current date     
    # NOTE: i went back and changed the previous "five_months_prior" to "nine_months_prior" after finishing these next few lines of code. Some of my comments will be outdated.
    nine_months_ahead = todays_date + relativedelta(months=+9)
    # prepares the API to make a request to "RAWG" to retrieve all the games added in the last 3 months
    BASE_URL =  f"https://rawg.io/api/games?dates={todays_date},{nine_months_ahead}&ordering=-added&page_size=40"

    # send a GET request to the RAWG API to get the data about the games which is then stored in the variable "response"
    response = requests.get(BASE_URL, params={"key": SECRET_API_KEY})

    # Holds parsed JSON data, allowing us to easily access specific parts of the reponse
    json_data = response.json()
    # in many API's the 'results' key will hold the main data. Now data_results will hold that information
    data_results = json_data["results"]
    # contains a URL or identifier for the next page of results. Otherwise it will be "none" if you are on the last page
    next_page = data_results["next"]
    # usually contains a URL or identifier for the previous page
    previous_page = data_results["previous"]
    # these lines of code is designed to handle paginated API responses, making it easy to navigate through multiple pages of results\

    # By storing it in the session the application can remember this value across multiple requests making it easier to fetch
    session['next_page'] = next_page
    session['previous_page'] = previous_page
    session['nine_months_ahead'] = nine_months_ahead

    # returns the data inside title.html
    return render_template('titles.html', data_results=data_results, next_page=next_page, previous_page=previous_page, nine_months_ahead=nine_months_ahead)


@app.route('/titles/newest')
def titles_new_page():
    """Homepage for the newest and most recently released games"""
    # iterates over all the keys in the session, and for each key that is not 'username' removes that key from the session. this effectiviely clears the session while presererving the 'username'
    [session.pop(key) for key in list(session.keys()) if key != "username"]
    # call and store today's date using the datetime package installed by pip
    todays_date = date.today()
    # using the dateutil package installed with pip take today's date along with three weeks prior to show all the most upcoming games
    one_month_prior = todays_date + relativedelta(months=-1)
    # prepares the API to make a request to "RAWG" to retrieve the newest games added from the past 3 weeks
    # NOTE: i believe this way my newest page will not be too similar to the regular home page if i were to do 1-3 months of the newest games (alot of new indie games every week it will be information overload)
    BASE_URL =  f"https://rawg.io/api/games?dates={one_month_prior},{todays_date}&ordering=-added&page_size=40"

    # send a GET request to the RAWG API to get the data about the games which is then stored in the variable "response"
    response = requests.get(BASE_URL, params={"key": SECRET_API_KEY})

    # Holds parsed JSON data, allowing us to easily access specific parts of the reponse
    json_data = response.json()
    # in many API's the 'results' key will hold the main data. Now data_results will hold that information
    data_results = json_data["results"]
    # contains a URL or identifier for the next page of results. Otherwise it will be "none" if you are on the last page
    next_page = data_results["next"]
    # usually contains a URL or identifier for the previous page
    previous_page = data_results["previous"]
    # these lines of code is designed to handle paginated API responses, making it easy to navigate through multiple pages of results\

    # By storing it in the session the application can remember this value across multiple requests making it easier to fetch
    session['next_page'] = next_page
    session['previous_page'] = previous_page
    session['one_month_prior'] = one_month_prior

    # returns the data inside title.html
    return render_template('titles.html', data_results=data_results, next_page=next_page, previous_page=previous_page, one_month_prior=one_month_prior)


@app.route('/titles/next_page')
def next_page():
    """Next page for titles"""
    # retrieves URL for next page of game data from the session
    next_page = session.get('next_page')
    one_month_prior = session.get('one_month_prior')
    nine_months_prior = session.get("nine_months_prior")
    # sends a request to the API that fetches the next page
    response = requests.get(next_page, params = {"key": SECRET_API_KEY})
    # removes the next_page entry from the session
    session.pop('next_page')

    json_data = response.json()
    data_results = json_data['results']
    next_page = data_results['next']
    previous_page = data_results['previous']

    session['next_page'] = next_page
    session['previous_page'] = previous_page

    return render_template('titles.html', data_results=data_results, next_page=next_page, previous_page=previous_page, one_month_prior=one_month_prior, nine_months_prior=nine_months_prior)


@app.route('/titles/previous_page')
def previous_page():
    """Previous page"""
    previous_page = session.get('previous_page')
    one_month_prior = session.get['one_month_prior']
    nine_months_prior = session.get['nine_months_prior']
    response = requests.get(previous_page, params = {"key": SECRET_API_KEY})
    session.pop('previous_page')

    json_data = response.json()
    data_results = json_data['results']
    next_page = data_results['next']
    previous_page = data_results['previous']

    session['next_page'] = next_page
    session['previous_page'] = previous_page

    return render_template('titles.html', data_results=data_results, next_page=next_page, previous_page=previous_page, one_month_prior=one_month_prior, nine_months_prior=nine_months_prior)

@app.route('/titles/<int:id>')
def title_info(id):

    """"information about the games"""
    # request data about the game that was selected
    response = requests.get(f"https://api.rawg.io/api/games{id}", params= {"key": SECRET_API_KEY})

    # Saves relative data from api

    response_data = response.json()

    return render_template('gameinfo.html', response_data=response_data)

@app.route('/genre/next_page')
def next_genre_page():
    """Next page when browsing games based on if their genre (shooting, adventure)"""
    next_page = session.get('next_page')
    chosen = session.get('chosen')
    response = requests.get(next_page, params= {"key": SECRET_API_KEY})
    session.pop('next_page')

    # saves relatice data from api
    response_data = response.json()
    response_results = response_data['results']
    next_page = response_data['next']
    previous_page = response_data['previous']

    session['next_page'] = next_page
    session['previous_page'] = previous_page

    return render_template('genre.html', response_results=response_results, next_page=next_page, previous_page=previous_page, chosen=chosen.upper())

# @app.route