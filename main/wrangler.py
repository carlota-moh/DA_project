def check_crawler(input_path, output_path, logger):
    from utils import read_json, read_csv
    
    input_data = read_csv(input_path, logger)
    output_data = read_json(output_path, logger)[0]

    if len(input_data) == len(output_data):
        logger.info("Crawler extracted information from all universities")
    
    else:
        logger.warning("Some universities' information is missing")

def check_keys(output_path, logger):
    from utils import read_json
    crawler_data = read_json(output_path, logger=logger)[0]
    unique_keys = set()
    for dic in crawler_data:
        keys = list(dic.keys())
        for key in keys:
            unique_keys.add(key)
    return unique_keys

def wrangler(input_path, output_path, logger):
    check_crawler(input_path=input_path, output_path=output_path, logger=logger)
    keys = check_keys(output_path=output_path, logger=logger)
    return list(keys)

def run_wrangler(input_path, output_path, keys_path):
    import logging
    from utils import write_json

    # Initialize logger
    logger = logging.getLogger("wrangler")
    logger.setLevel(logging.DEBUG)
    # Create a file handler to log the messages.
    log_file = "./logs/wrangler.log"
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

    keys = wrangler(input_path=input_path, output_path=output_path, logger=logger)
    write_json(keys, keys_path, logger)       
    logging.info("Successfully written data to file")
