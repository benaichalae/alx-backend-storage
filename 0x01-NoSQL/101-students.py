#!/usr/bin/env python3
"""function that returns all students sorted by average score"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """Prints all students in a collection sorted by average score"""
    dic_ = [
        {
            '$project': {
                '_id': 1,
                'name': 1,
                'topics': 1,
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {
                'averageScore': -1
            }
        }
    ]

    return list(mongo_collection.aggregate(dic_))


if __name__ == "__main__":
    log_stats()
