import requests
from helpers.math_helpers import numify


# Returns the value of an item based on the API call as an integer. Must use the item ID to make the API call
async def get_item_value(item_id):
    print("Trying to find price for", item_id)
    url = f'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={item_id}'

    try:
        response = requests.get(url)
        json_response = response.json()
        item_price = json_response['item']['current']['price']
        print("Price found", item_price)
        return numify(item_price)
    except Exception as e:
        print(f"Err fetching item {item_id} from Database:", e)
        return None
