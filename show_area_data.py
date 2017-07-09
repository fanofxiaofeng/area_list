#!/usr/local/bin/python3

import os
import bs4
import sys
import pprint
import html2text
import os.path

class country:
    def __init__(self, name, area):
        self.name = name
        self.area = area

def check():
    files = ['css/stylesheet.css', 'template.html', 'area_list.html']
    for file in files:
        if not os.path.exists(file):
            return False
    return True

def get_data(source_file_name):
    '''
    从 source_file_name 对应的文件里解析出各个国家(地区)的 rank, name, area 信息并返回
    '''
    soup = bs4.BeautifulSoup(open(source_file_name), 'html.parser')

    table = soup.table
    trlist = table.select('tr')
    cnt = 0
    countrylist = []
    for tr in trlist:
        cnt += 1
        # skip th in table
        if cnt == 1:
            continue
        tdlist = tr.select('td')

        # 获取 rank 的数据
        rank = tdlist[0].contents[-1]
        if '–' in rank:
            continue
        rank = int(rank)

        # 获取 name
        name = tdlist[1].a.get_text()

        # 获取 area 的数据
        area = tdlist[2].contents[1].replace(',', '')

        countrylist.append(country(name, area))

    return countrylist


def show_data(template_file_name, countrylist, output_html_file, output_md_file):
    '''
    将 countrylist 中保存的各个国家(地区) 的 rank, name, area 信息输出至
    output_html_file, output_md_file 所对应的文件中
    '''
    soup = bs4.BeautifulSoup(open(template_file_name), 'html.parser')

    table = soup.new_tag('table')

    # 处理表头
    tr = bs4.BeautifulSoup('''
    <tr>
        <th>Rank</th>
        <th>Sovereign state/dependency</th>
        <th>Total area</th>
    </tr>''', 'html.parser')
    table.append(tr)

    cnt = 0
    for country in countrylist:
        cnt += 1
        tr = bs4.BeautifulSoup('''
        <tr>
            <td class="rank">#{}</td>
            <td>{}</td>
            <td class="area">{}</td>
        </tr>
        '''.format(cnt, country.name, country.area), 'html.parser')
        table.append(tr)
    soup.body.append(table)
    content = soup.prettify()

    with open(output_html_file, 'w') as f:
        f.write(content)

    with open(output_md_file, 'w') as f:
        f.write(html2text.html2text(content))

if not check():
    print("Please check...")
    sys.exit()
countrylist = get_data('area.html')
show_data('template.html', countrylist, 'result.html', 'result.md')
