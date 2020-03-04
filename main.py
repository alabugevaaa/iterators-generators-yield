import hashlib
import json
import requests


class CheckWiki:

    def __init__(self, path):
        self.file = open(path, encoding='utf8')
        self.data = json.load(self.file)
        self.start = 0
        self.session = requests.Session()

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        if self.start > len(self.data):
            raise StopIteration
        country = self.data[self.start-1]

        country_name = country['name']['common']
        url = f'https://en.wikipedia.org/wiki/{country_name.replace(" ", "_")}'
        status = self.session.get(url).status_code
        if status == 200:
            result = {country_name: url}
        else:
            result = {country_name: "Not Found"}
        return result


def hash_line(path):
    with open(path, encoding='utf8') as hosts_file:
        for line in hosts_file:
            line = line.strip().encode('utf-8')
            hash = hashlib.md5(line).hexdigest()
            yield hash


if __name__ == '__main__':

    for hash_password in hash_line('passwords.list'):
        print(hash_password)

    with open('result.json', 'w', encoding='utf8') as file:
        for country in CheckWiki('countries.json'):
            json.dump(country, file, ensure_ascii=False, indent=2)
            print(country)
