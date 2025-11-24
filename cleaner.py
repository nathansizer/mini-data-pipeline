import pandas as pd
import json
import boto3
import os

def clean_fbref():
    """
    This function takes raw FBRef data, then transforms the json data to a dataframe

    This returns a dataframs for a 'stat group' (i.e. attacking stats)
    """

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

    bucket = "nathans-pipeline-bucket"

    obj = client.get_object(Bucket=bucket, Key="raw/fbr_raw_teamdata.json")

    raw_json = json.loads(obj["Body"].read())

    print(raw_json)

if __name__ == "__main__":
    main()
