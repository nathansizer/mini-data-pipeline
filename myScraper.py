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

def scrape_fbref():
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

def main():
    """
    The main function combines the scraper functions, and saves to the raw file directory
    """

    #scrape from Transfermarkt
    tm_df = scrape_transfermarkt()

    """
    #scrape from FBRef
    fbr_json = scrape_fbref()

    Note here: As FBRef keeps returning HTML 500 codes (as explained in README file in the repo),
    I'm commenting this function out as I'm placing the data there manually. The logic is the exact same,
    it's just a little "bodge" to make everything work as intended. As such, the saving of this file
    will also be commented out below.
    """

    #save the data to the raw subdirectory
    tm_df.to_csv("./raw/tm_raw_teamdata.csv")

    """
    commenting, as mentioned above

    with open("./raw/fbr_raw_teamdata.json", "w") as f:
        json.dump(fbref_json, "./raw/fbr_raw_teamdata.json")
    """    

if __name__ == "__main__":
    main()
