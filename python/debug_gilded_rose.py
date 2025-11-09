#!/usr/bin/env python3
"""Simple driver to run and debug GildedRose.update_quality from the terminal.

Usage examples (from repo root):
  # run with the repo venv python (recommended)
  /Users/krsreddy/Documents/interviewes/GildedRose-Refactoring-Kata/venv/bin/python python/debug_run.py \
      -i "Normal Item,5,10" -i "Backstage passes to a ANY concert,15,35" -d 3

  # drop into pdb before each update step
  /Users/krsreddy/Documents/interviewes/GildedRose-Refactoring-Kata/venv/bin/python python/debug_run.py -i "Normal Item,5,10" -d 2 --pdb

  # run under the Python debugger to step into lines
  /Users/krsreddy/Documents/interviewes/GildedRose-Refactoring-Kata/venv/bin/python -m pdb python/debug_run.py -i "Normal Item,5,10" -d 2

This script prints the items state before and after each day so you can inspect changes.
Use --step to pause between days for manual inspection, or --pdb to drop into pdb before each update.
"""

import argparse
from gilded_rose import Item, GildedRose
import sys


def parse_item(text: str) -> Item:
    """Parse a single item spec: 'name,sell_in,quality'"""
    parts = [p.strip() for p in text.split(',')]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Item must be 'name,sell_in,quality'")
    name = parts[0]
    try:
        sell_in = int(parts[1])
        quality = int(parts[2])
    except ValueError:
        raise argparse.ArgumentTypeError('sell_in and quality must be integers')
    return Item(name, sell_in, quality)


def items_to_lines(items: list[Item]) -> list[str]:
    return [f"{item.name}, {item.sell_in}, {item.quality}" for item in items]


def main(argv=None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description='Run and debug GildedRose.update_quality')
    p.add_argument('-i', '--item', action='append', type=parse_item,
                   help="Item spec 'name,sell_in,quality' (can be repeated)")
    p.add_argument('-d', '--days', type=int, default=1, help='Number of days to simulate')
    p.add_argument('--pdb', action='store_true', help='Drop into pdb before each update')
    p.add_argument('--step', action='store_true', help='Pause and wait for Enter between days')
    args = p.parse_args(argv)

    if not args.item:
        print('No items supplied; using example items')
        items = [
            Item('Normal Item', 5, 10),
            Item('Aged Brie', 2, 0),
            Item('Sulfuras, Hand of Ragnaros', 0, 80),
            Item('Backstage passes to a TAFKAL80ETC concert', 15, 20),
            Item('Conjured Mana Cake', 3, 6),
        ]
    else:
        items = args.item

    gr = GildedRose(items)

    print('\nInitial items:')
    for line in items_to_lines(gr.items):
        print('  ' + line)

    for day in range(1, args.days + 1):
        print(f'\n=== Day {day} - before update ===')
        for line in items_to_lines(gr.items):
            print('  ' + line)

        if args.pdb:
            import pdb
            print('\nEntering pdb before calling update_quality() - use n/s to step, p to print variables')
            pdb.set_trace()

        # method to debug iteratively
        gr.update_quality()

        print(f'\n=== Day {day} - after update ===')
        for line in items_to_lines(gr.items):
            print('  ' + line)

        if args.step:
            input('\nPress Enter to continue to next day...')


if __name__ == '__main__':
    main()

# When pdb starts you can use commands:

# n (next) — execute next line

# s (step) — step into function call (useful to step into update_quality)

# l (list) — show source

# p <expr> — print expression, e.g. p gr.items or p item.quality

# b <file>:<lineno> — set breakpoint

# c — continue until next breakpoint or end

# Run under the full pdb module (start the script under pdb, letting you step from program start):

# python debug_run.py -i "Normal Item,5,10" -d 3 --pdb
# python debug_run.py -i "Normal Item,5,10" -d 3 --step
# End of file debug_run.py