import requests
from bs4 import BeautifulSoup
import os


class Loader:
    def __init__(self):
        self.i = 0;
        self.set = ['|', '/', '-', '\\']

    def step(self):
        os.system('clear')
        print(self.set[self.i])
        self.i += 1
        if self.i > 3: self.i=0



class Catalog:
    def __init__(self, url: str):
        self.data = [{'name:': 'root', 'url': url}]
        self.version = ''
        self.url = url

    @staticmethod
    def __load_children(target):
        loader = Loader()
        for i in target:
            response = requests.get(i['url'], verify=False)
            soup = BeautifulSoup(response.text, 'lxml').find(id='content')
            children = []  # [{'url': i.a['href']} for i in soup.find_all(class_='col-md-4')]
            if soup.find(class_='col-md-4 text-center'):
                for j in soup.find_all(class_='col-md-4 text-center'):
                    child = {'url': j.a['href'], 'name': j.find('h4').text}
                    children.append(child)
                    loader.step()
                i['children'] = children
                Catalog.__load_children(i['children'])
            elif soup.find(class_='product-list'):
                for j in soup.find_all(class_='product-list'):
                    a = j.find('a')
                    child = {'url': a['href'], 'name': a.text}
                    children.append(child)
                    loader.step()
                i['children'] = children
                Catalog.__load_children(i['children'])
            elif soup.find(class_='product-description'):
                description = soup.find(class_='product-description')
                i['brand'] = description.ul.text


    def load(self):
        Catalog.__load_children(self.data)
        print(self.data)


my_catalog = Catalog('https://orangebattery.ru/category')
my_catalog.load()
