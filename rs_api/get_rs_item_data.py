import requests

async def get_rs_item_data(id):
    url = f'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={id}'

    try:
        response = requests.get(url)
        json_response = response.json()
        return json_response
    except:
        print(f"Err fetching item {id} from Database.")
        return None