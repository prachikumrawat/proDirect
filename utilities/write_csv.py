import unicodecsv as csv
from pymongo import MongoClient


class WriteCSV(object):
    def __init__(self, output_file , category_name):
        print 'Writing File'
        client = MongoClient()
        with open('../utilities/bin/prodirect_template.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
        self.writer = csv.DictWriter(output_file, fieldnames=header)
        self.writer.writeheader()
        db = client.Prodirect_Running
        print db
        collections = db[category_name].find({})
        print "Collections:", collections
        for collection in collections:
            print collection
            self.writecsv(collection)

    def writecsv(self, product):
        del product['_id']

        self.writer.writerow(product)


    def __del__(self):
        print 'Done'

if __name__ == '__main__':
    category_name = 'MensRunning'
    output_file = open('../utilities/bin/output/prodirect_running.csv', 'wb')
    WriteCSV(output_file, category_name)
    output_file.close()
