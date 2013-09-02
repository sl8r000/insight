import requests

class AnswersIds(object):
    def __init__(self, url, queryvars):
        self.url = url
        self.queryvars = queryvars

    def get(self, **params):
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(self.url, params=all_params)
        response.raise_for_status()
        return response.json()['items']

    def get_comments(self, **params):
        url = self.url + 'comments/'
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(url, params=all_params)
        response.raise_for_status()
        return response.json()['items']


class Answers(object):
    def __init__(self, url, queryvars):
        self.url = url
        self.queryvars = queryvars
        self.queryvars['pagesize'] = 100

    def get_all(self, **params):
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(self.url, params=all_params)
        response.raise_for_status()
        return response.json()['items']

    def ids(self, id_or_ids):
        if isinstance(id_or_ids, list):
            url = self.url + ';'.join(str(input_id) for input_id in id_or_ids) + '/'
        else:
            url = self.url + str(id_or_ids) + '/'
        return AnswersIds(url, self.queryvars)

class UsersIds(object):
    def __init__(self, url, queryvars):
        self.url = url
        self.queryvars = queryvars

    def get(self, **params):
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(self.url, params=all_params)
        response.raise_for_status()
        return response.json()['items']

    def get_answers(self, **params):
        url = self.url + 'answers/'
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(url, params=all_params)
        response.raise_for_status()
        return response.json()['items']

    def get_badges(self, **params):
        url = self.url + 'badges/'
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(url, params=all_params)
        response.raise_for_status()
        return response.json()['items']

    def get_comments(self, **params):
        url = self.url + 'comments/'
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(url, params=all_params)
        response.raise_for_status()
        return response.json()['items']

    def get_favorites(self, **params):
        url = self.url + 'favorites/'
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(url, params=all_params)
        response.raise_for_status()
        return response.json()['items']

    def get_questions(self, **params):
        url = self.url + 'questions/'
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(url, params=all_params)
        response.raise_for_status()
        return response.json()['items']

    def get_tags(self, **params):
        url = self.url + 'tags/'
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(url, params=all_params)
        response.raise_for_status()
        return response.json()['items']

class Users(object):
    def __init__(self, url, queryvars):
        self.url = url
        self.queryvars = queryvars
        self.queryvars['pagesize'] = 100

    def get_all(self, **params):
        all_params = dict(self.queryvars.items() + params.items())
        response = requests.get(self.url, params=all_params)
        response.raise_for_status()
        return response.json()['items']

    def ids(self, id_or_ids):
        if isinstance(id_or_ids, list):
            url = self.url + ';'.join(str(input_id) for input_id in id_or_ids) + '/'
        else:
            url = self.url + str(id_or_ids) + '/'
        return UsersIds(url, self.queryvars)

    
class StackExchangeClient(object):
    BASE_URL = 'http://api.stackexchange.com/2.1/'

    def __init__(self, site, client_id, key):
        self.site = site
        self.client_id = client_id
        self.key = key

        self.url = StackExchangeClient.BASE_URL
        self.queryvars = {'site': self.site, 'client_id': self.client_id, 'key': self.key}

    @property
    def answers(self):
        url = self.url + 'answers/'
        return Answers(url, self.queryvars)

    # @property
    # def comments(self):
    #     url = self.url + 'comments/'
    #     return Comments(url, self.queryvars)

    # @property
    # def questions(self):
    #     url = self.url + 'questions/'
    #     return Questions(url, self.queryvars)

    @property
    def users(self):
        url = self.url + 'users/'
        return Users(url, self.queryvars)

if __name__ == '__main__':
    client_id = 1962
    key = 'IHEAzrM4kaVEBHGcLOP)tQ(('

    client = StackExchangeClient(site='stackoverflow', client_id=client_id, key=key)
