import requests,re,json,uuid, fnmatch, os
from bs4 import BeautifulSoup   
from user_agent import generate_user_agent
from time import sleep 
from pprint import pprint

url_base  = "http://www.immostreet.com"
headers = requests.utils.default_headers()
headers.update({ 'User-Agent':generate_user_agent(os=('mac', 'linux'))})
proxies = {'http' : 'http://10.10.0.0:0000',  
          'https': 'http://120.10.0.0:0000'}


def get_number_total_page():
    """ Return number total of page to crawl """
    url = "http://www.immostreet.com/Agency/Search?currentPage=0&placeId=4814836"
    try:
        resource = requests.get(url, timeout=5,headers=headers)
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
            url_start = var[:start]
            url_last = var[last:]
            number_page = var[start:last]
            url = [url_start, url_last,int(number_page)]
        else :
            print(resource.status_code)
    except requests.Timeout as e:
        print('Times up')
        print(str(e))
    return url

# soupe_resource = BeautifulSoup(resource.text, "html.parser")

# # end get number

def crawlDef(soupe_resource,data_json) :
    """ crawl the current  page """

    crawl = soupe_resource.select('.panel-default')[1:11]

    # with open('C:/Users/sbens/Documents/ScrapKeeseek/users2.json') as outfile:
    #     data = json.load(outfile)
    titles = []
    scrape = {}
    
    #title annonce
    for r in crawl :
        title  = r.find('div', class_='panel-title').text.strip()
        if title == "" :
            title = "Ma title"
        titles.append(title)
    
    # adress information
    tags = soupe_resource.find_all("address")

    scrape = data_json

    for index,tag  in enumerate(tags) :
        address = tag.find('p').text.strip().lower()
        tel = tag.find('strong').text.strip()
        mail = tag.find('a').text.strip().lower()

        data_dict = {
            'id' : str(uuid.uuid4()),
            "title" : titles[index].lower(),
            "address" : re.sub("\n|\r", " ",address),
            "phone" : tel,
            "email" : re.sub("\n|\r", " ",mail )
        }

        scrape[data_dict['address']] = data_dict
    print(scrape)
    print('Done ...')
    return scrape

url = get_number_total_page()

def check_file_exist(file_name) :
    """ check if json file in parameter exist in the current directory """
    listOfFiles = os.listdir('.')  
    pattern = "*.json"  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            if entry == file_name :
                return True

def launch_crawl(url) :
    max = 11
    pages_max = url[2]
    if pages_max > max :
        pages_max = max
    else:
        pages_max
 
    if check_file_exist('dict.json') :
        with open('dict.json') as json_data:
            d = json.load(json_data)
            json_data.close()
            print('json loaded ...')
    else :
        json_data = open('dict.json', 'w+')
        d = {}
     
    for page in range(0,pages_max) :
        url = get_number_total_page()
        url = url_base+url[0]+ str(page) +url[1]
        print('pete here ...')
        pprint(url)
        # url = "http://www.immostreet.com/Agency/Search?currentPage=" + str(page) +"&placeId=4814836"

        try:
            if page % 2 == 0 :
                print('go to sleep ...', page)
                sleep(2)
            else :
                print('go to sleep ...', page)
                sleep(1)
            resource = requests.get(url, timeout=5,headers=headers)
            if resource.status_code == 200 :
                soupe_resource = BeautifulSoup(resource.text, "html.parser")
                json_test = json.dumps(crawlDef(soupe_resource,d))
                print("crawl activate ....")
                print("json dumps ....")

                f = open("dict.json","w")
                f.write(json_test)
                print('f writing ...')
            else :
                print(resource.status_code)
        except  requests.Timeout as e:
            print('Times up')
            print(str(e))
    f.close()
    resource.close()


launch_crawl(url)

print("crawl over thank _/¨^¨\_  ")






