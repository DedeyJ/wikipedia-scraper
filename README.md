# Wikipedia-scraper README

## Description

Welcome to the Wikipedia-scraper project. This initiative focuses on developing a specialized Wikipedia scraper designed to meticulously extract the initial paragraph from each historical leader's Wikipedia page.

## Installation & Requirements

To get started, obtain the code by either downloading or pulling it from the repository.

For optimal performance, use the virtual environment included in the repository

Activate the virtual environment:

~~~
.venv\Scripts\Activate.ps1
~~~

Install the necessary packages, if not working with the vritual environment:

~~~
pip install -r requirements.txt
~~~

## Usage

Run the program with the following command:

~~~
python3 main.py 
~~~
The program fetches country codes from the [Country Leaders API](https://country-leaders.onrender.com/). Subsequently, it retrieves country leaders' dictionaries based on these codes. The scraper then extracts the Wikipedia URL, captures the first paragraph from each page, and incorporates this information into the libraries. The output is a .json file, conveniently located in the data directory.

## Additional Information

This project was developed as part of the BeCode AI course and was successfully completed within a timeframe of 3 days.