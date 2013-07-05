"""Get searchable data for web query from GBT spectral products.

"""
import csv

if __name__ == '__main__':

    f = open('newtable.html','w')

    csvfile = open('spectral_products.csv','r')
    csvreader = csv.DictReader(csvfile)
    fields = csvreader.fieldnames
    f.write('<table id="spectable" class="bordered-table zebra-striped">')

    # write table header
    f.write("<thead>")
    f.write("<tr>")
    for field in fields:
        f.write("<th>{0}</th>".format(field))
    f.write("</tr>")
    f.write("</thead>")

    # write table data
    f.write("<tbody>")
    for line in csvreader:
        f.write("<tr>")
        for field in fields:
            if field != 'fits' and field != 'png':
                val = line[field]
            else:
                val = "<a href='static/{0}'>download</a>".format(line[field])
            f.write("<td>{0}</td>".format(val))
        f.write("</tr>")
    f.write("</tbody>")

    f.write("</table>")
    f.close()
