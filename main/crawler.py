def remove_unicode(str):
        """
        Get rid off unicode characters in string

        INPUTS:
        -str: string
            string to process
        
        RETURNS:
        -clean_str: string
            string without unicode characters
        """
        clean_str = str.encode('ascii', 'ignore').decode()
        return clean_str

def text_getter(target):
    return [remove_unicode(element.get_text()) for element in target]

def crawler(url, json_data, university_name, logger):
    from spider import get_soup, find_elements

    # Load HTML into soup object
    soup = get_soup(url, logger)

    # Locate target table in which information is located
    target_tables = find_elements(soup, logger, element_name="table", class_= "infobox vcard")

    if len(target_tables) > 1:
        logger.error("More than one table! Selecting first one")
    
    target_table = target_tables[0]
    
    # Create empty dictionary to store data
    data = {}
    data['university'] = university_name
    images = find_elements(target_table, logger, element_name="a", class_="image")
    data['seal'] = images[0]['href'] 

    try:
        data['logo'] = images[1]['href']
    except Exception as e:
        logger.warning("No logo found for %s" % university_name)
    
    try:
        data['motto_latin'] = target_table.find('i', lang='la').get_text()
    except Exception as e:
        logger.warning("No latin motto found for %s"  % university_name)

    k = find_elements(target_table, logger, element_name="th",\
                      scope="row", class_= "infobox-label")
                      
    t = find_elements(target_table, logger, element_name="td", class_ = "infobox-data")
    
    keys = text_getter(k)
    data_vals = text_getter(t)

    for key, val in zip(keys, data_vals):
        data[key] = val

    json_data.append(data)
    logger.info("Successfully retrieved data for %s" % university_name)

def run_crawler(csv_path, json_path):
    import csv
    import logging
    from utils import write_json

    # Initialize logger
    logger = logging.getLogger("crawler")
    logger.setLevel(logging.DEBUG)
    # Create a file handler to log the messages.
    log_file = "./logs/crawler.log"
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

    json_data = []
        
    with open(csv_path, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            university_name = row[0]
            url = 'https://en.wikipedia.org'+row[1]
            try:
                logger.info("Getting content from %s" % university_name)
                crawler(url=url, json_data=json_data, university_name=university_name, logger=logger)
            except Exception as e:
                logger.warning("Oh no! No infobox card found!")
                continue

    write_json(json_data, json_path, logger)       
    logging.info("Successfully written data to file")
        