# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def setUp(self):
        self.factory = lambda name, s, q: GildedRose([Item(name, s, q)])

    ##########################ITEM CREATION TESTS#########################

    def test_default_item_creation(self):
        gr = self.factory("Normal Item", 10, 20)
        self.assertEqual("Normal Item", gr.items[0].name)
        self.assertEqual(10, gr.items[0].sell_in)
        self.assertEqual(20, gr.items[0].quality)

    def test_default_item_str(self):
        gr = self.factory("Normal Item", 10, 20)
        self.assertEqual("Normal Item, 10, 20", str(gr.items[0]))
    
    def test_item_list_creation(self):
        items = [Item("Item1", 5, 10), Item("Item2", 3, 6)]
        gr = GildedRose(items)
        self.assertEqual("Item1", gr.items[0].name)
        self.assertEqual(5, gr.items[0].sell_in)
        self.assertEqual(10, gr.items[0].quality)
        self.assertEqual("Item2", gr.items[1].name)
        self.assertEqual(3, gr.items[1].sell_in)
        self.assertEqual(6, gr.items[1].quality)
        self.assertEqual(2, len(gr.items))
        
    #######################NORMAL ITEM TESTS#########################

    def test_normal_item_before_sell_date(self):
        gr = self.factory("Normal Item", 5, 20)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(19, gr.items[0].quality) # decreases by 1

    def test_normal_item_on_sell_date_quality_degrades_twice_as_fast(self):
        gr = self.factory("Normal Item", 0, 20)
        gr.update_quality()
        self.assertEqual(-1, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(18, gr.items[0].quality) # decreases by 2 because item is past sell date (sell_in<=0)

    def test_normal_item_after_sell_date_quality_degrades_twice_as_fast(self):
        gr = self.factory("Normal Item", -1, 20)
        gr.update_quality()
        self.assertEqual(-2, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(18, gr.items[0].quality) # decreases by 2 because item is past sell date (sell_in<=0)

    def test_normal_item_of_zero_quality(self):
        gr = self.factory("Normal Item", 5, 0)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(0, gr.items[0].quality) # stays the same, quality never negative

    def test_normal_item_of_quality_near_zero(self):
        gr = self.factory("Normal Item", 5, 1)
        gr.update_quality() # first day
        gr.update_quality() # second day
        self.assertEqual(3, gr.items[0].sell_in) # decreases by 2, 1 each day
        self.assertEqual(0, gr.items[0].quality) # quality min threshold at 0

    def test_normal_item_of_quality_near_max(self):
        gr = self.factory("Normal Item", 5, 49)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(48, gr.items[0].quality) # decreases by 1

    def test_normal_item_of_max_quality(self):
        gr = self.factory("Normal Item", 5, 50)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(49, gr.items[0].quality) # decreases by 1

    def test_normal_item_of_quality_greater_than_max(self):
        gr = self.factory("Normal Item", 5, 51)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(49, gr.items[0].quality) # decreases by 1 from max cap 50

    def test_normal_item_of_quality_greater_than_max_at_sell_in_zero(self):
        gr = self.factory("Normal Item", 0, 51)
        gr.update_quality()
        self.assertEqual(-1, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(48, gr.items[0].quality) # decreases by 2 from max cap 50

    #######################AGED BRIE TESTS#########################
    def test_aged_brie_before_sell_date(self):
        gr = self.factory("Aged Brie", 5, 20)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(21, gr.items[0].quality) # increases by 1

    def test_aged_brie_on_sell_date_quality_improves_twice_as_fast(self):
        gr = self.factory("Aged Brie", 0, 20)
        gr.update_quality()
        self.assertEqual(-1, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(22, gr.items[0].quality) # increases by 2 because item is past sell date (sell_in<=0)

    def test_aged_brie_after_sell_date_quality_improves_twice_as_fast(self):
        gr = self.factory("Aged Brie", -1, 20)
        gr.update_quality()
        self.assertEqual(-2, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(22, gr.items[0].quality) # increases by 2 because item is past sell date (sell_in<=0)

    def test_aged_brie_of_zero_quality(self):
        gr = self.factory("Aged Brie", 5, 0)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(1, gr.items[0].quality) # increases by 1

    def test_aged_brie_of_quality_near_zero(self):
        gr = self.factory("Aged Brie", 5, 1)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(2, gr.items[0].quality) # increases by 1

    def test_aged_brie_of_quality_near_max(self):
        gr = self.factory("Aged Brie", 5, 49)
        gr.update_quality() # first day
        gr.update_quality() # second day
        self.assertEqual(3, gr.items[0].sell_in) # decreases by 2, 1 each day
        self.assertEqual(50, gr.items[0].quality) # quality max capped at 50

    def test_aged_brie_of_max_quality(self):
        gr = self.factory("Aged Brie", 5, 50)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(50, gr.items[0].quality) # quality max capped at 50

    def test_aged_brie_of_quality_greater_than_max(self):
        gr = self.factory("Aged Brie", 5, 51)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(50, gr.items[0].quality) # quality max capped at 50

    def test_aged_brie_of_quality_greater_than_max_at_sell_in_zero(self):
        gr = self.factory("Aged Brie", 0, 51)
        gr.update_quality()
        self.assertEqual(-1, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(50, gr.items[0].quality) # quality max capped at 50


    #######################SULFURAS TESTS#########################
    def test_sulfuras_before_sell_date(self):
        gr = self.factory("Sulfuras, Hand of Ragnaros", 5, 80)
        gr.update_quality()
        self.assertEqual(5, gr.items[0].sell_in) # no update
        self.assertEqual(80, gr.items[0].quality) # no update

    def test_sulfuras_on_sell_date(self):
        gr = self.factory("Sulfuras, Hand of Ragnaros", 0, 80)
        gr.update_quality()
        self.assertEqual(0, gr.items[0].sell_in) # no update
        self.assertEqual(80, gr.items[0].quality) # no update

    def test_sulfuras_after_sell_date(self):
        gr = self.factory("Sulfuras, Hand of Ragnaros", -1, 80)
        gr.update_quality()
        self.assertEqual(-1, gr.items[0].sell_in) # no update
        self.assertEqual(80, gr.items[0].quality) # no update

    def test_sulfuras_of_quality_less_than_exceptional(self):
        gr = self.factory("Sulfuras, Hand of Ragnaros", 5, 70)
        gr.update_quality()
        self.assertEqual(5, gr.items[0].sell_in) # no update
        self.assertEqual(80, gr.items[0].quality) # quality reset to exceptional quality 80

    #########################BACKSTAGE PASS TESTS#########################
    def test_backstage_pass_long_before_sell_date(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 15, 20)
        gr.update_quality()
        self.assertEqual(14, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(21, gr.items[0].quality) # increases by 1 because sell_in>10

    def test_backstage_pass_medium_close_to_sell_date(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 10, 20)
        gr.update_quality()
        self.assertEqual(9, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(22, gr.items[0].quality) # increases by 2 because 5<sell_in<=10

    def test_backstage_pass_very_close_to_sell_date(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 5, 20)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(23, gr.items[0].quality) # increases by 3 because 0<sell_in<=5

    def test_backstage_pass_on_sell_date(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 0, 20)
        gr.update_quality()
        self.assertEqual(-1, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(0, gr.items[0].quality) # drops to 0 because sell_in<=0

    def test_backstage_pass_after_sell_date(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", -1, 20)
        gr.update_quality()
        self.assertEqual(-2, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(0, gr.items[0].quality) # drops to 0 because sell_in<=0

    def test_backstage_pass_of_zero_quality(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 5, 0)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(3, gr.items[0].quality) # increases by 3 because 0<sell_in<=5

    def test_backstage_pass_of_quality_near_zero(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 5, 1)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(4, gr.items[0].quality) # increases by 3 because 0<sell_in<=5

    def test_backstage_pass_of_quality_at_5(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 5, 15)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(18, gr.items[0].quality) # increases by 3 because 0<sell_in<=5

    def test_backstage_pass_of_quality_at_6(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 6, 20)
        gr.update_quality()
        self.assertEqual(5, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(22, gr.items[0].quality) # increases by 2 because 5<sell_in<=10

    def test_backstage_pass_of_quality_at_10(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 10, 30)
        gr.update_quality()
        self.assertEqual(9, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(32, gr.items[0].quality) # increases by 2 because 5<sell_in<=10

    def test_backstage_pass_of_quality_at_11(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 11, 20)
        gr.update_quality()
        self.assertEqual(10, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(21, gr.items[0].quality) # increases by 1 because sell_in>10

    def test_backstage_pass_of_quality_near_max(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 5, 49)
        gr.update_quality() # first day
        gr.update_quality() # second day
        self.assertEqual(3, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(50, gr.items[0].quality) # quality max capped at 50

    def test_backstage_pass_of_max_quality(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 5, 50)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(50, gr.items[0].quality) # quality max capped at 50

    def test_backstage_pass_of_quality_greater_than_max(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 5, 51)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(50, gr.items[0].quality) # quality max capped at 50

    def test_backstage_pass_of_quality_greater_than_max_at_sell_in_zero(self):
        gr = self.factory("Backstage passes to a TAFKAL80ETC concert", 0, 51)
        gr.update_quality()
        self.assertEqual(-1, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(0, gr.items[0].quality) # drops to 0 because sell_in<=0

    ########################CONJURED ITEM TESTS#########################
    def test_conjured_item_before_sell_date(self):
        gr = self.factory("Conjured Mana Cake", 5, 20)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(18, gr.items[0].quality) # decreases by 2

    def test_conjured_item_on_sell_date_quality_degrades_twice_as_fast(self):
        gr = self.factory("Conjured Mana Cake", 0, 20)
        gr.update_quality()
        self.assertEqual(-1, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(16, gr.items[0].quality) # decreases by 4

    def test_conjured_item_after_sell_date_quality_degrades_twice_as_fast(self):
        gr = self.factory("Conjured Mana Cake", -1, 20)
        gr.update_quality()
        self.assertEqual(-2, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(16, gr.items[0].quality) # decreases by 4

    def test_conjured_item_of_zero_quality(self):
        gr = self.factory("Conjured Mana Cake", 5, 0)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(0, gr.items[0].quality) # stays the same, quality never negative

    def test_conjured_item_of_quality_near_zero(self):
        gr = self.factory("Conjured Mana Cake", 5, 1)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 2, 1 each day
        self.assertEqual(0, gr.items[0].quality) # quality min capped at 0

    def test_conjured_item_of_quality_near_max(self):
        gr = self.factory("Conjured Mana Cake", 5, 49)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(47, gr.items[0].quality) # decreases by 2

    def test_conjured_item_of_max_quality(self):
        gr = self.factory("Conjured Mana Cake", 5, 50)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(48, gr.items[0].quality) # decreases by 2

    def test_conjured_item_of_quality_greater_than_max(self):
        gr = self.factory("Conjured Mana Cake", 5, 51)
        gr.update_quality()
        self.assertEqual(4, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(48, gr.items[0].quality) # decreases by 2 from max cap 50

    def test_conjured_item_of_quality_greater_than_max_at_sell_in_zero(self):
        gr = self.factory("Conjured Mana Cake", 0, 51)
        gr.update_quality()
        self.assertEqual(-1, gr.items[0].sell_in) # decreases by 1
        self.assertEqual(46, gr.items[0].quality) # decreases by 4 from max cap 50

    ############################### END TESTS ##################################

        
if __name__ == '__main__':
    unittest.main()
