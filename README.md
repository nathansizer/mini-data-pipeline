# mini-data-pipeline
A mini data pipeline to scrape, store and transform football data, then create a one page team/player overview.

## Author:
Nathan Sizer – [LinkedIn](https://www.linkedin.com/in/nathan-sizer)

## Task Outline
- Scrape basic football data from Transfermarkt and FBRef for the 2024/25 Championship season.
- Store raw data in cloud object storage.
- Transform and load it into a data warehouse/table format.
- Create a one page insight summary - player or team overview.

## Deliverables
- A short README to explain architecture, design decisions, setup instructions etc. (This file covers this).
- Python code (In this repo).
- Cloud integration.
- 1 page PDF of insight from the data.
- Notebook or report with workings for insights and visualizations.

## My Process and Decisions
Firstly, I wanted to tackle the FBRef API. Unfortunately I keep receiving HTTP 500 errors (internal server error), so without knowing the ins and outs, I have written code which I believe should work when the server is capable of fulfilling the request. As a workaround to this, I have taken the example team data from the FBR API, which is for Arsenal in the 2018/19 season. I'm aware this isn't specifically what the task brief wanted, however given the apparent limitations the API was facing, having some data for the later steps of the task is better than having none at all. From this point onwards, I'm going to be taking this data and trying to pass it off as "generic team data" so that I can combine it with data scraped from Transfermarkt in order to produce the insight summary for a random team in the Championship in the 2024/25 season. E.g. this insight report will inform us about a team in the Championship after 38 games of the season has been played - it won't be factually accurate data, but I'm mainly concerned about getting my thinking and logic across here. 

_**Aside**: I'm now going to decide on what team the report will be for, as we are using this "generic" data, I'm going to use a random number generator to pick a number between 1 and 24, whatever the result is, I'm going to pick the team that finished in that position in the 2024/25 championship table.\
![The random number generation, it came up as 7](images/rng.png)\
As number 7 was the result, our team for this report will be Blackburn._