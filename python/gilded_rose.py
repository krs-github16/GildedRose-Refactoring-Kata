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

            if item.name in self.exceptional_items:
                item.quality = self.exceptional_quality # enforce quality for exceptional items (sulfuras)
                continue # do nothing else for exceptional items

            if item.quality < self.min_quality:
                item.quality = self.min_quality # enforce minimum quality
            elif item.quality > self.max_quality:
                item.quality = self.max_quality # enforce maximum quality
            else:
                pass

            if item.name in self.improving_items or item.name in self.exceptional_items:
                if item.quality < self.max_quality:
                    increment = 1 # default increment for improving items

                    if item.name.startswith("Backstage passes"):
                        increment += (item.sell_in <= 10) + (item.sell_in <= 5) # +1 if 10 days or less, +1 if 5 days or less

                    item.quality = min(item.quality + increment, self.max_quality) # increase quality with cap at max_quality
            else:
                if item.quality > self.min_quality:
                    item.quality -= 1 # degrade in quality for normal items

            if item.sell_in <= 0:

                if item.name == "Aged Brie":
                    item.quality += 1 # Aged Brie further increases in quality after sell_in date
                    item.quality = min(item.quality, self.max_quality) # capped at max_quality
                
                if item.name.startswith("Backstage passes"):
                    item.quality = 0 # quality drops to 0 after concert

                if item.name in self.exceptional_items or item.name in self.improving_items:
                    pass

                elif item.quality > self.min_quality: # normal items degrade twice as fast after sell_in date
                    item.quality -= 1

            item.sell_in -= 1 # decrement sell_in for all but exceptional items


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
