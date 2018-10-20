#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
James
"""

import pymongo
import xlwt

class MongodbToExcel(object):
    def __init__(self):
        # 本地mongodb
        connection = pymongo.MongoClient('mongodb://localhost:27017')
        db = connection['data']
        self.collection = db['info_zyw_zl']
        self.total = 0
        self.row = 0
        self.col = 0
        self.rb = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.rb.add_sheet(u'足疗', cell_overwrite_ok=True)
        # self.path = r"E:/GMWork/01 Project/corpus/storage_data/jianfei.xls"
        # self.path = r"E:/GMWork/01 Project/corpus/storage_data/meirong.xls"
        self.path = r"E:/GMWork/01 Project/corpus/storage_data/足疗.xls"
        self.getMongodb()


    def getMongodb(self):
        resultsCount = self.collection.count()
        # for skipNum in range(0, resultsCount, 200):
        for skipNum in range(0, resultsCount, 20):
            results = self.collection.find().skip(skipNum).limit(20)
            print(skipNum)
            for result in results:
                # if result['answer'] != '' and len(result['answer']) != 0:
                #     if len(result['question']['askText']) > 5 and len(result['question']['askText']) < 11:
                #         if len(result['answer'][0]) < 25:
                            self.saveExcel(result)


    def saveExcel(self, item):
        self.sheet.write(self.row, 0, item['title'])
        self.sheet.write(self.row, 1, item['content'])
        self.rb.save(self.path)
        self.row += 1
        self.total += 1
        print(self.total)


if __name__ == '__main__':
    try:
        MongodbToExcel()
    except Exception as e:
        print(str(e))
