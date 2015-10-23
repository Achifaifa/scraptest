import scrapy

class MySpider(scrapy.Spider):
  name='testspider'
  allowed_domains=["tripadvisor.com"]
  start_urls=['http://www.tripadvisor.com/Restaurants-g187457-San_Sebastian_Donostia_Guipuzcoa_Province_Basque_Country.html']

  def parserest(self,response):
    lat=response.xpath('//div[@class="mapContainer"]/@data-lat').extract()
    lon=response.xpath('//div[@class="mapContainer"]/@data-lng').extract()
    nam=response.xpath('//div[@class="mapContainer"]/@data-name').extract()
    yield {'name':nam, 'latitude':lat, 'longitude':lon}
    with open("./rests-ss","a+") as rests:
      rests.write("%s, %s, %s\n"%(nam, lat, lon)) 

  def parse(self,response):
    restaurants=response.xpath("//h3[@class='title']/a/@href").extract()
    for restaurant in restaurants:
      resturl=response.urljoin(restaurant)
      yield scrapy.Request(resturl,callback=self.parserest)
    
    nexturl=response.xpath('//a[text()="Next"]/@href').extract()
    if nexturl: nexturl=response.urljoin(nexturl[0])
    yield scrapy.Request(nexturl, callback=self.parse)
