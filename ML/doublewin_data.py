import requests

extra_info_url = "https://api2.bybit.com/s1/byfi/get-products-extra-info"

resp = requests.post(url=extra_info_url, json={"product_type": 10})
all_product_info = resp.json()["result"]["double_win_offers"]
print("double win:",all_product_info)
