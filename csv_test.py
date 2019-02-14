from time import sleep
import os,fnmatch
import json
import uuid


listOfFiles = os.listdir('.')  
pattern = "*.json"  
for entry in listOfFiles:  
    # if fnmatch.fnmatch(entry, pattern):
    print (entry)

print("\n\t ************************************************")
print("\t   crawl over thank _/¨^¨\_  Keeseek \/¨^¨\/")
print("\n\t ************************************************") 
max = 0.47
max = round(max)
print('round float', max)

# for root, dirs, files in os.walk("."):  
#     for filename in files:
#         print('file ...',filename)

array ={}
datas = {}

datas['tata'] = 'mamie'
datas['toto'] = 'dada22'
datas['titi'] = 'foo222'

# array.append({'id': str(uuid.uuid4()),'tata': 'mamie', 'toto': 'dada', 'titi': 'foo', 'tyty': 'mamie', 'rere': 'dada', 'tigffgti': 'foo'})
# array.append({'id': str(uuid.uuid4()),'tata': 'mamie', 'toto': 'dada', 'titi': 'foo', 'tyty': 'mamie', 'rere': 'dada', 'tigffgti': 'foo'})

file_object =  open('users2.json', 'r')
       
data = json.load(file_object)
print(data)

array = data

array[datas['tata']] = datas
print(array)

json = json.dumps(array)
f = open("users2.json","w")
f.write(json)
f.close()

