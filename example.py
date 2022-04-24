import os
from grailed.api import GrailedSearch

gs = GrailedSearch()
gs.add_designer(designer="Carol Christian Poell")
gs.add_size(category="footwear", size="6.5")
gs._params()
gs.query()
print(gs.data[0])
