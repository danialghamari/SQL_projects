import asyncio, random, json, asyncio, aiohttp, pickle as pkl
from aiohttp_socks import ProxyConnector
from bs4 import BeautifulSoup as bs

semaphore_ = asyncio.Semaphore(10)

async def fetch_html_text(session, url):

    iter_exception_raise = 0
    async with semaphore_:
        while True:
            delay = 0.5 + random.uniform(0.2,0.2+iter_exception_raise*0.1)
            await asyncio.sleep(delay)
            
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()

                print(f"{url}: status {response.status}, retrying...")
                  
            except Exception as e:
                print(f"{url}: exception {e}, retrying...")

            iter_exception_raise+=1

async def get_pages(urls,headers):
    timeout = aiohttp.ClientTimeout(total=20        # Total time for the whole request
                                        )
    socks = ProxyConnector.from_url("socks5://127.0.0.1:9150")

    async with aiohttp.ClientSession(headers=headers,timeout=timeout,connector=socks) as session:
            html_pages = await asyncio.gather(
            *(fetch_html_text(session, url) for url in urls)
            )
    return html_pages
## -------------------------------------------------------------------------

alistofbooks_headers = {
'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0',
'Accept': 'text/html,application/xhtml+xml,text/vnd.turbo-stream.html,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.9',
'Accept-Encoding': 'gzip, deflate, br, zstd',
}

amazon_headers = {
'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0'
,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
,'Accept-Language':'en-US,en;q=0.9'
,'Accept-Encoding':'gzip, deflate, br, zstd'
,'Alt-Used':'www.amazon.com'
,'Cookie':'session-id=143-1504316-1054016; session-id-time=2082787201l; i18n-prefs=CHF; lc-main=en_US; sp-cdn="L5Z9:CH"; csm-hit=tb:1GJE13TRBB21Y9VSP9YB+s-1GJE13TRBB21Y9VSP9YB|1783181558093&t:1783181558093&adb:adblk_yes; ubid-main=135-2987448-5496464; session-token=4CyXyx9YAstJTU3TWJMY9sUFQH1mIxxxIXIhMA0oECdlkZRqytpPWnDhhuwpnz4/rpw0QAD9fOj73lq4ZGDA82GME35kwt6haXXmzgbv2kFWbsDwUxzw4aV8XfSuhxWPTqHNJSbT1VnpsnkSf79xfXn+K7uu8XjAEEeEO9kyOzuOh6QhffhJUVkE2aDEKQmK55nzoiBcp4ecAG7uYX6xItJRZpO3aPsN; rxc=AM8E/3X/ZWCKzxoLuZU; cmc=fm+AqniY+i3VHvBu0JroNt7d3yldcT1DmK2VgbGCMs7JSf+WUWz2LnTiww5Nt2Q6jv4P05/DylvNBwAxU7KdiOH94WqI/BWN6Qj7wBOFmfTk2Ov0rHmaeet9iQuc3YGTbkhnnWBAhg4VHiVNqDpJqpcervli66kTazimkum5ke67w9cqFt0kX9v497ZKS3ArxDe10bZD7dZ0zbRias3VtzpjiWsWB6UoYE58m8Ck5ZvpFyOGtli8QEQZhb6li8W8of8X6hBxM5CfyM2dsvISj8rc1Vz0IaAKqfZPuBdLvmICPXXnZXw=; rx=AQDEoU2Zg73y6zGoxqkqzN7Exqg=@Aa0wSWo='
,'Upgrade-Insecure-Requests':'1'
,'Sec-Fetch-Dest':'document'
,'Sec-Fetch-Mode':'navigate'
,'Sec-Fetch-Site':'none'
,'DNT':'1'
,'Sec-GPC':'1'
,'Priority':'u=0, i'}

