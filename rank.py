import requests
import json
from bs4 import BeautifulSoup

conf_submitted_paper = {
        'NDSS':570,
        'Usenix Sec':729,
        'IEEE S&P':679,
        'ACM CCS':933,
        'ACM AsiaCCS':258,
        'RAID':166,
        'ISC':86,
        'DIMVA':80,
        'ACSAC':266,
        'EuroS&P':210,
        'DSN':252,
        'PETS':300,
        'ACNS':111,
        'ESORICS':344,
        'ICICS':199,
        'ACM WiSec':91,
        'ACM-CODASPY':119,
        'ACM-SACMAT':52
        }

def get_author_rank():
    with open("author_rank.txt",'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html5lib')
    author_rank = {}
    for idx, tr in enumerate(soup.find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            author_rank[tds[1].string] = {
                        'rank':tds[0].string
                    }
    with open("author_rank.json",'w') as j:
        json.dump(author_rank, j)

def get_conf_rank():
    conf_rank = {}
    with open('list.txt','r') as f:
        conf_list = f.read().split('\n')[:-1]
    for c in conf_list:
        conf = c.split('.')[0]
        conf_rank[conf] = 0
        author_point = 0
        author_num = 0
        print('Now checking ' + c)
        with open("committee/"+c,'r') as f:
            txt = f.read()
        with open("author_rank.json",'r') as f:
            author_rank = json.load(f)
        for author in author_rank:
            if author in txt:
                point = 1531 - int(author_rank[author]['rank'])
                author_point += point
                author_num += 1
        committee_num = len(txt.split('\n'))-1
        committee_quality = author_point
        paper_submission = conf_submitted_paper[conf]
        conf_rank[conf] = paper_submission * 0.3 + committee_num * 0.2 + committee_quality * 0.5
        print("%f:%f:%f"%(paper_submission * 0.3, committee_num * 0.2, committee_quality * 0.5))
    print(sorted(conf_rank.items(), key=lambda conf_rank:conf_rank[1],reverse=True))


    


if __name__ == "__main__":
    #get_author_rank()
    get_conf_rank()
