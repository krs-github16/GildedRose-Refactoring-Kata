from item import Item
from product_list import ProductList

class GildedRoseUpdater():
    """Class encapsulating the update logic for Gilded Rose items"""

    def __init__(self):

        self.MIN_QUALITY = 0
        self.MAX_QUALITY = 50

        self.LEGENDARY_QUALITY = 80 # for Sulfuras

        self.BACKSTAGE_PASS_THRESHOLD_1 = 10 # days before concert when backstage pass quality increases faster
        self.BACKSTAGE_PASS_THRESHOLD_2 = 5  # days before concert when backstage pass quality increases fastest
    
    ### Quality boundary check helper methods

    def _normalize_quality(self, item: Item) -> None:
        """Ensure item's quality is within configured bounds"""

        if item.name == ProductList.SULFURAS.value:
            item.quality = self.LEGENDARY_QUALITY 
        else:
            item.quality = max(item.quality, self.MIN_QUALITY) # cap quality at min_quality when quality is too low < 0
            item.quality = min(item.quality, self.MAX_QUALITY) # cap quality at max_quality when quality is too high > 50
        
    #### Update methods for different item types for one day (sell_in decrement handled separately)

    def _update_sell_in(self, item: Item) -> None:
        """Update sell_in for non-legendary items"""

        if item.name == ProductList.SULFURAS.value:
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