import json
import requests


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


name = 'Inception'
get = requests.get('https://api.themoviedb.org/3/search/movie?api_key=76f0719660749f8255ebb6e4c3a0b8b5&query={}'.format(name))
results = get.json()['results'][0]
print(results)


c = requests.get('https://api.themoviedb.org/3/movie/{}/credits?api_key=76f0719660749f8255ebb6e4c3a0b8b5'.format(results.get('id')))


def casts():
    for i in c.json()['cast']:
        yield i

cas = casts()
for _ in range(5):
    print(next(cas).get('name'))


# print(casts.json()['cast'][0])