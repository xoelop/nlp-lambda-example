import os
from collections import Counter
from typing import List

import spacy

from src.manage_models import get_model_from_disk

model = os.environ['SPACY_MODEL_MEDIUM']
model_sm = os.environ['SPACY_MODEL_SMALL']
 
model_location = get_model_from_disk(model)

nlp = spacy.load(model_location)


def find_locations(text: str) -> List[str]:
    doc = nlp(text)
    location_labels = ['GPE', 'LOC']
    location_list = [ent.text for ent in doc.ents if ent.label_ in location_labels]
    locations_sorted_by_num_appearances = list(Counter(location_list).keys())
    return locations_sorted_by_num_appearances
