TITLE  = 'Live Leak'
ART    = 'art-default.jpg'
ICON   = 'icon-default.png'
PREFIX = '/video/liveleak'

BASE_URL = "http://www.liveleak.com"

RE_VIDEO_URL = Regex('.*file *: *\"(.*\.mp4.*)\".*', Regex.IGNORECASE)

HTTP_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1"

##########################################################################################
def Start():
	ObjectContainer.title1 = TITLE
	ObjectContainer.art    = R(ART)
	
	DirectoryObject.thumb = R(ICON)

	HTTP.CacheTime             = CACHE_1HOUR
	HTTP.Headers['User-agent'] = HTTP_USER_AGENT
	
##########################################################################################
@handler(PREFIX, TITLE, thumb = ICON, art = ART)
def MainMenu():
	oc = ObjectContainer()
	
	pageElement = HTML.ElementFromURL(BASE_URL)
	
	# Add all channels
	for item in pageElement.xpath("//*[@id = 'subnav']//li"):
		url = item.xpath(".//a/@href")[0]
		
		if url.startswith("c/"):
			title = item.xpath(".//a/text()")[0]
			
			oc.add(
				DirectoryObject(
					key = 
						Callback(
							Videos, 
							name = title, 
							url = BASE_URL + "/" + url,
							page = 1
						), 
					title = title
				)
			)		
	
	return oc
	
##########################################################################################
@route(PREFIX + "/Videos", page = int)
def Videos(name, url, page):
	oc = ObjectContainer(title1 = name)

	pageElement = HTML.ElementFromURL(url + '#item_page=' + str(page))
	
	for item in pageElement.xpath("//*[@class = 'item_list']//li"):
		try:
			link    = item.xpath(".//a/@href")[0]
			title   = item.xpath(".//a/text()")[0]
			summary = item.xpath(".//div//text()")[0]
			thumb   = item.xpath(".//a//img/@src")[0]
			
			oc.add(
				VideoClipObject(
					url = link,
					title = title,
					summary = summary,
					thumb = thumb,
				)
			)
			
		except:
			pass
			

	oc.add(
		NextPageObject(
			key = 
				Callback(
					Videos,
					name = name,
					url = url,
					page = page + 1
				),
			title = "More..."
		)
	)

	return oc
