from selectolax.parser import HTMLParser
import pandas as pd
from playwright.sync_api import sync_playwright
import csv 
def product_info(arr):
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
        
        try:
            data['asin'].append(asin),
        except AttributeError: data['asin'].append('')
        
        try:
            data['title'].append(html.css_first("span#productTitle").text().strip())
        except AttributeError: data['title'].append('')
        
        try:
            data['price'].append(html.css_first("span.a-offscreen").text().strip())
        except AttributeError: data['price'].append('')
        
        try:
            data['rating'].append(html.css_first("span#acrPopover").text().strip()[3:].strip())
        except AttributeError: data['rating'].append('')
        
        try:
            data['reviews'].append(html.css_first("span#acrCustomerReviewText").text().strip().replace('ratings','reviews'))
        except AttributeError: data['reviews'].append('')
        
        try:
            data['availability'].append(html.css_first("div#availability").text(deep = True).strip())
        except AttributeError: data['availability'].append('')
            
        return data

    def run(asin):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch()
        page = browser.new_page()
        html = get_html(page, asin)
        product = parse_html(html, asin)
        df = pd.DataFrame.from_dict(product)
        df.to_csv('csv1.csv')
        browser.close()
        playwright.stop()
        
    for x in arr:
        run(x)


def parse_listing():
    
    def get_html_listing(page):
        url =f'https://www.amazon.com.au/s?k=gtx+gpu&crid=2DFXGUNNEBTI4&sprefix=gtx+gp%2Caps%2C426&ref=nb_sb_noss_2'
        page.goto(url)
        html = HTMLParser(page.content())
        return html

    
    def parse_html_listing(html):
        arr = set()
        asins = ''
        asins = html.css('a[href*="/dp/"]')
        for x in asins:
            t = x.attributes
            ref = t.get('href',0)
            wordendindex = ref.index('/dp') + len('/dp') - 1
            wordfirstindex = ref.index('ref')
            asin = ref[wordendindex + 2:wordfirstindex - 1]
            arr.add(asin)
        return arr
        
        
    
    
    def run_listing():
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch()
        page = browser.new_page()
        html = get_html_listing(page)
        refs = parse_html_listing(html)
        browser.close()
        playwright.stop()
        return refs
    
    return run_listing()
        


amp = parse_listing()
product_info(amp)









'''''''''
##############################
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
##########################################
'''''''''