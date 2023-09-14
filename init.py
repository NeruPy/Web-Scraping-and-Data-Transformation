from selectolax.parser import HTMLParser
import pandas as pd
from playwright.sync_api import sync_playwright
import csv 

data = {
    'asin':[],
    'title':[],
    'price':[],
    'rating':[],
    'reviews':[],
    'availability':[]
}

def get_html(page, asin):
    url = f'https://www.amazon.com.au/dp/{asin}'
    page.goto(url)
    html = HTMLParser(page.content())
    return html

def parse_html(html, asin):
    
    data['asin'].append(asin),
    data['title'].append(html.css_first("span#productTitle").text().strip())
    data['price'].append(html.css_first("span.a-offscreen").text().strip())
    data['rating'].append(html.css_first("span#acrPopover").text().strip()[3:].strip())
    data['reviews'].append(html.css_first("span#acrCustomerReviewText").text().strip().replace('ratings','reviews'))
    data['availability'].append(html.css_first("div#availability").text(deep = True).strip())
    return data

def read_csv():
    with open('products.csv','r') as f:
        reader = csv.reader(f)
        return [item[0] for item in reader]

def run():
    asin = 'B083GGYNQ6'
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch()
    page = browser.new_page()
    html = get_html(page, asin)
    product = parse_html(html, asin)
    df = pd.DataFrame(product,index=range(1,100))
    df.to_csv('csv1.csv')
    
def main():
    run()
    
    
if __name__ == "__main__":
    main()