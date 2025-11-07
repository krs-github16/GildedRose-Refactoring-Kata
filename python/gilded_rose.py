# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items
        self.min_quality = 0
        self.max_quality = 50
        self.exceptional_items = ["Sulfuras, Hand of Ragnaros"] # never has to be sold or decreases in quality
        self.improving_items = ["Aged Brie", "Backstage passes to a TAFKAL80ETC concert"] # increase in quality over time (in general)
        self.exceptional_quality = 80 # for Sulfuras

    def update_quality(self):

        for item in self.items:

            if item.name not in self.improving_items and item.name not in self.exceptional_items:
                if item.quality > self.min_quality:
                    item.quality -= 1 # degrade in quality for normal/regular items
            else:
                if item.quality < self.max_quality:
                    increment = 1 # default increment for improving items

                    if item.name.startswith("Backstage passes"):
                        increment += (item.sell_in < 11) + (item.sell_in < 6) # +1 if 10 days or less, +1 if 5 days or less

                    item.quality = min(self.max_quality, item.quality + increment) # increase quality for improving items with cap at max_quality

            if item.name not in self.exceptional_items:
                item.sell_in -= 1

            if item.sell_in < 0:
                
                if item.name.startswith("Backstage passes"):
                    item.quality = 0

                if item.name == "Aged Brie":
                    item.quality += 1
                    item.quality = min(self.max_quality, item.quality)

                if item.name in self.exceptional_items or item.name in self.improving_items:
                    pass
                elif item.quality > self.min_quality:
                    item.quality -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        """
        :param name: str # name of the item
        :param sell_in: int # of days we have to sell the item
        :param quality: int # how valuable the item is
        """
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
