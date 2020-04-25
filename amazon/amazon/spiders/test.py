import json
import pandas as pd

with open('/home/vladislav/GitHub/laptops_scrapy/amazon/amazon/spiders/test2.json', 'r') as f:
    dicts = json.load(f)

params = []
values = []

for i, j in zip(dicts[0]['parameter'], dicts[1]['values']):
    params.append(i.strip())
    values.append(j.strip())

df = pd.DataFrame(values, params)

print(dicts)

# print(df['parameter'].str.strip())

# for i in dicts[0]['parameter']:
#     kd.append(i.strip())

# print(kd)
# print(len(df))

# to_drop = ["/electronics-store/b?ie=UTF8&node=172282",
#            "/computer-pc-hardware-accessories-add-ons/b?ie=UTF8&node=541966",
#            "/Computers-Tablets/b?ie=UTF8&node=13896617011"]

# for link in to_drop:
#     df = df.drop(df[df.link == link].index)   

# df = df[~df['link'].str.startswith('https://')]

# df = df.drop_duplicates()

# # print(len(df))


# url = 'https//gamno'

# testing = df.iloc[0:5]

# allow_urls = [url + str(i) for i in testing.link.values]

# print(allow_urls)