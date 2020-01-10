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
                        'rank':tds[0].string,
                        'top4':tds[3].string,
                        'tier2':tds[4].string
                    }
    with open("author_rank.json",'w') as j:
        json.dump(author_rank, j)

def normalize(sorted_rank):
    normalized_rank = {}
    m = sorted_rank[0][1]
    for c in range(len(sorted_rank)):
        normalized_rank[sorted_rank[c][0]] = sorted_rank[c][1] / m
    return normalized_rank

def get_conf_rank():
    ps_conf_rank = {}
    cn_conf_rank = {}
    ca_conf_rank = {}
    with open('list.txt','r') as f:
        conf_list = f.read().split('\n')[:-1]
    for c in conf_list:
        conf = c.split('.')[0]
        author_point = 0
        author_num = 0
        print('Now checking ' + c)
        with open("committee/"+c,'r') as f:
            txt = f.read()
        with open("author_rank.json",'r') as f:
            author_rank = json.load(f)
        for author in author_rank:
            if author in txt:
                point = int(author_rank[author]['top4']) + int(author_rank[author]['tier2']) * 0.5
                author_point += point
                author_num += 1
        paper_submission = conf_submitted_paper[conf]
        committee_num = len(txt.split('\n'))-1
        committee_activeness = author_point
        ps_conf_rank[conf] = paper_submission 
        cn_conf_rank[conf] = committee_num
        ca_conf_rank[conf] =  committee_activeness
    ps_conf_rank = sorted(ps_conf_rank.items(), key=lambda ps_conf_rank:ps_conf_rank[1],reverse=True)
    cn_conf_rank = sorted(cn_conf_rank.items(), key=lambda cn_conf_rank:cn_conf_rank[1],reverse=True)
    ca_conf_rank = sorted(ca_conf_rank.items(), key=lambda ca_conf_rank:ca_conf_rank[1],reverse=True)

    ps_conf_rank = normalize(ps_conf_rank)
    cn_conf_rank = normalize(cn_conf_rank)
    ca_conf_rank = normalize(ca_conf_rank)

    print("Paper submission rank:")
    print(ps_conf_rank)
    print("Committee number rank:")
    print(cn_conf_rank)
    print("Committee activeness rank:")
    print(ca_conf_rank)

    total_conf_rank = {}
    for c in conf_list:
        conf = c.split('.')[0]
        total_conf_rank[conf] = ps_conf_rank[conf] * 0.3 + cn_conf_rank[conf] * 0.2 + ca_conf_rank[conf] * 0.5
    print("Total rank:")
    print(sorted(total_conf_rank.items(), key=lambda total_conf_rank:total_conf_rank[1],reverse=True))


    


if __name__ == "__main__":
    #get_author_rank()
    get_conf_rank()
