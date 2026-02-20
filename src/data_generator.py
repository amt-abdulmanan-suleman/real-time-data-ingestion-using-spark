import csv
import os
import random
import time
from datetime import datetime, timezone
from uuid import uuid4

OUTPUT_DIR = "streaming_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PRODUCTS = [
    {"product_id": 1, "name": "Laptop", "price": 1200},
    {"product_id": 2, "name": "Phone", "price": 800},
    {"product_id": 3, "name": "Headphones", "price": 150},
    {"product_id": 4, "name": "Keyboard", "price": 100},
]

EVENT_TYPES = ["view", "purchase"]

def generate_event():
    product = random.choice(PRODUCTS)
    return {
        "event_id": str(uuid4()),
        "user_id": random.randint(1000, 5000),
        "product_id": product["product_id"],
        "product_name": product["name"],
        "event_type": random.choice(EVENT_TYPES),
        "price": product["price"],
        "event_time": datetime.now(timezone.utc).isoformat()
    }

def write_csv():
    file_name = f"{OUTPUT_DIR}/events_{int(time.time())}.csv"

    with open(file_name, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "event_id",
            "user_id",
            "product_id",
            "product_name",
            "event_type",
            "price",
            "event_time"
        ])
        writer.writeheader()

        for _ in range(20):  # 20 events per batch
            writer.writerow(generate_event())

    print(f"Generated: {file_name}")

if __name__ == "__main__":
    while True:
        write_csv()
        time.sleep(20)
