import time
import random

epoch = int(time.mktime(time.strptime("2023-01-01", "%Y-%m-%d")))


def generate_id():
    current_timestamp = int(time.time())
    random_part = random.randint(100, 999)
    timestamp_part = current_timestamp - epoch
    generate_user_id = f"{int(timestamp_part)}{int(random_part)}"
    return generate_user_id
