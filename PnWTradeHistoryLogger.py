import urllib.request
import json

# Declaring Constants
API_KEY = 'key=fff8e63ea2ec60'
BASE_URL = 'https://politicsandwar.com/api/'
ACCESS_URL = 'trade-history/'
RECORDS_URL = '&records=5000'
RESOURCE_TYPES = ['food', 'coal', 'oil', 'uranium', 'iron', 'bauxite', 'lead', 'gasoline', 'munitions', 'steel', 'aluminum', 'credits']

# Initializing Dictionaries
TradePrices = {
    'pfood': 0,
    'qfood': 0,
    'pcoal': 0,
    'qcoal': 0,
    'poil': 0,
    'qoil': 0,
    'puranium': 0,
    'quranium': 0,
    'piron': 0,
    'qiron': 0,
    'pbauxite': 0,
    'qbauxite': 0,
    'plead': 0,
    'qlead': 0,
    'pgasoline': 0,
    'qgasoline': 0,
    'pmunitions': 0,
    'qmunitions': 0,
    'psteel': 0,
    'qsteel': 0,
    'paluminum': 0,
    'qaluminum': 0,
    'pcredits': 0,
    'qcredits': 0,
}

averageTradePrices = {
    'avgfood': 0,
    'avgoil': 0,
    'avguranium': 0,
    'avgcoal': 0,
    'avgiron': 0,
    'avgaluminum': 0,
    'avgmunitions': 0,
    'avgbauxite': 0,
    'avglead': 0,
    'avggasoline': 0,
    'avgsteel': 0,
    'avgcredits': 0,
}


# This method returns raw JSON data and JSON data as a dictionary (via API request)
def get_data(access_url):
    raw_data = urllib.request.urlopen(BASE_URL + access_url + API_KEY + RECORDS_URL)
    data = json.load(raw_data)

    return data, raw_data


# This method writes text to both 'TradeData' and 'TradeLogger' files.
def write_to_file(text, dictionary):
    # Initializing empty dictionary to store most recent trade data later.
    new_trade_history = {}

    # Try-Except statement to write text to files, if files if not found, create them.
    try:
        file = open('TradeData.txt', 'w')
        file.write(text)
        file.close()
    except OSError:
        file = open('TradeData.txt', 'x')
        history_file = open('TradeLogger.txt', 'x')

    # Try-Except statement to load json formatted data from 'TradeLogger.txt', if file is empty, continue.
    try:
        history_file = open('TradeLogger.txt', 'r')
        new_trade_history = json.load(history_file)
        history_file.close()
    except OSError:
        pass

    # Adding element to 'new_trade_history' dictionary to append most recent trade data.
    new_trade_history[str(len(new_trade_history) + 1)] = dictionary

    # Formatting 'new_trade_history' data to JSON format.
    new_text = json.dumps(new_trade_history, indent=4)

    # Writing to 'TradeLogger.txt' for long-term storage.
    history_file = open('TradeLogger.txt', 'w')
    history_file.write(new_text)
    history_file.close()


# This method retrieves the latest API data from server and updates text files.
def update_trade_data():
    # Getting API data as raw JSON data and as a dictionary.
    trade_data, raw_data = get_data(ACCESS_URL)

    # This loops through all player trades.
    for trades in trade_data['trades']:

        # Getting specific properties of the 'trades' object.
        resource_type = trades['resource']
        quantity = trades['quantity']
        price = trades['price']

        # Excludes all artificial trades or trades involving 'credits'.
        if int(price) < 6000 or (str(resource_type) == 'credits'):
            TradePrices['p' + str(resource_type)] += (int(price) * int(quantity))
            TradePrices['q' + str(resource_type)] += int(quantity)

    # Calculates the average price of each item and records it in a dictionary.
    for resource in RESOURCE_TYPES:
        if TradePrices['q' + resource] != 0:
            averageTradePrices['avg' + resource] += int(TradePrices['p' + resource] / TradePrices['q' + resource])

    # Writes the dictionary to text files in a JSON format for storage.
    write_to_file(json.dumps(averageTradePrices, indent=4), averageTradePrices)

    # Clears dictionaries.
    for i in TradePrices:
        TradePrices[i] = 0
    for i in averageTradePrices:
        averageTradePrices[i] = 0
