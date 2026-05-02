import os
import time, pytz
from datetime import datetime
from dotenv import load_dotenv
from sending_messages import send_data
load_dotenv()
TIME_MESSAGES = [t.strip() for t in os.getenv("TIME_MESSAGES").split(",")]

def start():
    print("start")
    while True:
        time_zone = pytz.timezone("Asia/Irkutsk")
        now_irkutsk = datetime.now(time_zone)
        current_time_str = now_irkutsk.strftime("%H:%M")

        if current_time_str in TIME_MESSAGES and now_irkutsk.second == 0:
            send_data()
            # Не зайти в это же условие еще раз
            time.sleep(2)
        time.sleep(0.9)

if __name__ == "__main__":
    start()