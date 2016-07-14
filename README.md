
# The Evolution of Mobiles
----------------

A data visualization experiment to analyze and explore the evolution of mobile phones through the years. I made this project to practice different parts of data science like - 

### Data Extraction
All the data for this project is extracted from [gsmarena.com](https://gsmarena.com) using a recursive async scraper, made using [Gevent](http://www.gevent.org/) and [lxml.html](http://lxml.de/lxmlhtml.html). The code for the crawler can be found in scraper.py. 

### Data Cleaning
Data is cleaned by using regex. All the cases(with regexr.com links) currently done are in the list below - 

- [Screen Size](http://regexr.com/3dmb5)
- [Dimensions](http://regexr.com/3dmbq)
- [Weight](http://regexr.com/3dmfu)
- [Resolution](http://regexr.com/3dmlc)
- [Battery](http://regexr.com/3dmor)
- [Year](http://regexr.com/3dmjp)
- [Month](http://regexr.com/3dmk8)

The code for the cleaner can be found in cleaner.py . 

### Data Wrangling (wip)
Data wrangling is done on the flask server(app.py) when the data is transfered between cleaner and D3

### Data Visualization (wip)
TBD using D3

