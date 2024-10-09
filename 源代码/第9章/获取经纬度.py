# _*_ coding:utf-8 _*_
import requests
import pandas as pd
import time
import json


class LngLat:
    # def __init__(self):
    #     self.headers = {
    #         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
    #     self.proxies = {
    #         "http": "http://61.135.217.7:80",
    #         "http": "http://118.190.95.43:9001",
    #         "http": "http://180.122.147.67:37153",
    #         "http": "http://118.190.95.35:9001",
    #         "http": "http://119.5.0.11:808",
    #         "http": "http://106.56.102.192:8070"
    #     }

    # 读取数据
    def read_data(self):
        file_path = open(r'C:\Users\admin\Desktop\链家北京租房数据_new.csv',encoding='utf-8')
        file_data = pd.read_csv(file_path)
        duplicate_removal = file_data.drop_duplicates()
        house_names = duplicate_removal['位置']
        house_names = house_names.tolist()
        return house_names

    def get_url(self):
        url_temp = "http://api.map.baidu.com/geocoder/v2/?address={}&output=json&ak=NnQokv12fkyf4YoG59j9fRbGq4G8Lb4K&callback=showLocation"
        # ak = 'NnQokv12fkyf4YoG59j9fRbGq4G8Lb4K'
        house_names = self.read_data()
        return [url_temp.format(i) for i in house_names]

    # 发送请求
    def parse_url(self, url):
        while 1:
            try:
                r = requests.get(url)
            except requests.exceptions.ConnectionError:
                time.sleep(2)
                continue
            return r.content.decode('utf-8')

    def run(self):
        li = []
        urls = self.get_url()
        for url in urls:
            data = self.parse_url(url)
            str = data.split("{")[-1].split("}")[0]
            try:
                lng = float(str.split(",")[0].split(":")[1])
                lat = float(str.split(",")[1].split(":")[1])
            except ValueError:
                continue
                # 构建字典
            dict_data = dict(lng=lng, lat=lat, count=1)
            li.append(dict_data)
        f = open(r'C:\Users\admin\Desktop\经纬度信息.txt', 'w')
        f.write(json.dumps(li))
        f.close()
        print('写入成功')

if __name__ == '__main__':
    execute = LngLat()
    execute.run()
