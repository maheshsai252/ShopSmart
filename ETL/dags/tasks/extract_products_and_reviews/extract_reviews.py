
from collections import defaultdict
import gzip
import json
import pandas as pd
import os
def fetch_asin(sample):
    return sample.get('asin', None)
def fetch_req_fields(sample):
    asin = sample.get('asin', None)
    return {
     "reviewText": sample.get('reviewText', None) ,
     "summary": sample.get('summary', None),
     "rating": sample.get('overall', None),
     "asin":asin,
    }
def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield json.loads(l)
# cats_desired = dataset['asin'].to_list()
from collections import defaultdict
def fetch_reviews():
    dags = os.path.join(os.getcwd(), 'dags')
    resources = os.path.join(dags, 'resources')
    input_file_path = os.path.join(resources, 'Clothing_Shoes_and_Jewelry.json.gz')
    
    for cat in ['Men Clothing','Women Clothing', 'Boys Clothing','Girls Clothing',
'Men Shoes', 'Women Shoes', 'Boys Shoes','Girls Shoes',
'Men Watches', 'Women Watches', 'Boys Watches','Girls Watches']:
        cat = cat.lower().replace(' ', '_')
        output, sub_cats= fetch_reviews("train/Clothing_Shoes_and_Jewelry.json.gz",cat)
        sub_cats = defaultdict(int)

        output = []
        dataset = pd.read_csv(f'{cat}_data.csv')
        cats_desired = dataset['asin'].to_list()
        for sample in parse(input_file_path):
            info = fetch_asin(sample)
            if info in cats_desired and sub_cats[info]<100:
                    dic=fetch_req_fields(sample)
                    if dic['reviewText'] != "" and dic['summary'] != "":
                        sub_cats[info]+=1
                        output.append(dic) 
                        
        dataset = pd.DataFrame(output)
        op_file_path = os.path.join(resources, f"{cat}_reviews_data.csv")
        dataset.to_csv(op_file_path, index=False)    
                    
