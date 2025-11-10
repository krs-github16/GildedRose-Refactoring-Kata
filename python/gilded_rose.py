# -*- coding: utf-8 -*-

class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
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


class GildedRose(object):
    """Class representing the Gilded Rose inventory system"""

    def __init__(self, items: list[Item]):
        """Initialize GildedRose with a list of items; set quality bounds and legendary items"""

        self.items = items

        self.MIN_QUALITY = 0
        self.MAX_QUALITY = 50

        self.LEGENDARY_QUALITY = 80 # for Sulfuras
        self.LEGENDARY_ITEMS = ["Sulfuras, Hand of Ragnaros"] # never has to be sold or decreases in quality

        self.BACKSTAGE_PASS_THRESHOLD_1 = 10 # days before concert when backstage pass quality increases faster
        self.BACKSTAGE_PASS_THRESHOLD_2 = 5  # days before concert when backstage pass quality increases fastest

    #### Item type check helper methods

    def is_aged_brie(self, item: Item) -> bool:
        """Check if the item is 'Aged Brie'"""
        return item.name == "Aged Brie"

    def is_backstage_pass(self, item: Item) -> bool:
        """Check if the item is a 'Backstage pass'. Flexible to allow for different concert names"""
        return item.name.startswith("Backstage passes")

    def is_conjured(self, item: Item) -> bool:
        """Check if the item is a 'Conjured' item. Flexible to allow for different conjured items"""
        return item.name.startswith("Conjured")

    def is_legendary(self, item: Item) -> bool:
        """Check if the item is legendary (e.g. Sulfuras)"""
        return item.name in self.LEGENDARY_ITEMS
    
    ### Quality boundary check helper methods

    def normalize_quality(self, item: Item) -> None:
        """Ensure item's quality is within configured bounds"""

        if self.is_legendary(item):
            item.quality = self.LEGENDARY_QUALITY 
        else:
            item.quality = max(item.quality, self.MIN_QUALITY) # cap quality at min_quality when quality is too low < 0
            item.quality = min(item.quality, self.MAX_QUALITY) # cap quality at max_quality when quality is too high > 50
        
    #### Update methods for different item types for one day (sell_in decrement handled separately)

    def _update_sell_in(self, item: Item) -> None:
        """Update sell_in for non-legendary items"""

        if self.is_legendary(item):
            pass
        else:
            item.sell_in -= 1
            
    def _update_normal_item_quality(self, item: Item) -> None:
        '''Update method for normal items'''

        if item.sell_in > 0: 
            change = -1
        else:
            change = -2

        item.quality = max((item.quality + change), self.MIN_QUALITY)

    def _update_aged_brie_quality(self, item: Item) -> None:
        '''Update method for Aged Brie items'''

        if item.sell_in > 0:
            change = 1
        else:
            change = 2

        item.quality = min((item.quality + change), self.MAX_QUALITY)

    def _update_backstage_pass_item_quality(self, item: Item) -> None:
        '''Update method for backstage pass items'''

        if item.sell_in > self.BACKSTAGE_PASS_THRESHOLD_1:
            change = 1
        elif item.sell_in > self.BACKSTAGE_PASS_THRESHOLD_2:
            change = 2
        elif item.sell_in > 0:
            change = 3
        else:
            item.quality = 0
            change = 0

        item.quality = min((item.quality + change), self.MAX_QUALITY)

    def _update_conjured_item_quality(self, item: Item) -> None:
        '''
        Update method for conjured items
        Quality degrades twice as fast as normal items
        '''

        if item.sell_in > 0:
            change = -2
        else:
            change = -4

        item.quality = max((item.quality + change), self.MIN_QUALITY)

    def update_quality(self):
        """Update quality and sell_in for all items for one day; legendary items do not change"""

        for item in self.items:

            self.normalize_quality(item)

            if self.is_aged_brie(item):
                self._update_aged_brie_quality(item)

            elif self.is_backstage_pass(item):
                self._update_backstage_pass_item_quality(item)

            elif self.is_legendary(item):
                pass # legendary items do not change

            elif self.is_conjured(item):
                self._update_conjured_item_quality(item)

            else:
                self._update_normal_item_quality(item)

            self._update_sell_in(item)


# End of gilded_rose.py