def read_json(file_path, logger):
    """
    Function used to read data from JSON in a specified file_path

    INPUTS:
    -file_path: string
        Location of the file
    -logger:
        Logger object

    RETURNS:
    -dic: dictionary
        Python dictionary containing information from JSON
    """
    import json

    try:
        with open(file_path, "r") as f:
            json_data = [json.loads(line) for line in f]
            return json_data
    except FileNotFoundError:
        logger.error("Could not read JSON. Invalid path to file")

def write_json(dic, file_path, logger):
    """
    Function used to write data to JSON in a specified file_path

    INPUTS:
    -dic: dictionary
        Python dictionary to be written to file
    -file_path: string
        final location of the file
    -logger:
        Logger object

    """
    import json

    try:
        with open(file_path, "w") as f:
            json.dump(dic, f)
        logger.info("Successfully written data to file")
    except FileNotFoundError:
        logger.error("Could not write JSON. Invalid path to file")

def write_csv(matrix, file_path, logger):
    """
    Function used to write matrix to csv file

    INPUTS:
    -matrix:
        Matrix to be written to file
    -file_path:
        final location of the file
    """
    import csv
    try:
        with open(file_path, 'w') as f:
            writer = csv.writer(f, delimiter=';')
            for row in matrix:
                writer.writerow(row)
    except:
        logger.error("Could not write CSV. Invalid path to file")

def read_csv(file_path, logger):
    """
    Function used to read csv file and load it into a matrix

    INPUTS:
    -file_path:
        Location of the file
    
    RETURNS:
    -matrix:
        Matrix containing information from csv file
    """
    import csv
    
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            matrix = [row for row in reader]
        return matrix
    except:
        logger.error("Could not read CSV. Invalid path to file")

def search_file(name, logger):
    """
    Function used for searching for specified file within 
    current directory and subdirectories

    INPUTS:
    -name: string
        Name of the file to search for
    -logger:
        Logger object
    
    RETURNS:
    -matches[0]: string
        Absolute path to desired file
    """
    import os
    import os.path

    matches = []
    for dirpath, dirnames, filenames in os.walk('.'):
        if name in filenames:
            matches.append(os.path.join(dirpath, name))
    if len(matches) == 0:
        logger.error("No files matching specified name")
    elif len(matches) > 1:
        logger.info("More than one file matches specified name,\
               only returning first match")
    return matches[0]
