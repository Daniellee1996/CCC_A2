import time

def get_time():
    time_str = time.strftime("%Y-%M-%d %X")
    return time_str


if __name__ == "__main__":
    print(get_time())