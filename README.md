# Unofficial Grailed API

Simple method for querying [Grailed](https://www.grailed.com/). Currently it supports being able to search by designer, and the category size. The results can be returned as a json or a custom object GrailedListing object.

## Setup

`pip install git+https://github.com/andrewbeattie/gg.git`

Add enviroment variables.

```
URL=https://mnrwefss2q-dsn.algolia.net
API_KEY=api_key
APP_ID=app_id
MIN_PAGES=0
MAX_PAGES=5
HITS_PER_PAGE=100
```

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
