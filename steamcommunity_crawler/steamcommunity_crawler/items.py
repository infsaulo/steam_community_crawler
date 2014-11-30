from scrapy.item import Item, Field

class SteamcommunityCrawlerItem(Item):
    steam_id = Field() # User id in steam platform
    app_id = Field() # Game id in steam platform
    app_name = Field() # Game's name
    total_hours_played = Field() # Amount of minutes user has spent playing this game
    achievements_percentage = Field() # Percentage of achievements an user has gotten from this game