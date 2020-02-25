import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    if not is_valid(url):  # if not a valid url
        return list()  # return an empty list, as nothing was scraped
    if 606 >= resp.status_code >= 600 or 599 >= resp.status_code >= 400:  # Checking for error response from caching server
        return list()  # return empty list, as nothing was scraped
    if not resp.text:
        return list()


    soup = BeautifulSoup(resp.text, "html.parser")  # parse the raw text
    atag_list = soup.findAll('a') # find all of the url links on the page
    listWithUrl = []  # initialize list to contain the new urls to be added to the frontier

    for atag in atag_list:
        potentialURL = atag.get('href')
        if is_valid(potentialURL):
            if potentialURL.find('#') > 0:
                potentialURL = potentialURL[0:potentialURL.find('#')]
            listWithUrl.append(potentialURL)

    return listWithUrl

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if parsed.netloc not in set(
                ["www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu", "today.uci.edu"]):
            return False
        if parsed.netloc == "today.uci.edu":
            if "/department/information_computer_sciences/" not in parsed.path:
                return False
            if "/department/information_computer_sciences/calendar" in parsed.path:
                return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise
