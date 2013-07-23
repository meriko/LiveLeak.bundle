TITLE  = 'Live Leak'
ART    = 'art-default.jpg'
ICON   = 'icon-default.png'
PREFIX = '/video/liveleak'

BASE_URL = "http://www.liveleak.com/"

HTTP_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1"

PREDEFINED_CATEGORIES = [ 
    {
        'title':    'Popular Recent Items',
        'url':      BASE_URL + 'browse?selection=popular'
    },
    {
        'title':    'All Recent Items',
        'url':      BASE_URL + 'browse?selection=all'
    },
    {
        'title':    'Upcoming Items',
        'url':      BASE_URL + 'browse?upcoming=1'
    },
    {
        'title':    'Top Items Today',
        'url':      BASE_URL + 'browse?rank_by=day'
    },
    {
        'title':    'Top Items Week',
        'url':      BASE_URL + 'browse?rank_by=week'
    },
    {
        'title':    'Top Items Month',
        'url':      BASE_URL + 'browse?rank_by=month'
    },
    {
        'title':    'Top Items All Time',
        'url':      BASE_URL + 'browse?rank_by=all_time'
    },
]

##########################################################################################
def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art    = R(ART)
    
    DirectoryObject.thumb = R(ICON)

    HTTP.CacheTime             = CACHE_1HOUR
    HTTP.Headers['User-agent'] = HTTP_USER_AGENT

##########################################################################################
def ValidatePrefs():
    oc = ObjectContainer()
    oc.header  = "Note!"
    oc.message = "Please restart channel for changes to take affect"
    return oc

##########################################################################################
@handler(PREFIX, TITLE, thumb = ICON, art = ART)
def MainMenu():
    oc = ObjectContainer()
    
    pageElement = HTML.ElementFromURL(CreateURL(BASE_URL))
    
    # Add predefined categories
    for category in PREDEFINED_CATEGORIES:
        oc.add(
            DirectoryObject(
                key = 
                    Callback(
                        Videos, 
                        name = category['title'], 
                        url = CreateURL(category['url'])
                    ), 
                title = category['title']
        )
    )
    
    # Add categories parsed from site
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
                            url = CreateURL(BASE_URL + url)
                        ), 
                    title = title
                )
            )       
    
    # Add preference for Safe Mode
    oc.add(PrefsObject(title = "Preferences..."))
    
    return oc
    
##########################################################################################
@route(PREFIX + "/Videos", page = int)
def Videos(name, url, page = 1):
    oc = ObjectContainer(title1 = name)

    pageElement = HTML.ElementFromURL(CreateURL(url + '#item_page=' + str(page)))
    
    for item in pageElement.xpath("//*[@class = 'item_list']//li"):
        try:
            link    = item.xpath(".//a/@href")[0]
            
            if not link.startswith("http://www.liveleak.com/view"):
                continue
                
            title   = item.xpath(".//a/text()")[0]
            
            try:
                summary = item.xpath(".//div/text()")[4].strip()
            except:
                summary = None
                
            try:
                thumb = item.xpath(".//a//img/@src")[0]
            except:
                thumbe = None
            
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

##########################################################################################
def CreateURL(url):
    if not '?' in url:
        url = url + '?'
    else:
        url = url + '&'
        
    if Prefs['safe']:
        url = url + 'safe_mode=on'
    else:
        url = url + 'safe_mode=off'
        
    return url
