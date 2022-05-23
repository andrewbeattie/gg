# Unofficial Grailed API

Simple method for querying [Grailed](https://www.grailed.com/). Currently it supports being able to search by designer, and the category size. The results can be returned as a json or a custom object GrailedListing object.

## Setup

`pip install git+https://github.com/andrewbeattie/gg.git`

## Usage

```
import os
from grailed.api import GrailedSearch

gs = GrailedSearch()
gs.add_designer(designer="Carol Christian Poell")
gs.add_size(category="footwear", size="6.5")
gs.add_size(category="footwear", size="7")
gs.query()
listings = gs.itemize()
for l in listings:
    print(l)
```
