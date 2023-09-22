from bs4 import BeautifulSoup
import requests


def extract_listing_info(li_element):
    try:
        title = li_element.find('div', class_='title').text.strip()
        link = li_element.find('a')['href']
        price = li_element.find('div', class_='price').text.strip()
        location = li_element.find('div', class_='location').text.strip()
    except AttributeError:
        location = "N/A"
        title = "N/A"
        link = "N/A"
        price = "N/A"
    return {
        "Title": title,
        "Link": link,
        "Price": price,
        "Location": location
    }

url = 'https://annapolis.craigslist.org/search/sss?bundleDuplicates=1&hasPic=1&max_price=200&min_price=2&purveyor=owner#search=1~grid~0~0'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    li_elements = soup.find_all('li', class_='cl-static-search-result')

    listing_info_list = [extract_listing_info(li_element) for li_element in li_elements]

    if listing_info_list:
        for listing_info in listing_info_list:
            for key, value in listing_info.items():
                print(f"{key}: {value}")
            print("-" * 40)

        print(f"Total listings printed: {len(listing_info_list)}")
    else:
        print("No matching elements found on the page.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
