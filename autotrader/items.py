# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutotraderItem(scrapy.Item):
    Title = scrapy.Field()
    Price = scrapy.Field()
    Make = scrapy.Field()
    Model = scrapy.Field()
    Kilometres = scrapy.Field()
    Status = scrapy.Field()
    Trim = scrapy.Field()
    BodyType = scrapy.Field()
    Engine = scrapy.Field()
    Cylinder = scrapy.Field()
    Transmission = scrapy.Field()
    StockNumber = scrapy.Field()
    ExteriorColour = scrapy.Field()
    InteriorColour = scrapy.Field()
    Passengers = scrapy.Field()
    Doors = scrapy.Field()
    FuelType = scrapy.Field()
    CityFuelEconomy = scrapy.Field()
    HwyFuelEconomy = scrapy.Field()
    Drivetrain = scrapy.Field()

