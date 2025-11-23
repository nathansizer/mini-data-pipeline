import requests
import pandas as pd
import ScraperFC as sfc
import json

def scrape_transfermarkt():
    """
    This function uses ScraperFC to scrape Transfermarkt,
    for all championship player data in the 24/25 Championship season.

    This returns a dataframe of raw data. Cleaning will be handled elsewhere
    """

    #create ScraperFC object
    tm = sfc.Transfermarkt()

    #scrape data from Transfermarkt
    tm_players_df = tm.scrape_players("24/25", "EFL Championship")

    return tm_players_df

def scrapr_fbref():
    """
    This function uses the requests package to scrape the FBRef API.

    This returns a json object, ready to be saved into a json file and cleaned later on.
    """

    #get FBRef API key
    #as I don't want it to be publically available in the git repo, it'll be read from a hidden file
    key_file = open("fbr_key.txt")
    fbref_key = key_file.read()

    #url of the FBRef API
    url = "https://fbrapi.com/team-season-stats"

    #set up parameters and headers for the API request
    params = {
        "league_id": "20",
        "season_id": "2024-2025"
    }

    headers = {"X-API-Key": fbref_key}

    #make the API request
    response = requests.get(url, params=params, headers=headers)

    #we can print the API response code, helpful for debugging
    #print(response)

    return (response.json())
