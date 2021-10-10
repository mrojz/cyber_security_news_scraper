import requests, re
from datetime import datetime

def get_hacker_news(url):

    r=requests.get(url)

    links=re.findall("<a class='story-link' href=\"(.*?)\">",r.text)
    titles=re.findall("<h2 class='home-title'>(.*?)</h2>",r.text)

    news=[]

    if 'breach' in url:
        news_type = 'breach'
    elif 'Attack' in url:
        news_type = 'attack'
    elif 'Vuln' in url:
        news_type = 'vuln'
    else:
        news_type = 'malware'

    for i in range(len(links)):
        news.append(
            {
            'link':links[i],
            'text':titles[i],
            'type':news_type,
            'date':str(datetime.now()),
            'source':'hacker news',
            'score':0,
            'show':1
            }
            )
    
    return news


def get_exploitdb():
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    }

    params = (
        ('draw', '1'),
        ('columns[0][data]', 'date_published'),
        ('columns[0][name]', 'date_published'),
        ('columns[0][searchable]', 'true'),
        ('columns[0][orderable]', 'true'),
        ('columns[0][search][value]', ''),
        ('columns[0][search][regex]', 'false'),
        ('columns[1][data]', 'download'),
        ('columns[1][name]', 'download'),
        ('columns[1][searchable]', 'false'),
        ('columns[1][orderable]', 'false'),
        ('columns[1][search][value]', ''),
        ('columns[1][search][regex]', 'false'),
        ('columns[2][data]', 'application_md5'),
        ('columns[2][name]', 'application_md5'),
        ('columns[2][searchable]', 'true'),
        ('columns[2][orderable]', 'false'),
        ('columns[2][search][value]', ''),
        ('columns[2][search][regex]', 'false'),
        ('columns[3][data]', 'verified'),
        ('columns[3][name]', 'verified'),
        ('columns[3][searchable]', 'true'),
        ('columns[3][orderable]', 'false'),
        ('columns[3][search][value]', ''),
        ('columns[3][search][regex]', 'false'),
        ('columns[4][data]', 'description'),
        ('columns[4][name]', 'description'),
        ('columns[4][searchable]', 'true'),
        ('columns[4][orderable]', 'false'),
        ('columns[4][search][value]', ''),
        ('columns[4][search][regex]', 'false'),
        ('columns[5][data]', 'type_id'),
        ('columns[5][name]', 'type_id'),
        ('columns[5][searchable]', 'true'),
        ('columns[5][orderable]', 'false'),
        ('columns[5][search][value]', ''),
        ('columns[5][search][regex]', 'false'),
        ('columns[6][data]', 'platform_id'),
        ('columns[6][name]', 'platform_id'),
        ('columns[6][searchable]', 'true'),
        ('columns[6][orderable]', 'false'),
        ('columns[6][search][value]', ''),
        ('columns[6][search][regex]', 'false'),
        ('columns[7][data]', 'author_id'),
        ('columns[7][name]', 'author_id'),
        ('columns[7][searchable]', 'false'),
        ('columns[7][orderable]', 'false'),
        ('columns[7][search][value]', ''),
        ('columns[7][search][regex]', 'false'),
        ('columns[8][data]', 'code'),
        ('columns[8][name]', 'code.code'),
        ('columns[8][searchable]', 'true'),
        ('columns[8][orderable]', 'true'),
        ('columns[8][search][value]', ''),
        ('columns[8][search][regex]', 'false'),
        ('columns[9][data]', 'id'),
        ('columns[9][name]', 'id'),
        ('columns[9][searchable]', 'false'),
        ('columns[9][orderable]', 'true'),
        ('columns[9][search][value]', ''),
        ('columns[9][search][regex]', 'false'),
        ('order[0][column]', '9'),
        ('order[0][dir]', 'desc'),
        ('start', '0'),
        ('length', '15'),
        ('search[value]', ''),
        ('search[regex]', 'false'),
        ('author', ''),
        ('port', ''),
        ('type', ''),
        ('tag', ''),
        ('platform', ''),
        ('_', '1633491555521'),
    )
    exploitdb=[]
    r = requests.get('https://www.exploit-db.com/', headers=headers, params=params).json()
    for data in r['data']:
        exploitdb.append(
            {
            'link':'https://www.exploit-db.com/exploits/{}'.format(data['description'][0]),
            'text':data['description'][1].replace('&#039;',"'"),
            'type':'exploit','verified':data['verified'],
            'date':str(datetime.now()),
            'source':'exploit db',
            'score':0,
            'show':1
            }
            )
    return exploitdb

urls=[]
urls.append("https://thehackernews.com/search/label/data%20breach")
urls.append("https://thehackernews.com/search/label/Cyber%20Attack")
urls.append("https://thehackernews.com/search/label/Vulnerability")
urls.append("https://thehackernews.com/search/label/Malware")