# Correios Web Crawler
Hi there. This is a web scraper made to retrieve the zip-code of cities from a specific brazilian state. With this application, you get all zip-codes in a matter of seconds.
CorreiosWebCrawler was made using [Scrapy](https://scrapy.org/), an open source and collaborative framework for extracting the data you need from websites. Also, I used [Selenium](https://www.selenium.dev/) for automating some interactions with the browser.

## Getting started
I created this applcation using Ubuntu 18.04 and the following steps are made for it. Check if the items below have specific types of installation for your OS. Also, in order to run it locally, you must have an internet connection. 
Follow the steps below and try it out. 

### Prerequisites

- [Python](https://www.python.org/downloads/) >= 3.6.9
- [Pip](https://pip.pypa.io/en/stable/) (python package manager)
- [Selenium](https://selenium-python.readthedocs.io/installation.html) webdriver downloaded and added to PATH (I used the Mozilla Firefox webdriver in my machine)

### Installation

Clone the repository:
```
git clone https://github.com/Barenco/correios-crawler.git
```

Create a virtual environment:
```
sudo apt install python3-venv
python3 -m venv correios-venv
source correios-venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

After that, you should be able to run it.

### Running

Now its very simple. All you have to do is pass the state abbreviation (such as SC, MG, etc) and the desired [format](https://docs.scrapy.org/en/latest/topics/feed-exports.html) as parameters to your crawl. An example would be:

```
scrapy crawl zip_code -o zip_code.json -a state=RJ
```

## Author

[David Barenco](https://www.linkedin.com/in/david-barenco-7b84a012a/)
