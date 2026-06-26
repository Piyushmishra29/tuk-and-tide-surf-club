#!/usr/bin/env python3
"""Assemble all page partials (sorted) into build/book.html and note the order."""
import glob, os

here = os.path.dirname(os.path.abspath(__file__))
partials = sorted(glob.glob(os.path.join(here, "partials", "*.html")))

head = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Tuk & Tide Club — Brand Book</title>
<link rel="stylesheet" href="../assets/brand.css">
</head><body>
"""
body = "\n".join(open(p, encoding="utf-8").read().strip() for p in partials)
out = head + body + "\n</body></html>\n"
open(os.path.join(here, "book.html"), "w", encoding="utf-8").write(out)
print("Assembled %d partials:" % len(partials))
for p in partials:
    print("  -", os.path.basename(p))
