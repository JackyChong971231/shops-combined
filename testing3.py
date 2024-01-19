import http.client
from bs4 import BeautifulSoup

conn = http.client.HTTPSConnection("www.amazon.ca")
payload = ''
headers = {
    'Cookie': 'i18n-prefs=CAD; session-id=144-9862407-0364707; session-id-time=2082787201l'
}
conn.request("GET", "/s?k=Breville+Barista+Express+Espresso+Machine", payload, headers)
res = conn.getresponse()
data = res.read()
html_content = data.decode("utf-8")
soup = BeautifulSoup(html_content, 'html.parser')
items = soup.find_all('div', {'class': 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'})
for item in items:
    item_info = {}
    item_name_element = item.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
    rating_element = item.find('span', {'class': 'a-icon-alt'})
    reviews_element = item.find('span', {'class': 'a-size-base s-underline-text'})
    price_element = item.find('span', {'class': 'a-offscreen'})

    # if price_element:
    #     price_text = price_element.text.strip()
    #     print(price_text)
    item_info['name'] = item_name_element.text.strip() if item_name_element else None
    item_info['rating'] = rating_element.text.strip() if rating_element else None
    item_info['reviews'] = reviews_element.text.strip() if reviews_element else None
    item_info['price'] = price_element.text.strip() if price_element else None

    print(item_info)
    print('/n')

# print(data.decode("utf-8"))