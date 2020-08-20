import re
from collections import Counter
from typing import List
from src.manage_models import get_model_from_disk

import spacy

model = 'en_core_web_md-2.3.1'
# model = 'en_core_web_sm-2.3.1'

model_location = get_model_from_disk(model)

nlp = spacy.load(model_location)


def find_locations(text: str) -> List[str]:
    doc = nlp(text)
    location_labels = ['GPE', 'LOC']
    location_list = [ent.text for ent in doc.ents if ent.label_ in location_labels]
    locations_sorted_by_num_appearances = list(Counter(location_list).keys())
    return locations_sorted_by_num_appearances
