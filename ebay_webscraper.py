import requests
from bs4 import BeautifulSoup

# TODO:
# 1. Make a request to the ebay.com and get a page 
# 2. Collect data from detail page 
# 3. Collect all links to detail pages of each product
# 4. Write scaped data to a csv file

def get_page(url):
    response = requests.get(url)

    # If error in reaching Ebay via provided url, throw a custom error message
    if not response.ok:
        print('Server responded:', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')

    return soup

# Returns a dictionary containing the title, price, currency, and number of item sold given an item's url link
def get_detail_data(soup):
    # Get title of item
    try:
        title = soup.find('h1', id='itemTitle').text
        title = title.lstrip("Details about \xa0")
    except:
        title = ''

    # Get price of item
    try:
        p = soup.find('span', id='prcIsum').text.strip()
        currency, price = p.split(' ')
    except:
        currency = ''
        price = ''

    # Get # of items sold (note, this is inconsistent)
    try:
        sold = soup.find('span', class_='vi-qtyS').find('a').text.strip().split(' ')[0].replace('\xa0', '')
    except:
        sold = ''

    data = {
        'title': title,
        'price': price,
        'currency': currency,
        'total_sold': sold
    }

    return data

def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []

    urls = [item.get('href') for item in links]
    urls = urls[1:]

    return urls

def main():
    # Copy paste a search URL from Ebay into the single quotes below:
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=lego+star+wars+republic+gunship+set+7676&_sacat=0&rt=nc&LH_ItemCondition=3&_pgn=1' # <-- ENTER SEARCH URL HERE
    numberOfHits = 15 # <-- ENTER NUMBER OF HITS FROM EBAY HERE TO HELP MINIMIZE ERROR
    sum = 0.0         # Will store sum of Ebay hits
    numberOfValidItems = 0 # Counts number of hits listed in US currency
    average = 0.0     # Will store average value of Ebay hits

    products = get_index_data(get_page(url))

    for link in products[0:numberOfHits]:
        data = get_detail_data(get_page(link))
        print(data)

        if (data['currency'] == 'US'):
            numberOfValidItems += 1
            sum +=  float(data['price'][1:]) # Add price of item to sum; the '[1:]' is used to omit the dollar sign from the price listed as a string

    average = sum / numberOfValidItems
    print("\nThe average price of this item on Ebay is: $%.2f" % average) # Print average price from relevant hits

if __name__ == '__main__':
    main()
