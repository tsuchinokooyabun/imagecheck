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


class ImageCheck:

    def __init__(self, input_str):
        self.input_str=input_str

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
                print json.dumps(self.jsonData, sort_keys=True, indent=4)

                for self.list in self.jsonData['detect']:
                    cv2.rectangle(self.img,(self.list['right'],self.list['top']),(self.list['left'],self.list['bottom']),(0,255,0),3)
                    cv2.putText(self.img,self.list['class'],(self.list['left'],self.list['top']-10),cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255),2)

                self.dirname = "static/images/"
                if not os.path.exists(self.dirname):
                    os.makedirs(self.dirname)
                self.detectimage = "detect-"+self.filename
                cv2.imwrite(os.path.join(self.dirname, self.detectimage), self.img)
                return os.path.join(self.dirname, self.detectimage), json.dumps(self.jsonData, sort_keys=True, indent=4)

            except Exception as e:
                return False,False

        if returnFilehandleFromInputStr():
            returnFilehandleFromInputStr().close()

if __name__ == "__main__":
    #ch = ImageCheck(sys.argv[1])
    #ch.goCheck()
    ImageCheck(sys.argv[1]).goCheck()
