import re
import time
from bs4 import BeautifulSoup

test_list = ["1小时10分钟","1小时1分钟","10小时1分钟","10小时10分钟","15分钟22秒","1分钟","10分钟","1秒","10秒"]


#获取视频页面剩余时间
def get_sleeptime(page):

	soup=BeautifulSoup(page,"html.parser")
	element = soup.find(id="spanLeavTimes")
	string = element.text
	return translate(string)
		



def translate(string):
	if "小时" in string:
		sleeptime = re.findall("(.*?)小时(.*?)分钟",string)
		#print(sleeptime)
		return int(sleeptime[0][0])*3600+int(sleeptime[0][1])*60+60 #外加60秒防止提前跳出
	elif "小时" not in string and "分钟" in string and "秒" in string:
	    sleeptime = re.findall("(.*?)分钟(.*?)秒",string)
	    #print(sleeptime)
	    return int(sleeptime[0][0])*60+int(sleeptime[0][1])
	elif "分钟" in string and "秒" not in string:
	    sleeptime = re.findall("(.*?)分钟",string)
	    #print(sleeptime)
	    return int(sleeptime[0])*60
	elif "秒" in string and "分钟" not in string:
	    sleeptime = re.findall("(.*?)秒",string)
	    #print(sleeptime)
	    return int(sleeptime[0])

	











