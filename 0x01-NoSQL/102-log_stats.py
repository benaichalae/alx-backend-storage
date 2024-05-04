#!/usr/bin/env python3
"""adding the top 10 of the most present IPs in the collection"""
from pymongo import MongoClient


def log_stats():
    """Prints stats about Nginx request logs"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx
    total_logs = nginx_collection.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: nginx_collection.count_documents(
        {"method": method}
        ) for method in methods}
    status_check_count = nginx_collection.count_documents(
            {"method": "GET", "path": "/status"}
            )
    print("{} logs".format(total_logs))
    print("Methods:")
    for method in methods:
        print("\tmethod {}: {}".format(method, method_counts[method]))
    print("{} status check".format(status_check_count))

    ips = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for data in ips:
        print("\t{}: {}".format(data['_id'], data['count']))


if __name__ == "__main__":
    log_stats()
