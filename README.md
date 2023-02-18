# CNUMBBMLProject

## Background

I recently took the Jovian [Data Analysis](https://jovian.com/learn/data-analysis-with-python-zero-to-pandas) and [Machine Learning](https://jovian.com/learn/machine-learning-with-python-zero-to-gbms) courses where I performed analysis and trained ML models from a varierty of open source datasets. And for both projects there were capstone projects, where I planned to use a dataset that I had more intimate knowledge about, my college basketball team's historical statistics. However, in my naivete I was assuming that the **avaiability** and _cleanliness_ of data in the "wild" would be similar to the datasets that I was presented on [Kaggle](https://www.kaggle.com/datasets). I quickly learned that was indeed NOT the case. Even for my universitiy where the stats have been religiously and dilligently taken for over a decade now, getting the data was not nearly as easy of a task as I initially imagined. Which was the spawn of this project.

## Problem Statement

It's an extremely common occurence for people to get into arguments about sports. And that is not limited to the great debaters that we see on Television like SportsCenter and ESPN, everday people constantly are arguing about sports in the same way. Even the PLAYERS of the sports themselves, which was a commonplace subject for my teammates and I. However, depsite the team having extremely detailed statistical analysis tools the licenses were extremely pricey so restricted to use by the coaches only. Which left us with the publically available stats on the athletics websites. However, that led to long drawn out discussions as we had to traverse the plethora of pages containing indivually detailed statistics distributed in an organized chaos not conducive to comparison or analysis.

Giving my background in computer science, I was able to write a few scripts to collect, aggregate, and do some basic aggregation on the data by scraping the website. And once I completed the forementioned data analysis courses I was armed with enough skills to wipe the floor with my teammates using the analysis that I could perform. However, the best arguments are had when all parties have equal access to the information. So I thought that it would be great to have a tool that everyone could use to analyze the team's data.

## Current Solution

I decided to combine my tools that I was using into a one tool that could be generally available to all players, coaches, and fans of the Captains Basketball Program. This tool will be dashboard that serves as the home for the individual tools that I was using that comprises of:

- Front End: Steamlit App
- Back End: PostgreSQL DB
- API: Fast API
- "Data Pipeline": Stats Web Scraper

And in my professional work we have been using [Docker](https://www.docker.com/) which I was only vaguely familiar with I thought that I would Dockerize these components to deploy later using [Azure Container Apps](https://azure.microsoft.com/en-us/products/container-apps/) to get more familiar with the entire process.

### Front End: Streamlit App

I think the best way to make the application accessible for everyone is to give the tool an easy to use user interface. And given that I have been a frontend developer and there are easy to use frameworks like React that I could use and would help me learn the framework better I chose a different route. I love python and wanted to stick within the language, and while I could've used django and flask I also didn't want to worry about the actual design. I wanted to focus strictly on the data, amd Streamlit is a tool/framework that is designed to be used by data analyst/scientist so they can focus on the data. Additionally since it's aimed at data analyst/scientist it's also designed to be used in the language that most analyst/scientist use, python.

So far I've loved it from the developer standpoint because it was easily intergrated into the data analysis that I was using in jupyter notebooks and I do little to no design work and the app looks great. There are definitely some tradeoffs but for the small applicaiton that this is, it works great for my use case currently.

### Back End: PostgresSQL

I decided to use a PostgreSQL database because initially the way I setup the streamlit app to work was every time that it was initialized that it scraped the university's athletics page for the stats and saved them locally. And while that would've been fine for me, I assume that if the website got some decent traffic that the university wouldn't like all the request that I would be making to the page. So instead I will scrape the data periodically and save it to the database, that way if there's traffic I will bombard my own resources and not theirs.

### API: FastAPI and SQLModel

TRo communicate with the database mentioned above I decided to create an API, that way my front end can interface with the data but also to solve another problem. What would've made my initial capstone projects much easier to complete would have been if I had an easier way to access the data. So I plan to make the API generally available so other can use it for whatever purpose they may have for the data as well and it will arrive in a clean and structured manner.

### "Data Pipeline": Web Scraper

Finally, I have my web scraper. I will have it in it's own Docker container that will run a cron job that will scrape the data at 12 AM on Tuesday Mornings during the basketball season to collect stats weekly and limit the amount of requests made to the team. I am hoping to also have the scraper use Pandas to clean and transform the data before sending the data to the database using the API that I have created. Hesitant to call it a pipeline as I'm not sure if it qualifies as a traditional data pipeline.

## Future Work/Improvement Ideas

I have some other ideas that I wanted to implement as well and may become part of the project as time goes on.
Here are some of the ideas that I have:

- Machine Learning Ideas:
  - Predicts Win Probability/Winner of Game
  - Predicts Over/Under of Stats for Players
  - Predicts Stat Lines for Players
  - Predicts Final Score of Game
- API Authentication
- Expand to All Teams in Conference (currently uses data from CNU's Website for only CNU Games)
- CI/CD Pipeline for Updates
