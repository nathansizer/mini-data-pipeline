import pandas as pd
import json
import boto3
import os
from io import StringIO

def clean_fbref(json_data):
    """
    This function takes raw FBRef json data, then transforms the json data to a dataframe
    This returns a dataframs for a 'stat group' (i.e. attacking stats)
    """
    return(pd.json_normalize(json_data))

def clean_tm(tm_df):
    """
    This function takes raw transfermarkt data, and transforms it into a more usable dataframe
    As part of this cleaning, I'll be removing all players which aren't needed in the report,
    in other words, all non-Blackburn players will be removed
    This returns a dataframe of all the transfermarkt data passed in, after cleaning changes have been made
    """
    #drop all columns considered unnecessary
    tm_df = tm_df.drop("Unnamed: 0", axis=1)
    tm_df = tm_df.drop("Value last updated", axis=1)
    tm_df = tm_df.drop("Citizenship", axis=1)
    tm_df = tm_df.drop("Last club", axis=1)
    tm_df = tm_df.drop("Contract expiration", axis=1)
    tm_df = tm_df.drop("Market value history", axis=1)
    tm_df = tm_df.drop("Transfer history", axis=1)
    tm_df = tm_df.drop("Since", axis=1)
    tm_df = tm_df.drop("ID", axis=1)
    tm_df = tm_df.drop("Joined", axis=1)
    tm_df = tm_df.drop("Other positions", axis=1)

    #remove all non-Blackburn players
    tm_df = tm_df.drop(tm_df.index[tm_df["Team"] != "Blackburn"])

    #drop all players with missing data
    tm_df = tm_df.dropna()

    #convert transfer values to numeric (e.g. £100k --> 100000 and £1.40m --> 1400000)
    tm_df["Value"] = tm_df["Value"].str.replace("€", "", regex=False)
    tm_df["Value"] = tm_df["Value"].str.replace("k", "000", regex=False)
    tm_df["Value"] = tm_df["Value"].str.replace(".", "", regex=False).str.replace("m", "0000", regex=False)

    return tm_df

def upload_cleaned_data(client, bucket):
    """
    This function takes everything in the folder containing cleaned data and uploads it to the S3 bucket
    """

    #loop through each file and send to the S3 bucket
    for file in os.listdir("./data/"):
        upload_key = "data/" +str(file)
        client.upload_file("./"+upload_key, bucket, upload_key)
    

def main():
    """
    The main function of the script: Reads data from the S3 bucket, cleans the data
    and returns the usable data to the corresponding folder in the S3 bucket.
    """

    #first, get my aws access keys
    #as I don't want them to be publically available in the git repo, they'll be read from a hidden file
    aws_file = open("aws_key.txt")
    secret_file = open("aws_secret.txt")
    aws_key = aws_file.read()
    secret_key = secret_file.read()

    #create a boto3 client
    client = boto3.client(
        "s3",
        aws_access_key_id = aws_key,
        aws_secret_access_key = secret_key)

    #specify the s3 bucket
    bucket = "nathans-pipeline-bucket"

    #FBRef data
    #get the s3 response object for our raw FBRef data
    obj = client.get_object(Bucket=bucket, Key="raw/fbr_raw_teamdata.json")

    #extract the json data
    fbr_json = json.loads(obj["Body"].read())

    #Transfermarkt data
    #get s3 response object
    obj = client.get_object(Bucket=bucket, Key="raw/tm_raw_teamdata.csv")
    tm_body = obj["Body"].read().decode("utf-8")
    tm_df = pd.read_csv(StringIO(tm_body))

    #from here, I want to separate the FBRef json file into each "stat group" and transform each into its own dataframe
    #note: I'm not taking every group, just ones I'm going to use in my report, purely for the sake of time
    fbr_stat_groups = ["stats","keepers","shooting","passing","defense","possession","playingtime","misc"]

    #iterate through the list and transform the json into a csv file
    for grp in fbr_stat_groups:
        grp_json = fbr_json["data"][0]["stats"][grp]
        cleaned_data = clean_fbref(grp_json)
        cleaned_data.to_csv("./data/"+grp+".csv")

    #clean transfermarkt data
    tm_df = clean_tm(tm_df)

    #store transfermarkt data
    tm_df.to_csv("./data/tm.csv")

    #now we want to upload all our clean data to the correct area of the S3 bucket
    upload_cleaned_data(client, bucket)

if __name__ == "__main__":
    main()
