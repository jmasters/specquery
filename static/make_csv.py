"""Get searchable data for web query from GBT spectral products.

"""
import fitsio
import sys
import os.path
import glob
import csv

class CSV:
    def __init__(self,newcsv=False):
        if newcsv:
            csvfile =  open('spectral_products.csv', 'w')
            self.csvwriter = csv.writer(csvfile)
            self.csvwriter.writerow(('target', 'projid', 'date', 'ra',
                                     'observer', 'fits', 'png'))
        else:
            csvfile =  open('spectral_products.csv', 'a')
            self.csvwriter = csv.writer(csvfile)
        
    def make_entry(self, fname):
        pngfile = os.path.splitext(fname)[0] + '.png'

        # open the file and read the primary header
        hdr = fitsio.read_header(fname, ext=0)
        date = hdr['DATE']

        # open the file, 'SINGLE DISH' extension and read the value from
        # the first row of the table
        table = fitsio.read(fname, ext='SINGLE DISH')
        observer = table[0]['OBSERVER'].strip()
        target = table[0]['OBJECT'].strip()
        projid = table[0]['PROJID'].strip()
        coordtype = table[0]['CTYPE2'].strip()
        if 'RA' == coordtype:
            ra = str(table[0]['CRVAL2'])[:6]
        else:
            print 'ERROR: CTYPE2 not RA, it\'s', coordtype
            sys.exit()
        
        self.csvwriter.writerow((target, projid, date, ra, observer, fname, pngfile))

if __name__ == '__main__':

    csv_object = CSV(newcsv=False)
    fitsfiles = glob.iglob('*.fits')
    map(csv_object.make_entry, fitsfiles )
