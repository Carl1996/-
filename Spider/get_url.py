from bs4 import BeautifulSoup
import re

#page_path:爱学堂目录网页
#从目录页获取Url
def from_page_get_url(page_path):

	# with open(page_path,"r",encoding="utf-8")as f:
	# 	page=f.read()

	soup=BeautifulSoup(page_path,"html.parser")

	list_finished=[]
	list_not_finished=[]
	list_all=[]

	for i in soup.find_all("li"):
		for l in i.find_all(attrs={"data-localize": "sty_lbl_usercomplete"}):
			if l.string:
				for j in i.find_all("div",class_="el-placehold el-placehold-default"):
					for k in j.find_all("img"):
						list_finished.append(re.findall("(/.*?)\'",str(k))[0])

		for j in i.find_all("div",class_="el-placehold el-placehold-default"):
			for k in j.find_all("img"):
				list_all.append(re.findall("(/.*?)\'",str(k))[0])

	for i in list_all:
		if i not in list_finished:
			list_not_finished.append("http://luxshare-ict.yunxuetang.cn"+i)
			
	return list_not_finished

#从Package包获取Url
def get_package_url(page):
	list_url_all=[]
	list_url_finished=[]
	list_url_not_finished=[]

	soup = BeautifulSoup(page,"html.parser")

	comp = re.compile("(/.*?)\'")
	for k in soup.find_all("div",class_="normalrow clearfix"):
		for elment in k.find_all("a",class_="text-color6"):
			for elment2 in k.find_all("td",class_="fontnumber study-schedule"):
				if elment2.string != " 100%":
					data = elment.get("href")
					for url in re.findall(comp,data):
						list_url_all.append("http://luxshare-ict.yunxuetang.cn"+url)
					
	return list_url_all
