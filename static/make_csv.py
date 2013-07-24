"""Get searchable data for web query from GBT spectral products.

"""
import fitsio
import sys
import os.path
import glob
import csv

# from http://www.bdnyc.org/2012/10/15/decimal-deg-to-hms/
# convert decimal degrees to HMS format
def deg2hms(ra='', dec='', doRound=False):
    RA, DEC, rs, ds = '', '', '', ''
    if dec:
        if str(dec)[0] == '-':
            ds, dec = '-', abs(dec)
        else:
            ds, dec = '+', abs(dec)
    deg = int(dec)
    decM = abs(int((dec-deg)*60))
    if doRound:
        decS = int((abs((dec-deg)*60)-decM)*60)
    else:
        decS = (abs((dec-deg)*60)-decM)*60
    DEC = '{0}{1:02d}d {2:02d}\' {3:02d}"'.format(ds, deg, decM, decS)
  
    if ra:
        if str(ra)[0] == '-':
            rs, ra = '-', abs(ra)
        raH = int(ra/15)
        raM = int(((ra/15)-raH)*60)
        if doRound:
            raS = int(((((ra/15)-raH)*60)-raM)*60)
        else:
            raS = ((((ra/15)-raH)*60)-raM)*60
        RA = '{0}{1:02d}h {2:02d}m {3:02d}s'.format(rs, raH, raM, raS)
  
    if ra and dec:
        return (RA, DEC)
    else:
        return RA or DEC

class CSV:
    def __init__(self,newcsv=False):
        if newcsv:
            csvfile =  open('spectral_products.csv', 'w')
            self.csvwriter = csv.writer(csvfile)
            self.csvwriter.writerow(('Target', 'Project ID', 'Date', 'Right Ascension',
                                     'Declination', 'Observer', 'FITS', 'PNG'))
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
        coordtype1 = table[0]['CTYPE2'].strip()
        coordtype2 = table[0]['CTYPE3'].strip()
        if 'RA' == coordtype1 and 'DEC' == coordtype2:
            ra, dec = deg2hms(ra=table[0]['CRVAL2'],dec=table[0]['CRVAL3'], doRound=True)
        else:
            print 'ERROR: CTYPE2,CTYPE3 not RA,DEC, it\'s', coordtype1, coordtype2
            sys.exit()
        
        self.csvwriter.writerow((target, projid, date, ra, dec, observer, fname, pngfile))

if __name__ == '__main__':

    csv_object = CSV(newcsv=True)
    fitsfiles = glob.iglob('*.fits')
    map(csv_object.make_entry, fitsfiles )
