"""Get searchable data for web query from GBT spectral products.

"""
import urllib
from BeautifulSoup import BeautifulSoup,Tag

if __name__ == '__main__':

    newsoup = BeautifulSoup(urllib.urlopen('newtable.html'))
    newtabl = newsoup.find('table')

    soup = BeautifulSoup(urllib.urlopen('../index.html'))
    soup.table.replaceWith(newtabl)
        
    f = open('../index.html','w')
    f.write(soup.prettify())
    f.close()
