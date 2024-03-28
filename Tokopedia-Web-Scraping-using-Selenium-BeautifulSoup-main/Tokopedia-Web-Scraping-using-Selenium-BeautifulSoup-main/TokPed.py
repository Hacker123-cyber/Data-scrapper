from Page import PageScraper
import sys
import pandas as pd
from bs4 import BeautifulSoup


class Tokopedia:
    """ 
    keyword           : search query
    total pages       : number of pages will be scrape
    sorting           : sort based on {None : following system rule; 1 : paling sesuai/most suitable; 2 : review/sold (highest review and total item sold); 3 : newest}
    stars4            : item with rating above 4 stars
    offStore          : official store
    merchant pro      : professional merchant
    merchant          : verified merchant
    minPrice          : minimum price
    maxPrice          : maximum price
    """
    def __init__(self, keyword=None, totalPages=5, sort=None, stars4=False, offStore=False, merchantPro=False, merchant=False, minPrice=None, maxPrice=None):
        self.keyword = keyword.replace(' ','%20')
        self.sort = sort
        self.totalPages = totalPages
        self.stars4 = stars4
        self.offStore = offStore
        self.merchantPro = merchantPro
        self.merchant = merchant
        self.minPrice = minPrice
        self.maxPrice = maxPrice
    
    # create url based on user's inputed format
    def generate_url_format(self):
        # assign default parameter
        sort = ''
        pageNum = '{pageNum}' # will be iterated
        stars4 = ''
        maxPrice = ''
        minPrice = ''
        keyword = self.keyword
        shopTier = ''
        
        # sort by
        if self.sort != None:
            
            # paling sesuai/most suitable
            if self.sort == 1:
                sort = '23'
            
            # review/sold (highest review and total item sold)
            elif self.sort == 2:
                sort = '5'
            
            # newest
            elif self.sort == 3:
                sort = '9'
            
            # beside 3 above
            else:
                sys.exit('please choose sort between {None : following web system rule; 1 : paling sesuai/most suitable; 2 : review/sold (highest review and total item sold); 3 : newest}')
        
        # stars 4 and up
        if self.stars4:
            stars4 = '4%2C5'
        
        # user's inputed max price
        if self.maxPrice != None:
            maxPrice = self.maxPrice
        
        # user's inputeed min price
        if self.minPrice != None:
            minPrice = self.minPrice
        
        # set shop tier
        if self.offStore != False or self.merchantPro != False or self.merchant != False:
            
            # set shopTier : official store, merchant pro, and merchant
            if self.offStore and self.merchantPro and self.merchant:
                shopTier = '2%233%231'

            # set shopTier : official store and merchant pro
            elif self.offStore and self.merchantPro:
                shopTier = '2%233'

            # set shopTier : official store and merchant
            elif self.offStore and self.merchant:
                shopTier = '2%231'

            # set shopTier : merchant pro and merchant
            elif self.merchantPro and self.merchant:
                shopTier = '3%231'

            # set shoptier : official store
            elif self.offStore:
                shopTier = '2'

            # set shoptier : merchant pro
            elif self.merchantPro:
                shopTier = '3'

            # set shoptier : merchant
            elif self.merchant:
                shopTier = '1'
        
        url = f'https://www.tokopedia.comsearch?navsource=home&ob={sort}&page={pageNum}&pmax={maxPrice}&pmin={minPrice}&q={keyword}&rt={stars4}&shop_tier={shopTier}&st=product'
        
        return url

    
    # get item's title
    def get_title(self, content):
        return content.find('a', {'class':'css-gwkf0u'})['title']
    
    # get item's price
    # return in form of int
    def get_price(self, content):
        data = content.find('div', {'class':'css-a94u6c'}).get_text()
        
        return int(''.join(n for n in data if n.isdigit()))
    
    # get total sold items
    # if item doesn't have any buyers return 'terjual 0'
    def get_sold(self, content):
        if content.find('span', {'class':'css-1agvax3'}) is not None:
            return content.find('span', {'class':'css-1agvax3'}).get_text()
        else:
            return 'terjual 0'
        
    # get item's rating ex = 4.2 (float)
    # if rating doesn't exist means there is no review from user
    def get_rating(self, content):
        if content.find('span', {'class':'css-1ffszw6'}) is not None:
            return float(content.find('span', {'class':'css-1ffszw6'}).get_text())
        else:
            return ''
        
    # get item's discount ex = 9 (%)
    # if discount doesn't exist return 0
    def get_discount(self, content):
        if content.find('div', {'data-testid':'spnSRPProdDisc'}) is not None:
            data = content.find('div', {'data-testid':'spnSRPProdDisc'}).get_text()
            return int(''.join(n for n in data if n.isdigit()))
        else:
            return 0

    # get item's discounted price
    # if discounted price doesn't exist return empty string
    def get_discounted_price(self, content):
        if content.find('div', {'data-testid':'lblProductSlashPrice'}) is not None:
            data = content.find('div', {'data-testid':'lblProductSlashPrice'}).get_text()
            return int(''.join(n for n in data if n.isdigit()))
        else:
            return ''
        
    # get store name
    def get_store_name(self, content):
        if content.find_all('span', {'class':'css-qjiozs flip'}) != []:
            return content.find_all('span', {'class':'css-qjiozs flip'})[1].get_text()
        else:
            return ''
    
    # get store location
    def get_store_location(self, content):
        if content.find_all('span', {'class':'css-qjiozs flip'}) != []:
            return content.find_all('span', {'class':'css-qjiozs flip'})[0].get_text()
        else:
            return ''
        
    # get item's link
    def get_link(self, content):
        return content.find('a', {'class':'pcv3__info-content css-gwkf0u'})['href']
    
     # get all searched item div's (class = css-974ipl)
    def get_items_div(self, content):
        divItem = content.find_all('div', {'class':'pcv3__container css-gfx8z3'})
            
        return divItem
    
    # assign data
    def get_data(self, content):
        data = {
            'Title' : self.get_title(content),
            'Price (Rp)' : self.get_price(content),
            'Total Item Sold' : self.get_sold(content),
            'Rating (5.0)' : self.get_rating(content),
            'Discount (%)' : self.get_discount(content),
            'Price Before Discount (Rp)' : self.get_discounted_price(content),
            'Store Name' : self.get_store_name(content),
            'Store Location' : self.get_store_location(content),
            'Link' : self.get_link(content),
        }
        
        return data
    
    # return string with filled page={pageNum} based on the page number
    def generate_page_url(self, url, Num):
        return url.format(pageNum = Num)

    # create excel format (source: https://xlsxwriter.readthedocs.io/working_with_pandas.html)
    def to_excel(self, data, f_name= 'data_product', sheet_name = 'Sheet1'):
        # Create a workbook and add a worksheet.
        df = pd.DataFrame(data)
        
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(f'{f_name}.xlsx', engine='xlsxwriter')
        
        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name=sheet_name)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def run(self):
        url = self.generate_url_format()
        datas = []
        i = 1

        print("PROGRAM IS RUNNING PLEASE WAIT ...\n")

        # looping for each pages
        while i <= self.totalPages:
            data = []

            print("=======================================")
            print(f"ACCESSING PAGE {i} ...")

            # Generate page url
            page_url = self.generate_page_url(url = url, Num = i)
            
            # Scrape page url
            scraper = PageScraper(page_url)
            content = scraper.get_page_information()
            scraper.close_page()

            # use bs4 to scrape all the data within the page
            soup = BeautifulSoup(content)
            divItems = self.get_items_div(soup)

            # loop for each item's content found
            for div in divItems:
                data.append(self.get_data(div))

            print(f"{len(data)} DATA FOUND\n")

            datas.extend(data)
            i += 1

        print(f"\nSCRAPING COMPLETE {len(datas)} DATA FOUND IN TOTAL")
        
        return datas