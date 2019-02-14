import requests
from bs4 import BeautifulSoup   
import re
from user_agent import generate_user_agent
from time import sleep
import json
import uuid
url_base  = "http://www.immostreet.com/Agency/Search?currentPage=0&placeId=4814836"
headers = requests.utils.default_headers()
headers.update({ 'User-Agent':generate_user_agent(os=('mac', 'linux'))})
proxies = {'http' : 'http://10.10.0.0:0000',  
          'https': 'http://120.10.0.0:0000'}


def get_number_total_page():
    """ Return number total of page to crawl """
    try:
        resource = requests.get(url_base, proxies=proxies, timeout=5,headers=headers)
        if resource.status_code == 200 :
            soupe_resource = BeautifulSoup(resource.text, "html.parser")
            resource.close()
            pagination = soupe_resource.find('ul', class_='pagination')

            # print(pagination)
            page  = pagination.find_all('a')[-1]

            var = page['href']

            # extract number page
            start = var.find('Page=')
            # print(start)

            last = var.find('&')
            # print(last)

            start+=5
            print(var[start:last])
            print(var[:start])
            print(var[last:])

            number_page = var[start:last]
        
        else :
            print(resource.status_code)
    except requests.Timeout as e:
        print('Times up')
        print(str(e))
    return number_page

# soupe_resource = BeautifulSoup(resource.text, "html.parser")

# # end get number

def crawlDef(soupe_resource) :
    """ crawl the current  page """

    crawl = soupe_resource.select('.panel-default')[1:11]

    titles = []
    scrape = []
    
    #title annonce
    for r in crawl :
        title  = r.find('div', class_='panel-title').text.strip()
        if title == "" :
            title = "Ma title"
        titles.append(title)
    
    # adress information
    tags = soupe_resource.find_all("address")

    for index,tag  in enumerate(tags) :
        address = tag.find('p').text.strip()
        tel = tag.find('strong').text.strip()
        mail = tag.find('a').text.strip()

        data_dict = {
            'id' : str(uuid.uuid4()),
            "title" : titles[index],
            "address" : re.sub("\n|\r", " ",address),
            "phone" : tel,
            "email" : re.sub("\n|\r", " ",mail )
        }

        scrape.append(data_dict)
        print(scrape)
        print('Done ...')
    return scrape

def launch_crawl() :
    # pages = get_number_total_page()  int(pages)-
    outfile = open('users.json', 'a')
    for page in range(0,1) :
        # url = url_base+var[:start]+ i +var[last:]
        url = "http://www.immostreet.com/Agency/Search?currentPage=" + str(page) +"&placeId=4814836"
        try:
            if page % 2 == 0 :
                print('go to sleep ...', page)
                sleep(2)
               
            resource = requests.get(url, timeout=5,headers=headers)
            if resource.status_code == 200 :
                soupe_resource = BeautifulSoup(resource.text, "html.parser")
                crawlDef(soupe_resource)
                json.dump(crawlDef(soupe_resource), outfile, ensure_ascii=False)
                resource.close()
                
            else :
                print(resource.status_code)
        except  requests.Timeout as e:
            print('Times up')
            print(str(e))
    outfile.close()
    print('created file ....', outfile.name)    



launch_crawl()




    




