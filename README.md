# CNUMBBMLProject

## Background

I recently took the Jovian [Data Analysis](https://jovian.com/learn/data-analysis-with-python-zero-to-pandas) and [Machine Learning](https://jovian.com/learn/machine-learning-with-python-zero-to-gbms) courses where I performed analysis and trained ML models from a varierty of open source datasets. And for both projects there were capstone projects, where I planned to use a dataset that I had more intimate knowledge about, my college basketball team's historical statistics. However, in my naivete I was assuming that the **avaiability** and _cleanliness_ of data in the "wild" would be similar to the datasets that I was presented on [Kaggle](https://www.kaggle.com/datasets). I quickly learned that was indeed NOT the case. Even for my universitiy where the stats have been religiously and dilligently taken for over a decade now, getting the data was not nearly as easy of a task as I initially imagined. Which was the spawn of this project.

## Problem Statement

It's an extremely common occurence for people to get into arguments about sports. And that is not limited to the great debaters that we see on Television like SportsCenter and ESPN, everday people constantly are arguing about sports in the same way. Even the PLAYERS of the sports themselves, which was a commonplace subject for my teammates and I. However, depsite the team having extremely detailed statistical analysis tools the licenses were extremely pricey so restricted to use by the coaches only. Which left us with the publically available stats on the athletics websites. However, that led to long drawn out discussions as we had to traverse the plethora of pages containing indivually detailed statistics distributed in an organized chaos not conducive to comparison or analysis.

Giving my background in computer science, I was able to write a few scripts to collect, aggregate, and do some basic aggregation on the data by scraping the website. And once I completed the forementioned data analysis courses I was armed with enough skills to wipe the floor with my teammates using the analysis that I could perform. However, the best arguments are had when all parties have equal access to the information. So I thought that it would be great to have a tool that everyone could use to analyze the team's data.

## Current Solution

I decided to combine my tools that I was using into a one tool that could be generally available to all players, coaches, and fans of the Captains Basketball Program. This tool will be dashboard that serves as the home for the individual tools that I was using that comprises of:

- Front End: Steamlit App
- Back End: Azure Storage
- "Data Pipeline": Stats Web Scraper

And in my professional work we have been using [Docker](https://www.docker.com/) which I was only vaguely familiar with I thought that I would Dockerize these components to deploy later using [Azure Container Apps](https://azure.microsoft.com/en-us/products/container-apps/) to get more familiar with the entire process.

### Front End: Streamlit App

I think the best way to make the application accessible for everyone is to give the tool an easy to use user interface. And given that I have been a frontend developer and there are easy to use frameworks like React that I could use and would help me learn the framework better I chose a different route. I love python and wanted to stick within the language, and while I could've used django and flask I also didn't want to worry about the actual design. I wanted to focus strictly on the data, amd Streamlit is a tool/framework that is designed to be used by data analyst/scientist so they can focus on the data. Additionally since it's aimed at data analyst/scientist it's also designed to be used in the language that most analyst/scientist use, python.

So far I've loved it from the developer standpoint because it was easily intergrated into the data analysis that I was using in jupyter notebooks and I do little to no design work and the app looks great. There are definitely some tradeoffs but for the small applicaiton that this is, it works great for my use case currently.

### Back End: Azure Storage

Currently, I am saving the data to local storage as a CSV. With Docker, I have been using a Docker volume to save these CSVs that the containers would use. In "production" I would want to be ablke to save and persist the data the same way. So I can create a Azure Storage ACcount to save the CSV files and mount the storage account to a Docker volume that can be used by all of the containers for persistant data storage.

### "Data Pipeline": Web Scraper

Finally, I have my web scraper. I will have it in it's own Docker container that will run a cron job that will scrape the data at 12 AM on Tuesday Mornings during the basketball season to collect stats weekly and limit the amount of requests made to the team. I am hoping to also have the scraper use Pandas to clean and transform the data before saving the data to CSV in the Azure Storage account. Hesitant to call it a pipeline as I'm not sure if it qualifies as a traditional data pipeline.

## Future Work/Improvement Ideas

I have some other ideas that I wanted to implement as well and may become part of the project as time goes on.
Here are some of the ideas that I have:

- Machine Learning Ideas:
  - Predicts Win Probability/Winner of Game
  - Predicts Over/Under of Stats for Players
  - Predicts Stat Lines for Players
  - Predicts Final Score of Game
- Expand to All Teams in Conference (currently uses data from CNU's Website for only CNU Games)
- CI/CD Pipeline for Updates
