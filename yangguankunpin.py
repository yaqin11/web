#阳光宽频网http://www.365yg.com/
'''
首先向365yg.com发送请求
获取响应，解析响应，将里面所有的标题链接获取到
依次向每个标题链接发送请求
获取响应，解析响应，获取video标签的src属性
向src属性发送请求，获取响应，将内容保存到本地即可
'''
import requests
from lxml import etree
import json
import time
from selenium import webdriver

headers ={
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}
def handle_title(widen):
	#将捕获的接口得到
	#api/pc/feed/?max_behot_time=1528197881&category=video_new&utm_source=toutiao&widen=1&tadrequire=true&as=A1854BD1F608533&cp=5B16D825E323BE1&_signature=g4eNzwAA2J0KZrRVc9EFpoOHjd HTTP/
	url = 'http://www.365yg.com/api/pc/feed/?max_behot_time=1528200083&category=video_new&utm_source=toutiao&widen={}&tadrequire=true&as=A1D55B5186189B9&cp=5B16A8F94BB90E1&_signature=oP61JRAa-.cpH4y.oI8FF6D-tT'
	url = url.format(widen)
		# 发送请求
	r = requests.get(url=url, headers=headers)
	# 解析内容,因为返回的是json格式数据，直接解析json格式即可
	# 通过分析，要data里面的 title\source_url
	# 将json数据转化为python对象
	obj = json.loads(r.text)
	# 取出所有和视频相关的数据,data是一个列表，里面存放的都是字典
	data = obj['data']
	# 循环data列表，依次取出每一个视频信息
	for video_data in data:
		title = video_data['title']
		a_href = 'http://www.365yg.com' + video_data['source_url']

		# 发送请求。获取内容，解析内容，获取src
		handle_href(a_href, title)
def handle_href(a_href,title):
	# 通过phantomjs来进行解决，
	browser = webdriver.PhantomJS(r'F:\爬虫知识\day05\ziliao\phantomjs-2.1.1-windows\bin\phantomjs.exe')
	browser.get(a_href)
	time.sleep(3)
	print(a_href)
	# 获取源码，生成tree对象，然后查找video里面的src属性

	tree = etree.HTML(browser.page_source)
	with open('lala.html', 'w', encoding='utf8') as fp:
		fp.write(browser.page_source)
	exit()
	video_src = tree.xpath('//video/@src')[0]
	# print(video_src)
	filepath = 'shipin/' + title + '.mp4'
	print('%s开始下载......' % title)
	r = requests.get(video_src)
	with open(filepath, 'wb') as fp:
		fp.write(r.content)
	print('%s结束下载' % title)
def main():
	#解析首页，返回所有的标题链接
	for i in range(1,2):
		handle_title(i)

if __name__ == '__main__':
	main()

