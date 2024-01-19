import http.client
from bs4 import BeautifulSoup
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    rating: float
    rating_count: int
    regular_price: float
    selling_price: float
    link: str

def get_amazon_price(product_keyword, num_of_items = 5):
    product_keyword_url = product_keyword.replace(' ','+')
    conn = http.client.HTTPSConnection("www.amazon.ca")
    payload = ''
    headers = {
        'Cookie': 'i18n-prefs=CAD; session-id=144-9862407-0364707; session-id-time=2082787201l'
    }
    conn.request("GET", "/s?k=%s" % (product_keyword_url), payload, headers)
    res = conn.getresponse()
    data = res.read()
    html_content = data.decode("utf-8")
    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.find_all('div', {'class': 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'})
    items_info = []
    for i in range(num_of_items):
        item = items[i]
        item_info = {}
        item_name_element = item.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
        rating_element = item.find('span', {'class': 'a-icon-alt'})
        reviews_element = item.find('span', {'class': 'a-size-base s-underline-text'})
        price_element = item.find('span', {'class': 'a-offscreen'})

        item_info['name'] = item_name_element.text.strip() if item_name_element else None
        item_info['rating'] = rating_element.text.strip() if rating_element else None
        item_info['reviews'] = reviews_element.text.strip() if reviews_element else None
        item_info['price'] = price_element.text.strip() if price_element else None

        items_info.append(item_info)
    return items_info

def get_bestbuy_price(product_keyword, num_of_items = 5):
    product_keyword_url = product_keyword.replace(' ','%20')
    import http.client
    import json
    conn = http.client.HTTPSConnection("www.bestbuy.ca")
    payload = ''
    headers = {
    'Cookie': '_abck=2A45CBEE376219C45CAD95E1AD60D184~-1~YAAQPKErFyWl9gSNAQAAW1xcIgvx5D4TRSTZ8ALSpuyJ+cbV3gWofpLKk7dOY+nORADBqRRQfzuNWCZoYXopvDrJycp45aKi/LRJxAr/erX3AN4A93xNEfbFX6a2p2LxJ4E52iXzu9W8kEIPKpuN17sijk5FPFYIdPud/z/Bp/L9v38Hb7Kq5J7Xy/L4TlQFUvB/uVxdfd1TTZw8iS/X3SM33omvOsHmmECZiWjh95fd6BalaKbCirHKYqj3qSQlIRr+tB0RzRE1bI7+5saW5EJx6fCpPvo1thsUs4cXdFOq0I7DzkjbnBph8hkAIC3yB0QrmTE+IvW+Vijd3TvF+Ags4YRVzxHIj0rUtm0bvanxKqd29wknZmQ92Gc=~-1~-1~-1; ak_bmsc=ABE753FB8FFA570C187A975FD69FFD19~000000000000000000000000000000~YAAQRqErF+oalRaNAQAAeMLfIhY/aAq9XQjoCSJWLLP9VvBVmsidBezMJfo0emNN8FEPF2HqxFv96tSMZybr6B+uBl7sQ+mStj90QNF91aUSOyPic55fhoQa2gJ47DqmJA4J6HMotWi26yNiI2AX6WV1heuZzbvzXClxJWj2FXjPz58yWe9yNmI/QFZjrXA/NiIkEsR37yFLaIPUYbt7OZHiN25qYHS7ZBCTYSBokkgIwpC7vrVsihfb8us5UqYKx37+bS97QIIhPKpjyT1YqLVtCFvw/Te1jgUAf+1sfm8egFnGn0hGT6kAUcoUBeqET6C47S93rOGL4tbs/Z6Rj8YU6Txx0FtG9dGWPct60C+mIUZ7lADes+ip9Gs=; bm_sv=B116CA205FC97FFA88401374CFFA0D03~YAAQVaErF94mH/CMAQAAmXtzIhYWjH7Ns5p6RstpFU0g6be9Ey27fv4f0v/2dLKcwicGTrQpctYx80NDY6XmZ5gvvqaOkqzrqbHoww1QIeqOKqJb2eAJLUCPZeYUrNCJyNw7JkW3DB1AsGszMf+8KoEXOXIkNdF3vEeyO1w4GUCKguahr5wd94PJJKZ2zublEp2vPUcHJadDtQz1WPeVi31OTPHf3QETaaaWaxEDVyLsc7UZluull8+UwZiEwmwp~1; bm_sz=91FBC0B8A46C82016CADDD461FA5A115~YAAQPKErFyil9gSNAQAAW1xcIhY/cTGT/kha4eNsXJt7Rzwpr2+vd/4dCCF5AqRHo1v8NoceH952ztOaalTV+/IYtSqujXp+ZvUvE9FjWCw/zfLTPCLWBJRmghgkmJ2ev8D17v8fJzd/jRsvDtLkbm6f8iclHne+2FDeXPr1iJA1zXaScpXONKCSbxi78kI25Byu4uIlBWEHD+rWJxdeLXpyc0tp0m6IAvbAc/OtpFocRzKBoT6igusyCq4d4trzQ04bOaUNIv2MuHI7dnc++v8CSkHmFnAoScQBzBku4ukJASnBIrMUaKec4pap8OXxzZaU44dFh12/PPfcYJ90xoKe2PEEBt3QlMJuUJb5b9bRuNQYAAx+LNtEXc7WSH4rkboHa5HASjwkTAYbQEtx0VxCPKRY04w2Cw==~4536113~4274487; 970ea41f6e2ccf8251d61b0248ed499d=ad74b91b58ad6f54ed3dcf450e2b758d; s_token=3ca12b1797b428009e96aa652b030000373d0000; search_abtesting_query=B0'
    }
    conn.request("GET", f"/api/v2/json/search?categoryid=&currentRegion=ON&include=facets%252C%2520redirects&lang=en-CA&page=1&pageSize=24&path=&query={product_keyword_url}&exp=labels%252Csearch_abtesting_100%253Ab0%252Csearch_abtesting_query%253Ab0&token=db36d91703e030007b9caa65d9000000ba070100&sortBy=relevance&sortDir=desc", payload, headers)
    res = conn.getresponse()
    data = res.read()
    html_content = data.decode("utf-8")
    html_content_json = json.loads(html_content)
    products = html_content_json['products']
    return products

# Example usage:
product_keyword = 'Breville Barista Express Espresso Machine'
# product_keyword_url = product_keyword.replace(' ','+')
amazon_items = get_amazon_price(product_keyword, 3)
bestbuy_price = get_bestbuy_price(product_keyword)

# print('Amazon Price:', amazon_itemsZ)
print('Best Buy Price:', bestbuy_price)
