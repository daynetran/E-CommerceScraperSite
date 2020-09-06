# E-CommerceScraperSite

I'm building a web application whose primary purpose is to scrape useful information off of well-known internet marketplaces. My scraper can web-crawl hundreds of links to product sites from Amazon to Home Depot. It then compiles all data (titles, prices, descriptions, ratings, reviews, etc.) into a compact csv file, autojmating away many man-hours of research into competitors' products and markets. It understands to rotate user-agent headings and proxies when faced with obstacles. 

I wrote a Python script that when given a URL, it can scrape the 100 best-selling products on Amazon. However, while this works perfectly on my local computer, I want the scraper to be accessible to anyone on the Internet. What you can't see on this specific repository is the following. I hooked up the web scraper to an AWS EC2 server to run whenever from any computer when said computer gives a curl command. My next step is to set up the front-end for the website that will be presented to client users. 

The main targets for this project are mid-sized and small businesses who sell products online but do not have the resources to better understand the e-commerce landscape and the markets they are competing in.

With this project, I learned how to get information from the web with web crawling and scraping. I learned how to clean the data and format it into a presentable format. I also learned how to work with APIs, packages, and documentation (this scraper was built with the Scrapy and Scrapyd packages). I also learned how to work with remote machines, uploading environments to them, and running code from them. I'm comfortable with learning and eager to continue learning how to improve on my web-app skills.

You can also use my (very young) personal website, https://daynetran.github.io, as another source to review. Thanks!
