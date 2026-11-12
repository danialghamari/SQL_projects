# Analyzing the effects of the pandemic in the top 20 GDP countries (up to Nov. 2026)

*This project is still under development*

## Goal
During and after the COVID-19 pandemic, we often heard vastly different and sometimes contradictory views about its long-term impacts in areas such as education, the economy, and, of course, national health. I was curious to know that in 2026, after almost 4 years, when [WHO declared the end of the pandemic](https://doi.org/10.1016/j.jiph.2025.102698) on 5th of May 2023, what effects are still prevalent. I was particularly interested in understanding:

1. The country's response to the pandemic, e.g., the evolution of the number of new cases and deaths
2. Effects on the national education systems, e.g., the number of children who exhibit educational difficulties
3. Effects on the economy, e.g., GDP trends before and after the pandemic
4. National health, e.g., life expectancy and population growth

To constrain my explorations and analysis, only the data (when available) regarding the top 20 countries in GDP ranking (Wikipedia) are obtained and stored. Meanwhile, since the population size can vastly affect the GDP, I reorder/rank the list according to the GDP per capita in a descending fashion. One major aspect in my analysis to note is the Ukraine-Russia and USA-Iran wars.
## Results
### A country's response to the pandemic
### Economy
### Education
### Health trends

## Data sources

1. Wikipedia: [GDP (2026)](https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)), [GDP per capita (2026)](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population), [Populations (2026)](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population)
  
2. [Worldindata's COVID-19 data](https://ourworldindata.org/covid-deaths): Number of new cases/deaths, Number of administered vaccines, Number of tests

3. [WorldBank](https://data.worldbank.org/)

    1. Economy:
       - GDP
       - Education expenditure
       - Health expenditure
       - Export value index
       - Exports of goods and services (% of GDP)
       - Labor force

    2. Education:
       - Educational attainment
       - Number of students at various levels
       - Share of youth not in education, employment, or training
       - Unemployment with different levels of education (% of labor force)

    4. Health:
       - Death rate
       - Population
       - Life expectancy at birth

## Data model

## Summary of the Analysis
### A country's response to the pandemic
**Questions**:
1. Evolution of new cases and deaths weekly from Jan. 2020 to May 2023
2. Covid variants, infection waves, which country had it worst
3. How fast did countries administer new tests and does it correlate with the registered new cases
4. Can we identify any noticeable effect on the new cases/deaths based on the number of administered vaccinces
5. 

### Economy

### Education

### Health trends

## Packages
Pandas, Requests (for scraping and interacting with REST API), NumPy, Matplotlib, Sqlalchemy.




## Notebooks
*Creating the DB:* [Jupyter notebook](./creating_db.ipynb)

First, using a simple script (requests, pandas), I scraped the list of top 20 countries in GDP rankings (oredered based on their GDP-per-capita), along with their respective populations. Then, I trim down the Covid data to include only these countries. Finally, using Sqlalchemy, I populated the tables in the DB with the data.

*Analysis:* [Jupyter notebook](./Analysis.ipynb)

All the analysis is done up to 5th of May 2023, when WHO declared the end of world wide pandemic.

