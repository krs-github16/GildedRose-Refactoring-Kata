# -*- coding: utf-8 -*-
from item import Item
from product_list import ProductList
from gilded_rose_updater import GildedRoseUpdater

class GildedRose(object):
    """Class representing the Gilded Rose inventory system"""

    def __init__(self, items: list[Item]):
        """Initialize GildedRose with a list of items; set quality bounds and legendary items"""

        self.items = items

    #### Item type check helper methods

    def is_aged_brie(self, item: Item) -> bool:
        """Check if the item is 'Aged Brie'"""
        return item.name == ProductList.AGED_BRIE.value

    def is_backstage_pass(self, item: Item) -> bool:
        """Check if the item is a 'Backstage pass'. Flexible to allow for different concert names"""
        return item.name.startswith(ProductList.BACKSTAGE_PASS.value)

    def is_legendary(self, item: Item) -> bool:
        """Check if the item is legendary (e.g. Sulfuras)"""
        return item.name == ProductList.SULFURAS.value
        
    def is_conjured(self, item: Item) -> bool:
        """Check if the item is a 'Conjured' item. Flexible to allow for different conjured items"""
        return item.name.startswith(ProductList.CONJURED.value)

    def update(self):
        """Update quality and sell_in for all items for one day; legendary items do not change"""
        
        updater = GildedRoseUpdater()

        for item in self.items:

            updater._normalize_quality(item)

            if self.is_aged_brie(item):
                updater._update_aged_brie_quality(item)

            elif self.is_backstage_pass(item):
                updater._update_backstage_pass_item_quality(item)

            elif self.is_legendary(item):
                pass

            elif self.is_conjured(item):
                updater._update_conjured_item_quality(item)

            else:
                updater._update_normal_item_quality(item)

            updater._update_sell_in(item)

# End of gilded_rose.py