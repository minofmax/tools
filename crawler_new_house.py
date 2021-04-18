import json
import random
import re
import time
from typing import List

import requests
import xlwt as xlwt
from bs4 import BeautifulSoup as bs, Tag
from xlwt import Worksheet

INFO_TEMPLATE = {
    '楼盘': {
        '楼盘名': '',
        '楼盘简介': ''
    },
    '周边设施': {
        '交通': '',
        '幼儿园': '',
        '中小学': '',
        '大学': '',
        '综合商场': '',
        '医院': '',
        '银行/ATM': '',
        '邮局/快递': '',
        '其他': ''
    },
    '基本信息': {
        '价格': '',
        '物业类别': '',
        '项目特色': '',
        '建筑类别': '',
        '装修状况': '',
        '产权年限': '',
        '开发商': '',
        '楼盘地址': '',
        '销售状态': '',
        '开盘时间': '',
        '交房时间': '',
        '售楼地址': '',
        '咨询电话': '',
        '主力户型': '',
        '预售许可证': '',
        '占地面积': '',
        '建筑面积': '',
        '容积率': '',
        '绿化率': '',
        '停车位': '',
        '楼栋总数': '',
        '总户数': '',
        '物业公司': '',
        '物业费': '',
        '物业费描述': '',
        '楼层状况': '',
    },
    '销售信息': {
        '销售状态': '',
        '开盘时间': '',
        '交房时间': '',
        '售楼地址': '',
        '咨询电话': '',
        '主力户型': '',
        '预售许可证': ''
    },
    '小区规划': {
        '占地面积': '',
        '建筑面积': '',
        '容积率': '',
        '绿化率': '',
        '停车位': '',
        '楼栋总数': '',
        '总户数': '',
        '物业公司': '',
        '物业费': '',
        '物业费描述': '',
        '楼层状况': ''
    }
}

PROXY_LIST = ["218.91.13.2:46332",
              "121.31.176.85:8123",
              "218.71.161.56:80",
              "49.85.1.230:28643",
              "115.221.121.165:41674",
              "123.55.177.237:808"
              ]

USER_AGENT = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]


def parse_html(html: str) -> dict:
    soup = bs(html, features='lxml')
    title = soup.find('a', {'id': 'huxinxq_E02_15'}).text
    items: List[Tag] = soup.find_all('div', {'class': 'main-item'})
    info_dict = INFO_TEMPLATE.copy()
    info_dict['楼盘']['楼盘名'] = title
    for item in items:
        part_title = item.find('h3').text
        if part_title == '项目简介':
            description = item.find('p').text
            info_dict['楼盘']['楼盘简介'] = description
            continue
        if part_title == '价格信息':
            # 价格信息是个表，数据太复杂，并且冗余，不做处理
            continue
        if part_title == '周边设施':
            li_tags = item.find_all('li')
            for li in li_tags:
                sub_title = li.find('span').text.replace('：', '')
                description = li.text
                info_dict[part_title][sub_title] = description
            continue
        if part_title == '基本信息':
            price_info = item.find('div', {'class': 'main-info-price'}).text.replace('\n', '').replace(' ', '')
            info_dict[part_title]['价格'] = price_info
        li_list: List[Tag] = item.find_all('li')
        for info in li_list:
            sub_info = info.find('div', {'class': re.compile(r'list-left.*')})
            if not sub_info:
                continue
            sub_title = sub_info.text.replace('\n', '').replace(' ', '').replace('：', '')
            sub_info = info.find('div', {'class': re.compile(r'list-right.*')})
            if not sub_info:
                value = ''
            else:
                value = sub_info.text.replace('\n', '').replace(' ', '')
            info_dict[part_title][sub_title] = value
    return info_dict


def write_csv(buildings_data: List[dict], name_prefix, path: str):
    # 构造表格
    f = xlwt.Workbook()
    sheet: Worksheet = f.add_sheet('buildings', cell_overwrite_ok=True)
    # 写入头部
    if len(buildings_data) < 1:
        raise Exception('未能爬取到有效数据')
    headers: list = list(INFO_TEMPLATE.keys())
    row1: dict = {header: list(INFO_TEMPLATE.get(header).keys()) for header in headers}
    prefix = 0
    for header in headers:
        suffix = prefix + len(row1.get(header)) - 1
        sheet.write_merge(0, 0, prefix, suffix, header)
        prefix = suffix + 1
    sub_headers = []
    [sub_headers.extend(v) for _, v in row1.items()]
    for i in range(len(sub_headers)):
        sheet.write(1, i, sub_headers[i])
    # 写入数据
    row_num = 2
    for data in buildings_data:
        prefix = 0
        for _, v in data.items():
            length = len(v)
            values = list(v.values())
            for i in range(length):
                sheet.write(row_num, i + prefix, values[i])
            prefix += length
        row_num += 1
    f.save(path + name_prefix + '_buildings.xlsx')


def get_id(city):
    url = 'https://' + city + '.newhouse.fang.com/house/s/b91'
    user_agent = random.choice(USER_AGENT)
    header = {'User-Agent': user_agent}
    proxy = {'Proxies': random.choice(PROXY_LIST)}
    r = requests.get(url, headers=header, proxy=proxy)
    r.encoding = 'GBK'
    pattern1 = re.compile(r'(?<=现有新楼盘)\d+')
    total = int(re.findall(pattern1, r.text)[0]) // 20 + 1
    result = []
    for i in range(1, total + 1):
        url = 'https://' + city + '.newhouse.fang.com/house/s/b9' + str(i)
        user_agent = random.choice(USER_AGENT)
        header = {'User-Agent': user_agent}
        r = requests.get(url, headers=header)
        time.sleep(2)
        r.encoding = 'gb2312'
        pattern = re.compile(r'(?<=loupan/)\d+')
        data_ids = re.findall(pattern, r.text)
        '''
        TODO: 因为数据庞大，就默认选择爬前100，这个可以修改或者直接注释，同步爬取会比较慢，并行爬取可能会被封 
        '''
        if len(result) >= 100:
            break
        for data_id in data_ids:
            result.append(data_id)
    return result


def get_data(city, id) -> dict:
    url = 'https://' + city + '.newhouse.fang.com/loupan/' + id + '/housedetail.htm'
    user_agent = random.choice(USER_AGENT)
    header = {'User-Agent': user_agent}
    proxy = {'Proxies': random.choice(PROXY_LIST)}
    r = requests.get(url, headers=header, proxy=proxy)
    time.sleep(1)
    r.encoding = 'utf8'
    return parse_html(r.text)


def write_txt(data_list: List[dict], path: str):
    with open(path, 'a+', encoding='utf8') as f:
        for data in data_list:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    '''
    主要是针对某房产中介网站的数据进行爬取，
    新楼盘：地址、开盘价、周边的设施如学校，医院等做了爬取
    最后会输出成一个表格
    '''
    # 城市的首字母，作为city参数传入
    city = 'bj'
    ids = get_id(city)
    info_list: List[dict] = []
    for building_id in ids:
        try:
            # 没有用协程的原因是对应网站对于爬取速度的限制有点迷，所以为了避免触发反爬，就用单线程
            data = get_data(city, building_id)
        except Exception as e:
            continue
        info_list.append(data)
    save_path = '/data/app/'
    write_csv(info_list, city, save_path)
