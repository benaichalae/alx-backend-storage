#!/usr/bin/env python3
"""
function that inserts a new
document in a collection based on kwargs
"""

def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection"""
    doc_insert = mongo_collection.insert_one(kwargs)
    return doc_insert.inserted_id
