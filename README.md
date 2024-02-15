# README
## _Wikipedia-scraper_

### Description
In this small project, we create a wikipedia scraper for the express purpose of scraping the first paragraph found on each wiki page from all the leaders of a country in history

### Installation & Requirements
Download or pull this code from the repository.

This is best run in a virtual python 3.12 environment

If virtualenv is not yet installed, install it using:
~~~
pip install virtualenv
~~~
Start a new envrionment:
~~~
python -m venv <virtual-environment-name>
~~~
Install required packages:
~~~
pip install -r requirements.txt
~~~


### Usage
The program is run by using following code
~~~
python3 main.py 
~~~

This program will lookup the country code from following API: https://country-leaders.onrender.com/

Based on these country codes, it will lookup the country leaders dictionaries. 
Then it will take the wiki-url and take the first paragraph, and add this to these libraries.
This is then output in a .json file that can be found in the data directory.

### More
This was a project done for the BeCode AI course. Time to complete was 3 days.

