from rapidfuzz import fuzz, process

def get_best_match(query, items, key=lambda x: x["title"], threshold=80):
    choices = {f"{key(i)} ({i.get('releaseDate', '')[:4]})": i for i in items}
    match = process.extractOne(query, choices.keys(), scorer=fuzz.ratio)
    if match and match[1] >= threshold:
        return choices[match[0]]
    return None
