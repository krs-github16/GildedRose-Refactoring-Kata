# -*- coding: utf-8 -*-

class GildedRose(object):
    """Class representing the Gilded Rose inventory system"""

    def __init__(self, items):
        """Initialize GildedRose with a list of items; set quality bounds and legendary items"""
        self.items = items
        self.MIN_QUALITY = 0
        self.MAX_QUALITY = 50

        self.BACKSTAGE_PASS_THRESHOLD_1 = 10 # days before concert when backstage pass quality increases faster
        self.BACKSTAGE_PASS_THRESHOLD_2 = 5  # days before concert when backstage pass quality increases fastest

        self.LEGENDARY_QUALITY = 80 # for Sulfuras
        self.LEGENDARY_ITEMS = ["Sulfuras, Hand of Ragnaros"] # never has to be sold or decreases in quality

    #### Item type check helper methods ####
    
    def is_aged_brie(self, item):
        """Check if the item is 'Aged Brie'"""
        return item.name == "Aged Brie"
    
    def is_backstage_pass(self, item):
        """Check if the item is a 'Backstage pass'"""
        return item.name.startswith("Backstage passes")
    
    def is_conjured(self, item):
        """Check if the item is a 'Conjured' item"""
        return item.name.startswith("Conjured")
    
    def is_legendary(self, item):
        """Check if the item is legendary"""
        return item.name in self.LEGENDARY_ITEMS

    #### Quality check helper methods ###

    def is_quality_above_minimum(self, item):
        """Check if the item's quality is above the minimum"""
        return item.quality > self.MIN_QUALITY

    def is_quality_below_maximum(self, item):
        """Check if the item's quality is below the maximum"""
        return item.quality < self.MAX_QUALITY

    ### Quality limiting/capping helper methods ###

    def get_legendary_quality(self):
        """Get the fixed quality for legendary items"""
        return self.LEGENDARY_QUALITY # enforce quality for legendary items (sulfuras)
    
    def limit_quality_at_minimum(self, item):
        """Ensure quality is not below minimum"""
        return max(item.quality, self.MIN_QUALITY) # cap quality at min_quality

    def limit_quality_at_maximum(self, item):
        """Ensure quality is not above maximum"""
        return min(item.quality, self.MAX_QUALITY) # cap quality at max_quality

    ### Extra degradation for conjured items ###
    
    def _apply_conjured_extra_degradation(self, item):
        """Apply extra degradation for conjured items"""
        if self.is_quality_above_minimum(item):
            item.quality -= 1 # further degradation for conjured items

    ### Main update quality method ###
    def _increment_quality(self, item):
        item.quality += 1

    def _decrement_quality(self, item):
        item.quality -= 1

    def update_quality(self):
        """Update quality and sell_in for all items for one day; legendary items do not change"""

        for item in self.items:

            if self.is_legendary(item):

                item.quality = self.get_legendary_quality()
                continue

            item.quality = self.limit_quality_at_minimum(item) # correct incorrect quality below minimum right at the start
            item.quality = self.limit_quality_at_maximum(item) # correct incorrect quality above maximum right at the start

            if self.is_aged_brie(item) or self.is_backstage_pass(item):
                
                if self.is_quality_below_maximum(item):

                    self._increment_quality(item) # default increment for improving items

                    if self.is_backstage_pass(item): 
                        item.quality += (item.sell_in <= self.BACKSTAGE_PASS_THRESHOLD_1) + (item.sell_in <= self.BACKSTAGE_PASS_THRESHOLD_2) # +1 if 10 days or less, +1 if 5 days or less

                    item.quality = self.limit_quality_at_maximum(item) # increase quality with cap at max_quality
            else:

                if self.is_quality_above_minimum(item):

                    self._decrement_quality(item) # degrade in quality for normal items

                    if self.is_conjured(item):
                        self._apply_conjured_extra_degradation(item)

            item.sell_in -= 1 # decrease sell_in for all non-legendary items

            if item.sell_in < 0:

                if self.is_aged_brie(item):

                    self._increment_quality(item) # Aged Brie further increases in quality after sell_in date
                    item.quality = self.limit_quality_at_maximum(item) # capped at max_quality
                    continue

                if self.is_backstage_pass(item):
                    item.quality = 0 # quality drops to 0 after concert
                    continue

                if self.is_quality_above_minimum(item): # normal items further degrade after sell_in date
                    
                    self._decrement_quality(item)

                    if self.is_conjured(item): 
                        self._apply_conjured_extra_degradation(item)

class Item:
    def __init__(self, name, sell_in, quality):
        """
        :param name (str): name of the item
        :param sell_in (int): # of days we have to sell the item; decreases by 1 each day
        :param quality (int): how valuable the item is (bounded in most cases between 0 and 50)
        """
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
