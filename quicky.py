#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os, datetime, re, json
from py_mini_racer import py_mini_racer

from bs4 import BeautifulSoup
import urllib
import ssl
context = ssl._create_unverified_context()
import sys

soup = BeautifulSoup
csv_file = 'Quicksell_' + str(datetime.datetime.today().date()) + '.csv'
ctx = py_mini_racer.MiniRacer()




def quicksell():
    # url = 'https://quicksell.co/s/tbc-wholesale/tbc-wholesale-complete-product-list/lnt'
    url = 'https://quicksell.co/s/tbc-wholesale/below-cost-sale---2019/qrf'
    headers = {'accept-encoding': 'gzip, deflate, br'}
    resp = requests.get(url, headers=headers)
    # print(resp)
    html = soup(resp.text, 'html.parser')
    return html


def json_data(resp_data):

    products = resp_data.find("meta", {"name":"amalgam"})['content'].strip()
    # .text.strip()
    
    #print(products)
    #exit()
    #trim_data = products.replace('<script type="text/javascript">', "").replace('window.amalgamObject = ', '').replace('</script>', '')
    #f= open("guru99.txt","w+")
    #f.write(json.dumps((ctx.eval(trim_data))))
    #f.close()
    #print()
    #exit()
    #json_data = json.loads((ctx.eval(trim_data)))
    json_data = json.loads(products)
    # f= open("tbc.json","w+")
    # f.write(json_data)
    # f.close()
    # print("File written as tbc.json")
    # exit()
    # product_list = json_data['catalogue']['productList']
    # product_tags = json_data['productTags']
    # data = {'product_list': product_list, 'product_tags': product_tags}
    return json_data


def get_products(json_data):
    # print(json_data)
    #json_data = json_data
    uspid = json_data['catalogue']['productList']
    sortedpid = sorted(uspid.items(), key=lambda x: x[1], reverse=False)
    # for id in sortedpid:
    #    print(id[0])

    for sid in sortedpid:
        pid = sid[0]
        # pid = pid[0]
        #print(pid)

        product = json_data[pid]
        #print(json_data)
        # sys.exit()
        if 'tags' in product:
            product_tag = product['tags']
            sizes = extract_size(product_tag)
        else:
            sizes = ['no size']
        product_name = product['name'].replace(',', '').replace('\n', '').replace('/', '')
        product_des = product['description']
        product_price = str(product['price'])
        product_pics = get_pics(product['pictures'])
        for different_size in sizes:
            different_size = different_size.split("°")[0]+"."+different_size.split("°")[1] if "°" in different_size else different_size
            product = {'pid': pid.replace('-', ''), 'product_name': product_name.replace(',', ''), 'sizes': different_size,
                       'product_price': product_price,
                       'product_des': product_des.replace('\n', '').replace(',', ''), 'product_pics': product_pics}

            write_product_csv(product, product_price)
        saveimages(product)


def saveimages(product):
    if not os.path.exists('productsImages/{} {}/'.format(product.get('name'), product.get('pid'))):
        imgnam = 0
        # print(product)
        # exit()
        for key in product['product_pics']:
            picture = key
            print(picture, imgnam)
            resp = get_image(picture)
            # print(product)
            # exit()
            if not os.path.exists('productsImages/' + str(product.get('product_name')) + " " + product.get('pid') + '/'):
                os.makedirs('productsImages/' + str(product.get('product_name')) + " " + product.get('pid') + '/')
            print(imgnam)
            imagefile = str(imgnam)+'.jpg'
            output = open('productsImages/' + str(product.get('product_name')) + " " + product.get('pid') + '/' + imagefile,
                          'wb')
            output.write(resp.read())
            output.close()
            imgnam = imgnam + 1


def get_image(image_url):
    resource = urllib.request.urlopen(image_url, context=context)
    return resource


def get_pics(data):
    pics = []
    for i in data:
        pic = data[i]['url']
        pics.append(pic)
    return pics


def extract_size(product_tag):
    sizes = []
    for size in product_tag.keys():
        sizes.append(size.replace(" ",""))
    return sizes


def write_product_csv(product, product_price):
    data_write = open(csv_file, 'a', encoding='utf-8')
    price = product['product_price']
    print(price)
    p_data = []
    for data in product:
        exdata = product[data]
        p_data.append(exdata)
    print(p_data[0], p_data[1])
    data_write.write(
        str(p_data[0]) + "," +
        str(p_data[1]) + "," +
        str(p_data[2]) + "," +
        str(p_data[3]) + "," +
        str(p_data[4]) + ",\n"
    )
    data_write.close()


def main():
    resp_data = quicksell()
    JsonData = json_data(resp_data)
    products = get_products(JsonData)


if __name__ == '__main__':
    main()