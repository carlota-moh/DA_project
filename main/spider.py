def get_soup(url, logger):
    """
    Function used for loading HTML content into soup

    INPUTS:
    -url: string
        Desired url from whichi to retrieve HTML
    -logger:
        Logger object
    
    RETURNS:
    -soup:
        BeautifulSoup soup object with HTML content
    """
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        logger.warning("Something went wrong... Response code: {}".format(response.status_code))

def find_elements(soup, logger, element_name, **kwargs):
    """
    Function used for finding elements by name within soup

    INPUTS:
    -soup:
        BeautifulSoup soup object with HTML content
    -logger:
        Logger object
    -element_name: string
        Name of the HTML tag by which to search for element
    -**kwargs:
        Other keyword arguments used for finding the element
    
    RETURNS:
    -elements: list
        List of elements in soup matching specified conditions
    """  
    try:
        elements = soup.find_all(element_name, **kwargs)
        if len(elements) == 0:
            logger.warning("No %s found") % element_name
        return elements
    except:
        logger.warning("No %s found") % element_name

def get_attributes(links, logger):
    """
    Function used for retrieving attributes from links

    INPUTS:
    -links: list
        List of HTML links (i.e.: having tagname "a")
    -logger:
        Logger object
    
    RETURNS:
    -urls: list
        urls for each link in links
    -titles: list
        titles for each link in links
    """
    urls = []
    titles = []
    for link in links:
        try:
            urls.append(link['href'])
            titles.append(link['title'])
        except:
            logger.debug("URL and title not found")
            
    return titles, urls

def find_country_url(country_name, country_matrix, logger):
    """
    Functions used for finding the full url to get the list
    of universities for a specific country

    INPUTS:
    -country_name: string
        Name of the desired country. Must be lowercase
    -country_matrix: matrix
        Matrix containing all country names and corresponding
        relative urls
    -logger:
        Logger object
    
    RETURNS:
    -country_url: string
        full url to get list of universities for specified country

    """
    try:
        country = list(filter(lambda x: country_name in x[0].lower(), country_matrix))[0]
        country_url = 'https://en.wikipedia.org'+country[1]
        return country_url
    except IndexError:
        logger.critical("University not listed")

def spider(url, logger, file_path, title_filter):
    from utils import write_csv

    # Get HTLM content parsed into soup
    soup = get_soup(url, logger)

    # Find all universities
    universities = find_elements(soup, logger, element_name="li")

    # Retrieve names and corresponding url for each university
    # and save them to a dictionary
    data = {}
    for university in universities:
        links = university.find_all("a")
        titles, urls = get_attributes(links, logger)

        for title, url in zip(titles, urls):
            try:
                data[title] = url
            except:
                None

    # Create a matrix containing all university names and corresponding links
    country_matrix  = [[k, v] for k, v in data.items() if title_filter in k]
    write_csv(matrix=country_matrix, file_path=file_path, logger=logger)

def spider_university(countries_path, logger, university_path, country_name):
    from utils import read_csv

    # Read csv file
    try:
        country_matrix = read_csv(countries_path, logger=logger)
    except:
        logger.critical("Invalid path")

    # Get url for specified country
    country_url = find_country_url(country_name=country_name, country_matrix=country_matrix, logger=logger)

    # run spider for specificied country
    spider(url=country_url, logger=logger, file_path=university_path, title_filter="University")

def run_spider(country_name):
    import logging

    # Initialize logger
    logger = logging.getLogger("spider")
    logger.setLevel(logging.DEBUG)
    # Create a file handler to log the messages.
    log_file = "./logs/spider.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    # Create a console handler with a higher log level.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    # Modify the handlers log format to your convenience.
    handler_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(handler_format)
    console_handler.setFormatter(handler_format)
    # Finally, add the handlers to the logger.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    countries_url = 'https://en.wikipedia.org/wiki/Lists_of_universities_and_colleges_by_country'
    countries_path = './data/countries.csv'
    university_path = './data/universities_%s.csv' % country_name  

    spider(url=countries_url, logger=logger, file_path=countries_path, title_filter="List of universities in")
    spider_university(countries_path=countries_path, logger=logger, university_path=university_path,\
                      country_name=country_name)