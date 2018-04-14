# Retrive stock codes and data from 'http://quote.eastmoney.com'.
import os
import sys
import urllib.request
import re

# Retrive all stock codes


def getAllStockCodes(url):
    allCodes = []
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    for item in code:
        if item[0] == '6' or item[0] == '3' or item[0] == '0':
            allCodes.append(item)
    return allCodes

# Retrive all stock data


def getAllStockData(date):
    stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'
    allCodes = getAllStockCodes(stock_CodeUrl)

    currentFilePath = os.path.realpath(__file__)
    dirPath = os.path.dirname(currentFilePath)
    dataDirPath = os.path.join(dirPath, 'data')
    if not os.path.exists(dataDirPath):
        os.mkdir(dataDirPath)

    # http://www.sse.com.cn/assortment/stock/list/share/
    # http://www.szse.cn/main/marketdata/jypz/colist/
    shStockIdsFilePath = os.path.join(dataDirPath, 'sh_stock_ids.xls')
    szStockIdsFilePath = os.path.join(dataDirPath, 'sz_stock_ids.xlsx')

    stocksDirPath = os.path.join(dataDirPath, 'stocks')
    if not os.path.exists(stocksDirPath):
        os.mkdir(stocksDirPath)

    url = 'http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1'
    # https://www.cnblogs.com/majianguo/p/8186429.html
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ("Referer", "http://www.sse.com.cn/assortment/stock/list/share/")
    ]
    originalOpener = urllib.request._opener
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, shStockIdsFilePath)
    urllib.request.install_opener(originalOpener)

    url = 'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1110&tab1PAGENO=1&ENCODE=1&TABKEY=tab1'
    urllib.request.urlretrieve(url, szStockIdsFilePath)

    for code in allCodes:
        print('Retriving data of %s...' % code)
        if code[0] == '6':
            url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code +\
                '&end=' + date + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        else:
            url = 'http://quotes.money.163.com/service/chddata.html?code=1'+code +\
                '&end=' + date + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        urllib.request.urlretrieve(
            url, os.path.join(stocksDirPath, code + '.csv'))


if __name__ == '__main__':
    getAllStockData('20180413')
