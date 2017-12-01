import csv
import os
import time


class StartURLs(object):
    """ Start urls select based on user input for selected category"""

    def user_input(object):

        start_url_category_list = []
        file_path = os.path.realpath('../utilities/bin/start_url/start_URL.csv')
        with open(file_path, 'r') as start_url_file:
            for row in csv.DictReader(start_url_file):
                if row['Category'] not in start_url_category_list:
                    start_url_category_list.append(row['Category'])

        sorted_category_list = sorted(start_url_category_list)
        for index, category in enumerate(sorted_category_list, 1):
            print '{0}. {1}'.format(index, category)

        category_choice = int(raw_input("Choose Category:\n"))

        while True:
            if category_choice != (index + 1):
                category = sorted_category_list[category_choice - 1]
                return category
            else:
                pass

    def get_start_urls(self, category_name):

        path_to_file = os.path.realpath('../utilities/bin/start_url/start_URL.csv')

        start_urls_list = []
        with open(path_to_file, 'r') as start_url_file:
            for row in csv.DictReader(start_url_file):
                if row['Category'] == category_name:
                    if row['URL'] not in start_urls_list:
                        row['URL'] = row['URL'].replace('+AC0', '')
                        start_urls_list.append(row['URL'])
                        time.sleep(3)

        # print start_urls_list
        return start_urls_list
