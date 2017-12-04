
class CleanUp_class(object):

    def __init__(self, category_name):
        self.category_name = category_name

    def sku_suffix(self, category_name):
        return self.sku_dict()[category_name]

    def sku_dict(self):
        dict = {
                'MensRunning': 'MENSRUNN',
                'Running': 'RUNNING',
                }
        return dict
