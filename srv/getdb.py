import mysqlh

dblookup = {
    "mysql": mysqlh.MySQLHandler    
}


def get_handler(config: dict):
    return dblookup[config["type"]](config=config)
