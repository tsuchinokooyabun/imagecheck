#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import json
import urllib2
import os
import urllib
import sys
import StringIO
import peewee
import datetime
import ccdb

class ImageCheck:

    def __init__(self, input_str, model):
        self.input_str=input_str
        self.model=model

    def returnFilehandleFromInputStr(self):
        if "http" in self.input_str:
            self.urls = StringIO.StringIO(self.input_str)
        else:
            if __name__ == '__main__':
                self.urls = open(self.input_str)
            else:
                self.urls = StringIO.StringIO(self.input_str)
        return self.urls

    def returnDownloadImageCV2(self):
        self.resp = urllib.urlopen(self.url)
        self.image = np.asarray(bytearray(self.resp.read()), dtype="uint8")
        self.image = cv2.imdecode(self.image, cv2.IMREAD_COLOR)
        return self.image

    def goCheck(self):
        for self.url in self.returnFilehandleFromInputStr():
            self.filename = self.url.split("/")[-1]
            print "downloading %s" % (self.url)
            try:
                self.img = self.returnDownloadImageCV2()

                self.aurl = 'http://104.199.154.201:5000/api/maria?url='+str(self.url)

                self.r = urllib2.urlopen(self.aurl)
                self.jsonData = json.loads(self.r.read())
                self.r.close()
                self.jdump = json.dumps(self.jsonData, sort_keys=True, indent=4)
                #print self.jdump
                #print self.jsonData
                self.count=0
                self.prob=[]
                for self.list in self.jsonData['detect']:
                    cv2.rectangle(self.img,(self.list['right'],self.list['top']),(self.list['left'],self.list['bottom']),(0,255,0),3)
                    cv2.putText(self.img,self.list['class'],(self.list['left'],self.list['top']-10),cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255),2)
                    self.count+=1
                    self.prob.append(self.list['prob'])
                if self.prob:
                    self.mx = max(self.prob)
                else:
                    self.mx = 0
                self.dirname = "static/images/"
                if not os.path.exists(self.dirname):
                    os.makedirs(self.dirname)
                self.detectimage = "detect-"+self.filename
                self.predict_url = os.path.join(self.dirname, self.detectimage)

                print "prob max is "+str(self.mx)
                #print "predict url is %s" % self.predict_url
                #print "input url is %s" % self.url
                self.jsonData2 = self.jsonData
                #self.jsonData2['predict_url']=self.predict_url
                #self.jsonData2['predict_date']=str(datetime.datetime.today())
                self.jsonData2['prob_max']=self.mx
                self.jsonData2['breast_count']=self.count
                self.jdump2 = json.dumps(self.jsonData2, sort_keys=True, indent=4)
                print self.jdump2
                if "messege" not in self.jdump2:
                    if cv2.imwrite(self.predict_url, self.img):
                        i = ccdb.InsertDB(self.url, self.predict_url, self.jdump2, self.model)
                        i.insertData()
                return os.path.join(self.dirname, self.detectimage), json.dumps(self.jsonData2, sort_keys=True, indent=4), self.url
            except Exception as e:
                return False,False,False

        if self.returnFilehandleFromInputStr():
            self.returnFilehandleFromInputStr().close()

if __name__ == "__main__":
    ImageCheck(sys.argv[1],sys.argv[2]).goCheck()
    for p in ccdb.PredictDb.select():
        print p.result, p.input_url, p.predict_url, p.model, p.predict_date

#def viewList():
#for p in ccdb.PredictDb.select():
#    print p.result, p.input_url, p.predict_url, p.model, p.predict_date
