import requests
from bs4 import BeautifulSoup


class Catalog:
    def __init__(self, url: str):
        self.data = []
        self.version = ''
        self.url = url

    @staticmethod
    def __load_children(target):
        for i in target:
            response = requests.get(i['url'], verify=False)
            soup = BeautifulSoup(response.text, 'lxml').find(id='content')
            print(soup.find_all(class_='col-md-4'))
            children = []  # [{'url': i.a['href']} for i in soup.find_all(class_='col-md-4')]
            for j in soup.find_all(class_='col-md-4'):
                if j.a:
                    child = {'url': j.a['href']}
                    children.append(child)
            i['children'] = children
            Catalog.__load_children(i['children'])



    def load(self):
        response = requests.get(self.url, verify=False)
        soup = BeautifulSoup(response.text, 'lxml').find(id='menu').find(class_='dropdown-menu')
        self.data = [{'name': i.a.text.replace('  ', ''), 'url': i.a['href']} for i in soup.find_all('li')]
        Catalog.__load_children(self.data)
        print(self.data)


my_catalog = Catalog('https://orangebattery.ru/')
my_catalog.load()