async def get_book_urls(urls,savefile):

    html_pages = await get_pages(urls,headers=alistofbooks_headers)


    # Find the reference link to each book, where you'd find the amazon/goodread link    
    ref_urls = []
    for html_text in html_pages:
        
        if html_text is None:
            continue

        soup = bs(html_text, "html.parser")

        ref = soup.find_all("h3",class_='text-xl font-bold text-primary-500 mb-1 hover:text-primary-600 transition-colors')
        for link in ref:
            ref_urls.append(f"https://www.alistofbooks.com"+link.find('a')["href"])

    html_pages = await get_pages(ref_urls,headers=alistofbooks_headers)

    book_urls = []
    
    for c,html_text in enumerate(html_pages):

        if html_text is None:
            continue
        
        soup = bs(html_text,'html.parser')
        links = soup.find_all("a",href=lambda h: h and ("amazon.com" in h or "goodread" in h))
        if len(links)>1:
            for i in links:
                if 'goodread' in i["href"]:
                        book_urls.append(i["href"])
        elif len(links)==1:
            book_urls.append(links[0]["href"])
        else:
            print(urls[c])
    
    with open(savefile,'wb') as file:
        pkl.dump(book_urls,file)

#-------------------------------------------------------------------------------------------------------

async def get_book_details(urls,savefile):
    
    html_pages = await get_pages(urls,headers=alistofbooks_headers)

    details = []

    for counter,html_text in enumerate(html_pages):

        if html_text is None:
            continue
        
        if 'amazon' in urls[counter]:
            details.append(get_amazon_details(html_text))
        elif 'goodread' in urls[counter]:
            details.append(get_goodread_details(html_text))

    
    with open(savefile,'wb') as file:
        pkl.dump(details,file)


#-------------------------------------------------------------------------------------------------------

def get_goodread_details(html_text):
    
    book_template = [
                'name',
                'bookFormat',
                'numberOfPages',
                'inLanguage',
                'isbn',
                'awards',
                ['author' , ['@type' , 'name']],
                ['aggregateRating', ['ratingValue']]]
    
    
        
    soup = bs(html_text,'html.parser')

    script = soup.find("script", type="application/ld+json")

    book_json = json.loads(script.string)

    book_details = {}
    
    for tag in book_template:
        
        if type(tag)==str:
            book_details.update({tag : book_json[tag] if tag in book_json.keys() else ''})
        else:
            book_details.update({tag[0] : {}})
            if tag[0]=='author':
                book_details[tag[0]].update({sub_tag : book_json[tag[0]][0][sub_tag] for sub_tag in tag[1]})
            else:
                book_details[tag[0]].update({sub_tag : book_json[tag[0]][sub_tag] for sub_tag in tag[1]})
    

    
    return book_details
#-------------------------------------------------------------------------------------------------------

def get_amazon_details(html_text):
    
    def get_attribute(soup,name):
        div = soup.select_one(
            f'[data-rpi-attribute-name="{name}"] .rpi-attribute-value'
        )
        return div.get_text(strip=True) if div else None

    soup = bs(html_text,'html.parser')

    book = {}
    try:
        book["title"] = soup.select_one("#productTitle").get_text(strip=True)
    
        book["author"] = soup.select_one("#bylineInfo a").get_text(strip=True)

        spans = soup.select_one("#bylineInfo").find_all('span')
        for i,span in enumerate(spans):
            if span.get_text(strip=True) == "Format:":
                book["format"] = spans[i+1].get_text(strip=True)
                break

        book["publisher"] = get_attribute(soup,"book_details-publisher")
        book["publication_date"] = get_attribute(soup,"book_details-publication_date")
        book["isbn10"] = get_attribute(soup,"book_details-isbn10")
        book["isbn13"] = get_attribute(soup,"book_details-isbn13")
        book["num_pages"] = get_attribute(soup,"book_details-fiona_pages")
        book["languages"] = get_attribute(soup,"language")

        book["amazon_rating"] = soup.select_one(
            '[data-hook="rating-out-of-text"]'
        ).get_text(strip=True)

        book["amazon_review_count"] = soup.select_one(
            '[data-hook="total-review-count"]'
        ).get_text(strip=True)
        
    except:
        with open('dummy.txt','w') as f: f.write(html_text)
        raise Exception("amazon didn't return")

    
    return book



    