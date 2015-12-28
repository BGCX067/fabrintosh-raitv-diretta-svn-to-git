#####################################################################################
#
# License GNU GPLv2
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
####################################################################################


import urllib,urllib2,re,xbmcplugin,xbmcgui
import socket
import gzip
try:
    import io
except:
    import cStringIO 

import subprocess
import base64, random
try:
    import http.client as httpclient
except:
    import httplib as httpclient

__scriptname__ = "XBMC Video Plugin"
__author__ = 'fabrintosh [http://fabrintosh.blogspot.com]'
__date__ = '06-04-2010'
__version__ = "r003"

#palinsesto
#http://www.rai.tv/dl/portale/html/palinsesti/static/palinsestoOraInOnda.html 

#TV DASH - by You 2008.
#based on rai.sh (http://flavio.tordini.org/dirette-raitv-senza-silverlight-o-moonlight) source in https://launchpad.net/~olrait
#modificato per python 2.4 incorporato in XBMC 9.11 per mac os x e per python 2.6 in ubuntu


agent	= "Mozilla/5.0 (X11; U; Linux x86_64; it; rv:1.9.1.7) Gecko/20100106 Ubuntu/9.10 (karmic) Firefox/3.6"

def CATEGORIES():
		addDir('Rai1','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=983',2,'http://www.rai.it/dl/images/1233832365974RaiUno_02.png')
		addDir('Rai2','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=984',2,'http://www.rai.it/dl/images/1233832404832RaiDue02.png')
		addDir('Rai3','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=986',2,'http://www.rai.it/dl/images/1233832447578RaiTre_02.png')
		addDir('Rai4','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=75708',2,'http://www.rai.it/dl/images/124949355986510090805-3.jpg')
		addDir('RaiNews24','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=1',2,'http://www.rai.it/dl/images/1233841893415RaiNews24_02.png')
		addDir('RaiSport+','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=4145',2,'http://www.rai.it/dl/images/1233856927849raisport_.png')
		addDir('RaiStoria','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=24269',2,'http://www.rai.it/dl/images/1233857018728raistoria.png')
		addDir('RaiEdu','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=24268',2,'http://www.rai.it/dl/images/1233837355373RaiEdu1_02.png')
		addDir('RaiSat Extra','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=72926',2,'http://videowall.rainet.it/png/Raisat%20Extra.png')
		addDir('RaiSat Premium','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=72383',2,'http://videowall.rainet.it/png/Raisat%20Premium.png')
		addDir('RaiSat Cinema','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=72381',2,'http://videowall.rainet.it/png/Raisat%20Cinema.png')
		addDir('RaiSat YoYo','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=72384',2,'http://videowall.rainet.it/png/Raisat%20YoYo.png')
		addDir('RaiSat Gulp','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=4119',2,'http://videowall.rainet.it/png/Raisat%20Gulp.png')
		addDir('Rai International','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=87578',2,'http://www.italiani.lu/mmp/online/website/menu_left/notices/92/490/image_16912/rai_international.jpg')
		addDir('EuroNews','http://mediapolis.rai.it/relinker/relinkerServlet.htm?cont=113784',2,'http://www.menassat.com/files/images/euronews_1.jpg')
         
def INDEX(url):
	req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('').findall(link)
        for thumbnail,url,name in match:
        	addDir(name,url,2,thumbnail)

def VIDEOLINKS(url,name):
	re_url	= "^http://(?P<host>[a-zA-Z0-9]*\.([a-zA-Z0-9]*\.)+[a-zA-Z0-9]*)(?P<path>/[\w\-\+\~\%\#\.\/]*)\?cont\=(?P<chanid>\w*)"
	match_url = re.match(re_url, url).groupdict()
	host = match_url["host"] 
	path = match_url["path"]
	chan = match_url["chanid"]
 
	re_date = "^(?P<day>\d*)-(?P<month>\d*)-(?P<year>\d*)\s(?P<hour>\d*):(?P<minutes>\d*):(?P<seconds>\d*)"
	match_date = re.match(re_date, raiDate()).groupdict()
        print match_date
	day	= match_date["day"]
	month	= match_date["month"]
	year	= match_date["year"]
	hour	= match_date["hour"]
	minutes	= match_date["minutes"]
	seconds	= match_date["seconds"]
 
	rnd1 = str(random.randint(0, 1234))
	rnd2 = str(random.randint(0, 1234))
 
	token = year+";"+chan+";"+day+"-"+month+"-"+"528"+"-"+hour+"-"+minutes+"-"+seconds+"-"+"565"
	ttAuth = encode3(encode2(encode1(token)))
	url = urlURL(host, path, chan, ttAuth)

        addLink('Riproduci',url,'')
        #per un futura programmazione
        #addLink('Riproduci',url,'','Melrose Place VII Sospetto Ep. 7', "1:00")

                
