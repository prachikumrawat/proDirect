import csv
import os


class Restrictions(object):
    def __init__(self):
        self.file_path = "../utilities/bin/restricted/"

    def parse_brands(self, brand_name):
        path = os.path.realpath(self.file_path + 'Restricted_Brands.csv')
        print "Check Brand Name:", brand_name
        restricted_brands_list = []
        with open(path, 'r') as restricted_brands_file:
            for row in csv.DictReader(restricted_brands_file):
                brand = row['Brands'].replace('+AC0', '').strip()
                restricted_brands_list.append(brand)

        if brand_name in restricted_brands_list:
            return True
        else:
            return False
