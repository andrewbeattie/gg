import os
import json
import requests
from typing import List
from dataclasses import dataclass

url = os.getenv("URL")

@dataclass
class GrailedListing:
    id: int
    designer:str
    color: str
    category:str
    size: str
    condition:str
    sold_price: float
    ask_price: float

class Grailed(requests.Session):
    def __init__(self):
        super().__init__()
        self._add_headers()

    def _add_headers(self):
        headers = {
            'Host': 'mnrwefss2q-dsn.algolia.net',
            'Origin': 'https://www.grailed.com',
            'accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'X-Algolia-API-Key': os.getenv("API_KEY", ""),
            'X-Algolia-Application-Id': os.getenv("APP_ID", ""),
            'hitsPerPage': os.getenv("HITS_PER_PAGE", 100)
        }
        self.headers.update(headers)

class GrailedFilters:
    def __init__(self):
        self.filters = {}
    
    def add_filters(self, key: str, values: List[str]):
        self.filters.update({key: values})

    def __str__(self):
        filters_list = []
        for key, values in self.filters.items():
            filters_list.append([f"{key}:{value}" for value in values])
        return json.dumps(filters_list)

class GrailedSearch(Grailed):
    def __init__(self, pages=range(int(os.getenv("MIN_PAGES", "0")), int(os.getenv("MAX_PAGES", "1")))):
        super().__init__()
        self.designers = []
        self.category_size = []
        self.pages = pages
        self.data = []
    def add_designer(self, designer: str):
        self.designers.append(f"{designer}")

    def add_size(self, category: str, size: str):
        self.category_size.append(f"{category}.{size}")

    def _params(self):
        self.facetFilters = GrailedFilters()
        if self.designers:
            self.facetFilters.add_filters(key="designers.name", values=self.designers)
        if self.category_size:
            self.facetFilters.add_filters(key="category_size", values=self.category_size)
        str(self.facetFilters)

    def query(self, sold=False):
        self._params()
        hits = 100
        self.listings = []
        for page in self.pages:
            params = f'page={page}&hitsPerPage={hits}&facetFilters={str(self.facetFilters)}'
            if sold:
                r = self.get(url + '/1/indexes/Listing_sold_production/', params=params)
            else:
                r = self.get(url + '/1/indexes/Listing_production/', params=params)
            if r.status_code == 200:
                data = r.json()
                page_listings = data['hits']
                self.listings.extend(page_listings)
                if len(data["hits"]) < 100:
                    break
            else:
                print(self.r.status_code)
        return self.listings

    def itemize(self):
        listings = []
        for listing in self.listings:
            grailed_listing = GrailedListing(
                id=listing.get("id"),
                designer=listing.get("designer", {"name": None}).get("name"),
                color=listing.get("color"),
                category=listing.get("category"),
                size=listing.get("size"),
                condition=listing.get("condition"),
                sold_price=listing.get("sold_price"),
                ask_price=listing.get("price")
            )
            listings.append(grailed_listing)
        return listings

    def _get_listings(self, designer:str):
        hits = 100
        master_list = []
        for page in self.pages:
            params = f'page={page}&hitsPerPage={hits}&facetFilters=[["category_size:footwear.6.5","category_size:footwear.7","category_size:footwear.7.5","category_size:outerwear.s","category_size:outerwear.xs","category_size:outerwear.xxs"],["designers.name:{designer}"]]'
            r = self.get(url + '/1/indexes/Listing_sold_production/', params=params)
            if r.status_code == 200:
                data = r.json()
                page_listings = data['hits']
                master_list.extend(page_listings)
                if len(data["hits"]) < 100:
                    break
            else:
                print(self.r.status_code)
        return master_list

    def _query(self):
        for designer in self.designers:
            print(designer)
            self.data.extend(self._get_listings(designer))

