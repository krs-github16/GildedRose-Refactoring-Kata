from enum import Enum

class ProductList(Enum):
    """Enumerated list of available products for easy reference."""

    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASS = "Backstage passes" # startswith , flexible for any concert
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    CONJURED = "Conjured" # startswith, flexible for any conjured item
