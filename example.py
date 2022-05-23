import os
from grailed.api import GrailedSearch

gs = GrailedSearch()
gs.add_designer(designer="Carol Christian Poell")
gs.add_size(category="footwear", size="6.5")
gs.add_size(category="footwear", size="7")
gs.add_designer(designer="Paul Harnden Shoemakers")
gs.add_size(category="outerwear", size="xs")
gs.add_size(category="outerwear", size="s")
gs.query()
listings = gs.itemize()
for l in listings:
    print(l)