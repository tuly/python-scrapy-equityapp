import re
from equityapp.items import EquityappItem

__author__ = 'tuly'

from scrapy import Spider, Selector, Request, FormRequest


class EquityAppSpider(Spider):
    name = 'equity'
    host = 'www.equityapartments.com'
    allowed_domains = ['equityapartments.com']
    start_urls = ['http://www.equityapartments.com/massachusetts/west-boston-apartments.aspx',
                  'http://www.equityapartments.com/new-jersey/west-new-york-apartments.aspx',
                  'http://www.equityapartments.com/new-jersey/south-plainfield-apartments.aspx',
                  'http://www.equityapartments.com/connecticut/stamford-apartments.aspx',
                  'http://www.equityapartments.com/new-york/westchester-apartments.aspx',
                  'http://www.equityapartments.com/massachusetts/south-boston-apartments.aspx',
                  'http://www.equityapartments.com/washington-dc/washington-dc-apartments.aspx',
                  'http://www.equityapartments.com/washington/seattle-apartments.aspx',
                  'http://www.equityapartments.com/arizona/phoenix-apartments.aspx',
                  'http://www.equityapartments.com/new-jersey/philadelphia-apartments.aspx',
                  'http://www.equityapartments.com/florida/palm-beach-apartments.aspx',
                  'http://www.equityapartments.com/california/san-diego-apartments.aspx',
                  'http://www.equityapartments.com/florida/orlando-apartments.aspx',
                  'http://www.equityapartments.com/california/san-francisco-apartments.aspx'
                  'http://www.equityapartments.com/california/orange-county-apartments.aspx',
                  'http://www.equityapartments.com/connecticut/norwalk-apartments.aspx',
                  'http://www.equityapartments.com/virginia/northern-virginia-apartments.aspx',
                  'http://www.equityapartments.com/maryland/maryland-apartments.aspx',
                  'http://www.equityapartments.com/california/los-angeles-apartments.aspx',
                  'http://www.equityapartments.com/new-york/new-york-city-apartments.aspx',
                  'http://www.equityapartments.com/florida/miami-apartments.aspx',
                  'http://www.equityapartments.com/colorado/denver-apartments.aspx',
                  'http://www.equityapartments.com/new-jersey/jersey-city-apartments.aspx',
                  'http://www.equityapartments.com/connecticut/hartford-apartments.aspx',
                  'http://www.equityapartments.com/california/inland-empire-apartments.aspx',
                  'http://www.equityapartments.com/florida/fort-lauderdale-apartments.aspx',
                  'http://www.equityapartments.com/colorado/boulder-apartments.aspx',
                  'http://www.equityapartments.com/massachusetts/boston-apartments.aspx'
                  'http://www.equityapartments.com/virginia/alexandria-arlington-apartments.aspx']

    def parse(self, response):
        try:
            selector = Selector(response)
            apartments = selector.xpath('//div[@class="PostalAddress"]/span[@itemprop="name"]/a/@href').extract()
            if len(apartments) > 0:
                for apartment in apartments:
                    yield Request(url=apartment, meta={'url': apartment}, callback=self.parse_apartment)

        except Exception, x:
            print 'Problem 1'
            print x

    def parse_apartment(self, response):
        try:
            selector = Selector(response)
            lat_lon = selector.xpath('//meta[@name="GPS"]/@content').extract()
            lat, lon = lat_lon[0].split(' ')
            lat = float(lat) if self.is_number(lat.strip()) else 0
            lon = float(lon) if self.is_number(lon.strip()) else 0

            building_name_content = selector.xpath(
                '//div[@id="local-business"]/h1/span[@itemprop="name"]/text()').extract()
            building_name = building_name_content[0] if len(building_name_content) > 0 else ''

            address_selector = selector.xpath('//div[@id="addressText"]/span')
            addresses = []
            for sel in address_selector:
                addresses.append(sel.xpath('text()')[0].extract().strip())
            address = ' '.join(addresses)

            description = selector.xpath('string(//div[@id="communityDescription"])')[0].extract().strip()
            pictures = []
            pictures_selector = selector.xpath('//ul[@id="altThumbnailNav"]/li/a[@class="altNavLink"]/@href').extract()
            for pic_sel in pictures_selector:
                pictures.append(pic_sel.strip())

            post_url = '/'.join(response.url.split('/')[:-2])
            # # post request for getting all floor plans
            post_url_part = selector.xpath('//form[@name="aspnetForm"]/@action')[0].extract()
            view_state_generator = selector.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value')[0].extract()
            view_state = selector.xpath('//input[@id="__VIEWSTATE"]/@value')[0].extract()
            post_data = {'__ASYNCPOST': 'true',
                         '__EVENTTARGET': 'ctl00$Body$FloorplansContainer1$UnitSelectionControl1$uxAllFloorplans',
                         '__VIEWSTATEGENERATOR': view_state_generator,
                         '__VIEWSTATE': view_state}
            header = {'Accept': 'text/html, */*',
                      'Connection': 'keep-alive',
                      'Host': self.host,
                      'Referer': response.url,
                      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0',
                      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                      'X-MicrosoftAjax': 'Delta=true',
                      'X-Requested-With': 'XMLHttpRequest'}
            meta = {'latitude': lat,
                    'longitude': lon,
                    'building': building_name,
                    'address': address,
                    'description': description,
                    'pictures': pictures}
            yield FormRequest(post_url + '/' + post_url_part, meta=meta, method='POST',
                              formdata=post_data, headers=header,
                              callback=self.parse_apartment_details)
        except Exception, x:
            print 'apartment error: '
            print x

    def parse_apartment_details(self, response):
        try:
            selector = Selector(response)
            meta = response.meta

            move_in_date = ''
            move_in_date_sel = selector.xpath('//div[@id="moveInDatePanel"]/input/@value')
            if move_in_date_sel and len(move_in_date_sel) > 0:
                move_in_date_arr = move_in_date_sel[0].extract().strip().split('/')
                if move_in_date_arr and len(move_in_date_arr) > 2:
                    move_m, move_d, move_y = move_in_date_arr
                    move_in_date = move_y + move_m.zfill(2) + move_d.zfill(2)

            floorplan_selector = selector.xpath('//div[@class="floorplan"]')
            for f_sel in floorplan_selector:
                av = f_sel.xpath('.//i[@class="viewUnits"]')
                if not av: continue

                floor_plan = ''
                floor_plan_sel = f_sel.xpath('.//h3/text()').extract()
                if floor_plan_sel and len(floor_plan_sel) > 0:
                    floor_plan = floor_plan_sel[0].strip()

                bedroom = 0
                bathroom = 0
                size = 0
                price = 0
                length = 0

                fp_detail_selector = f_sel.xpath('p')
                if fp_detail_selector:
                    fp_details = fp_detail_selector.xpath('text()').extract()
                    if fp_details and len(fp_details) > 0:
                        bedroom_content = fp_details[0]
                        bedroom = bedroom_content.replace('bed', '').strip()
                        bedroom = float(bedroom) if self.is_number(bedroom) else 0
                    if fp_details and len(fp_details) > 1:
                        bathroom_content = fp_details[1]
                        bathroom = bathroom_content.replace('bath', '').strip()
                        bathroom = float(bathroom) if self.is_number(bathroom) else 0
                    if fp_details and len(fp_details) > 2:
                        size_content = fp_details[2]
                        size = size_content.replace('sqft', '').strip()
                        size = float(size) if self.is_number(size) else 0
                    if len(fp_detail_selector.extract()) > 3:
                        price_length_content = fp_detail_selector[3].extract()
                        price_content = re.search(
                            '(?i)<p>[^<]*<b>\s*?\$([0-9\,]+)</b>\s*?\((\d+)\s*?month\s*?\)\s*?</p>',
                            price_length_content)
                        if price_content:
                            price = float(price_content.group(1).replace(',', ''))
                            length = float(price_content.group(2))

                item = EquityappItem()
                item['address'] = meta['address']
                item['building'] = meta['building']
                item['floor_plan'] = floor_plan
                item['bedroom'] = bedroom
                item['bathroom'] = bathroom
                item['size'] = size
                item['price'] = price
                item['length'] = length
                item['move_in'] = move_in_date
                item['description'] = meta['description']
                item['latitude'] = meta['latitude']
                item['longitude'] = meta['longitude']
                item['pictures'] = meta['pictures']
                item['source'] = 'equityapartments'
                item['url'] = response.url

                yield item
        except Exception, x:
            print 'Detail error: '
            print x

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

