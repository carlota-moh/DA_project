if __name__== "__main__":
    import sys
    import logging
    from spider import run_spider
    from crawler import run_crawler
    from wrangler import run_wrangler

    arguments = sys.argv
    country_name = str(arguments[-1]).lower()
    university_path = './data/universities_%s.csv' % country_name

    if "SPIDER" in arguments:
        run_spider(country_name)
        logger = logging.getLogger("spider.spider")
        logger.info("Successfully run spider")

    if "CRAWLER" in arguments:
        json_path = './data/crawler.json'
        run_crawler(csv_path=university_path, json_path=json_path)
        logger = logging.getLogger("crawler.crawler")
        logger.info("Successfully run crawler")
    
    if "WRANGLER" in arguments:
        from utils import search_file
        output_filename = "crawler.json"
        logger = logging.getLogger("wrangler.wrangler")
        output_path = search_file(output_filename, logger)
        keys_path = './data/unique_keys.json'
        run_wrangler(input_path=university_path, output_path=output_path,\
                    keys_path=keys_path)
        logger.info("Successfully run crawler")
    



