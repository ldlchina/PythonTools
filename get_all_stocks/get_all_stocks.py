# Retrive stock ids and data from 'http://quote.eastmoney.com'.
import os
import sys
import urllib.request
import re

# Retrive all stock ids
def urlTolist(url):
    allCodeList = []
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    for item in code:
        if item[0] == '6' or item[0] == '3' or item[0] == '0':
            allCodeList.append(item)
    return allCodeList

# Retrive all stocks data
def main():
    stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'
    allCodelist = urlTolist(stock_CodeUrl)

    currentFilePath = os.path.realpath(__file__)
    dirPath = os.path.dirname(currentFilePath)
    dataDirPath = os.path.join(dirPath, 'data')
    if not os.path.exists(dataDirPath):
        os.mkdir(dataDirPath)

    szStockIdsFilePath = os.path.join(dataDirPath, 'sz_stock_ids.xlsx')
    stocksDirPath = os.path.join(dataDirPath, 'stocks')
    if not os.path.exists(stocksDirPath):
        os.mkdir(stocksDirPath)

    url = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1110&tab1PAGENO=1&ENCODE=1&TABKEY=tab1'
    urllib.request.urlretrieve(url, szStockIdsFilePath)

    for code in allCodelist:
        print('Retriving data of %s...' % code)
        if code[0] == '6':
            url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code +\
                '&end=20180413&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        else:
            url = 'http://quotes.money.163.com/service/chddata.html?code=1'+code +\
                '&end=20180413&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        urllib.request.urlretrieve(url, os.path.join(stocksDirPath, code +'.csv'))

main()
