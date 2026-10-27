# Looking at various variables related to the Covid pandemic

**Goal**: How Covid pandemic developed in wealthy countries?

Wealthy countries are considered those with highest GDP. However, since GDP is highly dependent on the population of a country, after obtain the list of top 20 countries, they are reordered using their GDP per capita. I believe this would be a more reliable way of comparison.

Then, we take a look at general trends in number of cases, deaths, and how variables such as the introduction of vaccines affected these numbers.

## Packages
Pandas, Requests (for scraping wikipedia), Numpy, Matplotlib, Sqlalchemy.

## Data sources
1. [Wikipedia's list of countries GDP](https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal))
   
2. [Wikipedia's list of countries GDP per capita](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population)

3. [Wikipedia's list of populations](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population)
  
4. [Worldindata's Covid-19 data](https://ourworldindata.org/covid-deaths)


## Notebooks
*Creating the DB:* [Jupyter notebook](./creating_db.ipynb)

First, using a simple script (requests, pandas), I scraped the list of top 20 countries in GDP rankings (oredered based on their GDP-per-capita), along with their respective populations. Then, I trim down the Covid data to include only these countries. Finally, using Sqlalchemy, I populated the tables in the DB with the data.

*Analysis:* [Jupyter notebook](./Analysis.ipynb)

All the analysis is done up to 5th of May 2023, when WHO declared the end of world wide pandemic.

