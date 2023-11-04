from selectolax.parser import HTMLParser
import pandas as pd
from playwright.sync_api import sync_playwright
import csv 
arr = 0
def url_listing():
    stack = []
    stack.append('https://www.amazon.com.au/s?k=gtx+gpu&crid=2DFXGUNNEBTI4&qid=1699090438&sprefix=gtx+gp%2Caps%2C426&')
    for page in range(1,7):
        stack.append(f'https://www.amazon.com.au/s?k=gtx+gpu&page={page}&crid=2DFXGUNNEBTI4&qid=1699090438&sprefix=gtx+gp%2Caps%2C426&')
    stack.reverse()
    return stack

def product_info(urls):
        big_df = []
        df = pd.DataFrame()
        def parse_listing():
        
            def get_html_listing(page):
                if urls:
                    url = urls.pop()
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
                page = browser.new_page()
                html = get_html_listing(page)
                refs = parse_html_listing(html)
                return refs
            
        
            return run_listing()
        
        arr = parse_listing()
    
        Working = True
        while urls:
            if Working == True:
                data = {'asin':[],
                        'title':[],
                        'price':[],
                        'rating':[],
                        'reviews':[],
                        'availability':[]}

                def get_html(page, asin):
                    url = f'https://www.amazon.com.au/dp/{asin}'
                    page.goto(url)
                    html = HTMLParser(page.content())
                    return html

                def parse_html(html, asin):
                    
                    data['asin'].append(asin)
                    
                    data_points = {
                    'title': "span#productTitle",
                    'price': "span.a-offscreen",
                    'rating': "span#acrPopover",
                    'reviews': "span#acrCustomerReviewText",
                    'availability': "div#availability"
                    }

                    for key, selector in data_points.items():
                        element = html.css_first(selector)
                        if element and 'logAssetsNotLoaded' not in element.text(deep = True):
                            if key == 'rating':
                                data[key].append(element.text(deep = True).strip()[3:].strip())
                            elif key == 'reviews':
                                data[key].append(element.text(deep = True).strip().replace('rating','review'))
                            else:
                                data[key].append(element.text(deep = True).strip())
                        else:
                            data[key].append('')
                
                    return data
                

                def run(asin):
                    page = browser.new_page()
                    html = get_html(page, asin)
                    product = parse_html(html, asin)
                    df = pd.DataFrame.from_dict(product)
                    
                
                for x in arr:
                    run(x)
                    
                Working = False
            else:
                ds = pd.concat(df)
                ds.to_csv('csv1.csv')
                arr = parse_listing()
                Working = True
                

        

        

playwright = sync_playwright().start()
browser = playwright.chromium.launch()
urls = url_listing()
product_info(urls)
browser.close()
playwright.stop()






