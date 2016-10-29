#/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script takes a URL, http://data-interview.enigmalabs.org,
scrapes the links from each page, scrapes the data from each link,
and outputs the data in JSON format to the solution.json file.
get_pages is called at the bottom with Edgar url and 10 as arguments.
"""

import json
import urllib2
from bs4 import BeautifulSoup


COMPANIES = []


def get_pages(url, pages):
    """Build url for each page of Edgar and ouput scraped data in JSON."""
    for i in range(1, pages+1):
        page_url = url
        page_url += "?page=" + repr(i)
        get_links(page_url)

    with open('solution.json', 'a') as json_file:
        # JSON encode company data and add to solution.json
        json.dump(COMPANIES, json_file)


def get_links(url):
    """Open each page of Edgar and parse the html for company links."""
    try:
        open_page = urllib2.urlopen(url)
    except HTTPError as err:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', err.code
    except URLError as err:
        print 'We failed to reach a server.'
        print 'Reason: ', err.reason
    else:
        soup = BeautifulSoup(open_page, "lxml")

        # grab each company link from current page
        for link in soup.find('table').find_all('a'):
            href = link.get('href')
            get_html(href)

        open_page.close()


def get_html(link):
    """Add links' relative path to base url and get html for that page."""
    link_url = BASE_URL + urllib2.quote(link)
    open_link = urllib2.urlopen(link_url)
    soup = BeautifulSoup(open_link, "lxml")
    add_company(soup)
    open_link.close()


def add_company(soup):
    """Build object with company data and add to global list of companies."""
    company = {}
    comp_attr = ("name", "street_address", "street_address_2", 
                 "city", "state", "zipcode", "phone_number", "website", "description")
    for attr in comp_attr:
        company[attr] = soup.find(id=attr).get_text()

    COMPANIES.append(company)


BASE_URL = "http://data-interview.enigmalabs.org"
# Scrape first 10 pages of Edgar.
get_pages(BASE_URL, 10)
