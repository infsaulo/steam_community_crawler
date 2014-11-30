import re
import simplejson as json
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from steamcommunity_crawler.items import SteamcommunityCrawlerItem
from exceptions import AttributeError, IndexError

class SteamCommunitySpider(CrawlSpider):
    name = 'steamcommunity'
    allowed_domains = ['steamcommunity.com']
    start_urls = ['http://steamcommunity.com/profiles/76561197960265729/games/?tab=all']

    rules = (
        Rule(SgmlLinkExtractor(allow=[r'/profiles/\d+/games/\?tab=all']),
             callback='parse_game_list', follow=True),
    )


    def parse_game_list(self, response):
        sel = Selector(response)

        steam_id = None
        try:
            steam_id = re.search('/profiles/(\d+)/games', response.url).group(1)
        except AttributeError:
            steam_id = response.meta['steam_id']

        try:
            game_list = json.loads(re.search('rgGames = (\[.*\]);',
                                             sel.xpath('//script[@language="javascript"]')
                                             .extract()[0]).group(1))

            for game in game_list:
                if game.has_key('hours_forever') and game['availStatLinks']['achievements']:
                    game_id = game['appid']
                    game_name = game['name']
                    total_hours_played = game['hours_forever']

                    request = Request('http://steamcommunity.com/profiles/'
                                      + str(steam_id) + '/stats/' + str(game_id) + '/?tab=achievements',
                                      callback=self.parse_game_achievements)
                    request.meta['steam_id'] = steam_id
                    request.meta['game_id'] = game_id
                    request.meta['game_name'] = game_name
                    request.meta['total_hours_played'] = total_hours_played

                    yield request

        except IndexError: # Page is private
            pass

        request = Request('http://steamcommunity.com/profiles/' + str(int(steam_id)+1) + '/games/?tab=all',
                              callback=self.parse_game_list)
        request.meta['steam_id'] = str(int(steam_id)+1)
        yield request

    def parse_game_achievements(self, response):
        sel = Selector(response)

        item = SteamcommunityCrawlerItem()
        try:
            item['achievements_percentage'] = re.search('\((\d+)%\)',
                                                sel.xpath('//div[@id="topSummaryAchievements"]/text()')
                                                .extract()[0]).group(1)
        except IndexError:
            try:
                item['achievements_percentage'] = re.search('\((\d+)%\)',
                                                    sel.xpath('//div[@class="achievementStatusText"]/text()')
                                                    .extract()[1]).group(1)
            except IndexError:
                return

        item['steam_id'] = response.meta['steam_id']
        item['app_id'] = response.meta['game_id']
        item['app_name'] = response.meta['game_name']
        item['total_hours_played'] = response.meta['total_hours_played']

        return item

