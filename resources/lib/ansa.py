import sys
import urllib
import urllib2
import httplib
import time
from xml.dom import minidom
from xml.parsers import expat

class Ansa:
    __BASEURL = "http://www.ansa.it"

    def getChannels(self):
        url = "http://www.ansa.it/web/video/videohp_video_channels.xml"
        xmldata = urllib2.urlopen(url).read()
        dom = minidom.parseString(xmldata)

        channels = []
        for node in dom.getElementsByTagName('c'):
            channel = {}
            channel["title"] = node.attributes["name"].value
            channel["url"] = self.__BASEURL + node.attributes["index"].value
            channels.append(channel)
       
        return channels

    def getVideoByChannel(self, url):
        xmldata = urllib2.urlopen(url).read()
        dom = minidom.parseString(xmldata)

        videos = []
        for videoNode in dom.getElementsByTagName('n'):
            video = {}
            videoFlv = videoNode.getElementsByTagName('video')[0].childNodes[0].data
            videoId = self.getVideoId(videoFlv)
            pageUrl = self.__BASEURL + videoNode.getElementsByTagName('url')[0].childNodes[0].data
            titleNode = videoNode.getElementsByTagName('titolo')[0]
            if titleNode.childNodes.length > 0:
                video["title"] = titleNode.childNodes[0].data
            else:
                video["title"] = ""
            video["channel"] = videoNode.getElementsByTagName('categoria')[0].childNodes[0].data
            dateTime = videoNode.getElementsByTagName('dataora')[0].childNodes[0].data
            if url == "http://www.ansa.it/web/elementiHP/hp_video_index.xml":
                video["date"] = time.strptime(dateTime, "%d-%m-%Y %H:%M")
            else:
                video["date"] = time.strptime(dateTime, "%Y-%m-%d %H:%M")
            thumbUrl = self.__BASEURL + videoNode.getElementsByTagName('fotoMed')[0].childNodes[0].data
            video["thumb"] = self.getThumbURL(thumbUrl)
            video["url"] = self.getVideoURL(videoId, pageUrl)
            videos.append(video)
            
        return videos
        
    def getVideoId(self, videoFlv):
        videoId = videoFlv[:videoFlv.find(".flv")]
        return videoId

    def getVideoURL(self, videoId, pageUrl):
        url = "rtmp://play.ansa.it/vod/ playpath=%s tcUrl=rtmp://play.ansa.it/vod/ app=vod/ swfUrl=https://www.ansa.it/web/video/0110203050_videopanel.swf pageUrl=%s" % (videoId, pageUrl)
        return url

    def getThumbURL(self, thumbUrl):
        thumbUrl = thumbUrl.replace("/hp_300/", "/hp_340/")
        return thumbUrl
