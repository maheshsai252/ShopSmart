from collections import defaultdict
import gzip
import json
import pandas as pd
import os
def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield json.loads(l)
def fetch_category(sample):
    return sample.get('category', None)
def fetch_req_fields(sample):
    asin = sample.get('asin', None)
    fs = sample.get('feature', None)
    fea=""
    if fs:
        for i in fs:
            fea+=i+"\n"
    ds = sample.get('description', None)
    desc=""
    if ds:
        for i in ds:
            desc+=i+"\n"
    title = sample.get('title', None)

    return {
     "title": title,
     "features": fea,
     "description": desc,
     "asin":asin,
     "imageurl": sample.get('imageURL', None),
     "imageURLHighRes": sample.get('imageURLHighRes', None)
    }


def extract():
    cats_desired = ['Men Clothing','Women Clothing', 'Boys Clothing','Girls Clothing',
'Men Shoes', 'Women Shoes', 'Boys Shoes','Girls Shoes',
'Men Watches', 'Women Watches', 'Boys Watches','Girls Watches']
    for i in cats_desired:
        dags = os.path.join(os.getcwd(), 'dags')
        resources = os.path.join(dags, 'resources')
        input_file_path = os.path.join(resources, 'meta_Clothing_Shoes_and_Jewelry.json.gz')
        sub_cats = defaultdict(int)
        output = []
        k=0
        dics = defaultdict(int)
        for sample in parse(input_file_path):
            info = fetch_category(sample)
            if len(info)>=3:
                cat = info[1]+ " "+ info[2]            
                if cat == i and sub_cats[cat]<500:  
                    dic=fetch_req_fields(sample)
                    dic["category"] = cat
                    if dic['features'] != "" and dic['description'] != "" and dic['imageurl']:
                        sub_cats[cat]+=1
                        output.append(dic) 

            k+=1        
        dataset = pd.DataFrame(output)
        
        op_file_path = os.path.join(resources, f"{i.lower().replace(' ','_')}_data.csv")

        dataset.to_csv(op_file_path, index=False)
                    