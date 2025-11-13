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
