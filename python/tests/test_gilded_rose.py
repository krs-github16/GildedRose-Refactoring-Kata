# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    #######################NORMAL ITEM TESTS#########################
    def test_normal_item_before_sell_date(self):
        items = [Item("normal item", 5, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(19, items[0].quality) # decreases by 1

    def test_normal_item_on_sell_date_quality_degrades_twice_as_fast(self):
        items = [Item("normal item", 0, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(-1, items[0].sell_in) # decreases by 1
        self.assertEqual(18, items[0].quality) # decreases by 2 because item is past sell date (sell_in<=0)

    def test_normal_item_after_sell_date_quality_degrades_twice_as_fast(self):
        items = [Item("normal item", -1, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(-2, items[0].sell_in) # decreases by 1
        self.assertEqual(18, items[0].quality) # decreases by 2 because item is past sell date (sell_in<=0)

    def test_normal_item_of_zero_quality(self):
        items = [Item("normal item", 5, 0)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(0, items[0].quality) # stays the same, quality never negative

    def test_normal_item_of_quality_near_zero(self):
        items = [Item("normal item", 5, 1)]
        gr = GildedRose(items)
        gr.update_quality() # first day
        gr.update_quality() # second day
        self.assertEqual(3, items[0].sell_in) # decreases by 2, 1 each day
        self.assertEqual(0, items[0].quality) # quality min threshold at 0

    def test_normal_item_of_quality_near_max(self):
        items = [Item("normal item", 5, 49)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(48, items[0].quality) # decreases by 1

    def test_normal_item_of_max_quality(self):
        items = [Item("normal item", 5, 50)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(49, items[0].quality) # decreases by 1

    #######################AGED BRIE TESTS#########################
    def test_aged_brie_before_sell_date(self):
        items = [Item("Aged Brie", 5, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(21, items[0].quality) # increases by 1

    def test_aged_brie_on_sell_date_quality_improves_twice_as_fast(self):
        items = [Item("Aged Brie", 0, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(-1, items[0].sell_in) # decreases by 1
        self.assertEqual(22, items[0].quality) # increases by 2 because item is past sell date (sell_in<=0)

    def test_aged_brie_after_sell_date_quality_improves_twice_as_fast(self):
        items = [Item("Aged Brie", -1, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(-2, items[0].sell_in) # decreases by 1
        self.assertEqual(22, items[0].quality) # increases by 2 because item is past sell date (sell_in<=0)

    def test_aged_brie_of_zero_quality(self):
        items = [Item("Aged Brie", 5, 0)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(1, items[0].quality) # increases by 1

    def test_aged_brie_of_quality_near_zero(self):
        items = [Item("Aged Brie", 5, 1)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(2, items[0].quality) # increases by 1

    def test_aged_brie_of_quality_near_max(self):
        items = [Item("Aged Brie", 5, 49)]
        gr = GildedRose(items)
        gr.update_quality() # first day
        gr.update_quality() # second day
        self.assertEqual(3, items[0].sell_in) # decreases by 2, 1 each day
        self.assertEqual(50, items[0].quality) # quality max capped at 50

    def test_aged_brie_of_max_quality(self):
        items = [Item("Aged Brie", 5, 50)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(50, items[0].quality) # quality max capped at 50


    #######################SULFURAS TESTS#########################
    def test_sulfuras_before_sell_date(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(5, items[0].sell_in) # no update
        self.assertEqual(80, items[0].quality) # no update

    def test_sulfuras_on_sell_date(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 0, 80)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(0, items[0].sell_in) # no update
        self.assertEqual(80, items[0].quality) # no update

    def test_sulfuras_after_sell_date(self):
        items = [Item("Sulfuras, Hand of Ragnaros", -1, 80)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(-1, items[0].sell_in) # no update
        self.assertEqual(80, items[0].quality) # no update

    #########################BACKSTAGE PASS TESTS#########################
    def test_backstage_pass_long_before_sell_date(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(14, items[0].sell_in) # decreases by 1
        self.assertEqual(21, items[0].quality) # increases by 1 because sell_in>10

    def test_backstage_pass_medium_close_to_sell_date(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(9, items[0].sell_in) # decreases by 1
        self.assertEqual(22, items[0].quality) # increases by 2 because 5<sell_in<=10

    def test_backstage_pass_very_close_to_sell_date(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(23, items[0].quality) # increases by 3 because 0<sell_in<=5

    def test_backstage_pass_on_sell_date(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(-1, items[0].sell_in) # decreases by 1
        self.assertEqual(0, items[0].quality) # drops to 0 because sell_in<=0

    def test_backstage_pass_after_sell_date(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", -1, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(-2, items[0].sell_in) # decreases by 1
        self.assertEqual(0, items[0].quality) # drops to 0 because sell_in<=0

    def test_backstage_pass_of_zero_quality(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 0)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(3, items[0].quality) # increases by 3 because 0<sell_in<=5

    def test_backstage_pass_of_quality_near_zero(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 1)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(4, items[0].quality) # increases by 3 because 0<sell_in<=5

    def test_backstage_pass_of_quality_at_5(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 15)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(18, items[0].quality) # increases by 3 because 0<sell_in<=5

    def test_backstage_pass_of_quality_at_6(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 6, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(5, items[0].sell_in) # decreases by 1
        self.assertEqual(22, items[0].quality) # increases by 2 because 5<sell_in<=10

    def test_backstage_pass_of_quality_at_10(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 30)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(9, items[0].sell_in) # decreases by 1
        self.assertEqual(32, items[0].quality) # increases by 2 because 5<sell_in<=10

    def test_backstage_pass_of_quality_at_11(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 11, 20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(10, items[0].sell_in) # decreases by 1
        self.assertEqual(21, items[0].quality) # increases by 1 because sell_in>10

    def test_backstage_pass_of_quality_near_max(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 49)]
        gr = GildedRose(items)
        gr.update_quality() # first day
        gr.update_quality() # second day
        self.assertEqual(3, items[0].sell_in) # decreases by 1
        self.assertEqual(50, items[0].quality) # quality max capped at 50

    def test_backstage_pass_of_max_quality(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 50)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in) # decreases by 1
        self.assertEqual(50, items[0].quality) # quality max capped at 50

    ############################### END TESTS ##################################

        
if __name__ == '__main__':
    unittest.main()