def urlURL(host, path, chan, ttAuth):
	asx_connection = httpclient.HTTPConnection(host)
	asx_connection.putrequest("POST", path+"?cont="+chan)
	asx_connection.putheader("User-Agent", agent)
	asx_connection.putheader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	asx_connection.putheader("Accept-Language", "it-it,it;q=0.8,en-us;q=0.5,en;q=0.3")
	asx_connection.putheader("Accept-Encoding", "gzip,deflate")
	asx_connection.putheader("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.7")
	asx_connection.putheader("Connection", "keep-alive")
	asx_connection.putheader("Keep-Alive", "115")
	asx_connection.putheader("viaurl", "www.rai.tv")
	asx_connection.putheader("ttAuth", ttAuth)
	asx_connection.putheader("Content-Length", "0")
	asx_connection.endheaders()
	asx_response = asx_connection.getresponse().read()
	asx_connection.close()
	try: ###niente bytes su python 2.5
		asx = bytes.decode(asx_response)
	except:
		asx = str.decode(asx_response)
	#asx = str.decode(asx_response)
	return re.search("(?P<mms>mms://.*)\"", asx).groupdict()["mms"]
 
def raiDate():
	date_connection = httpclient.HTTPConnection("videowall.rai.it")
	date_connection.putrequest("GET", "/cgi-bin/date")
	date_connection.putheader("User-Agent", agent)
	date_connection.putheader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	date_connection.putheader("Accept-Language", "it-it,it;q=0.8,en-us;q=0.5,en;q=0.3")
	date_connection.putheader("Accept-Encoding", "gzip,deflate")
	date_connection.putheader("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.7")
	date_connection.putheader("Connection", "keep-alive")
	date_connection.putheader("Keep-Alive", "115")
	date_connection.endheaders()
	date_response = date_connection.getresponse().read()
	date_connection.close();
	try: ###niente bytes su python 2.5
		return bytes.decode(date_response[:len(date_response)-1])
	except:
		return str.decode(date_response[:len(date_response)-1])

	#return str.decode(date_response[:len(date_response)-1])
def encode1(token):
	encoded = ""
 
	for ch in token:
		encoded += chr(ord(ch)^1)
	print(encoded+";1")
	return encoded+";1"
 
def encode2(token, key="hMrxuE2T8V0WRW0VmHaKMoFwy1XRc+hK7eBX2tTLVTw="):
	i = len(token)-1
	j = 0
	encoded = ""
	while i>=0:
		enc = chr(ord(token[i]) ^ ord(key[j]))
		encoded = enc + encoded
		i = i-1 
		j = j+1
	#print(encoded)
	return encoded
 
def encode3(token):
	return base64.encodestring(str.encode(token)).decode()
 
                
def get_params():
	param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
        	params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                	params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                	splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                        	param[splitparams[0]]=splitparams[1]
                                
        return param


def addLink(name,url,iconimage):
#def addLink(name,url,iconimage, titolo, time):
        #tentativo di inserire la programmazione
        #liz=xbmcgui.ListItem('Melrose Place VII Sospetto Ep. 7', iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        #liz.setInfo( type="Video", infoLabels={ "Title": titolo } )
        #liz.setInfo( type="Video", infoLabels={ "genre": "Commedia" } )
        #liz.setInfo( type="Video", infoLabels={ "duration": "1:00" } )
	ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


params=get_params()
url=None
name=None
mode=None

#non mi sembra serva a qualcosa....
timeout = 120
socket.setdefaulttimeout(timeout)

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
	print ""
        CATEGORIES()
       
elif mode==1:
	print ""+url
        INDEX(url)

elif mode==2:
	print ""+url
        VIDEOLINKS(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
