import os
import ydb
import ydb.iam
from dotenv import load_dotenv
from helper import *
load_dotenv()

driver = ydb.Driver(
  endpoint=os.getenv('YDB_ENDPOINT'),
  database=os.getenv('YDB_DATABASE'),

  #credentials=ydb.iam.MetadataUrlCredentials(),)
  #credentials=ydb.AccessTokenCredentials(os.getenv('YDB_CREDINTALS_TOKEN')))
  credentials=ydb.iam.ServiceAccountCredentials.from_file(
           os.getenv("SA_KEY_FILE")
        ))
# Wait for the driver to become active for requests.G
driver.wait(fail_fast=True, timeout=5)
# Create the session pool instance to manage YDB sessions.
pool = ydb.SessionPool(driver)

def truncate_string(string, max_length):
    if len(string.encode('utf-8')) > max_length:
        return string[:max_length]
    else:
        return string


intList = ['all_token', 'all_messages', 'time_epoh', 'token', 'stock_id','id'
           ,'num_order','strategia','user_id','strateg','deal_id','strategia',
           'leadID','lead_id']

floatList = ['token_price','amount','price_open',
              'price_insert','price_close','need_price_close','bb_bu',
              'rate_change', 'lower_price', 'upper_price','need_price_close','price_open',
              'persent_ot_depo','depo', 'depo_deals','commission','cred_plecho','stop_loss','all_price']

dateTimeList = ['date_time','date_close','need_data_close','date_open', 'date_open','deal_id','time_last_mess'] 
class Ydb:
    def replace_query(self, tableName: str, rows: dict):
        field_names = rows.keys()
        fields_format = ", ".join(field_names)
        my_list = list(rows.values())
    
        value = '('
        #for i in my_list:
        for key, value1 in rows.items():
            try:
                value1 = value1.replace('"',"'")    
            except:
                1 + 0
            
            #TODO переделать под разные форматы
            value1 = truncate_string(str(value1), 2000)            
            if key == 'id':
                value += f'{value1},'

            elif key in intList:
                value += f'{int(value1)},'
            
            elif key in floatList:
                value += f'{float(value1)},'
            
            elif key in dateTimeList:
                value += f'CAST("{value1}" AS datetime ),'
            else:
                value += f'"{value1}",'
            
        value = value[:-1] + ')'
        # values_placeholder_format = ', '.join(my_list)
        query = f"REPLACE INTO `{tableName}` ({fields_format}) VALUES {value}"
        print(query)
        def a(session):
            session.transaction(ydb.SerializableReadWrite()).execute(
            #session(ydb.SerializableReadWrite()).execute(
                query,
                commit_tx=True,
            )
        return pool.retry_operation_sync(a)

    def update_query(self, tableName: str, rows: dict, where: str):
        # 'where id > 20 '
        field_names = rows.keys()
        fields_format = ", ".join(field_names)
        my_list = list(rows.values())
        sets = ''
        for key, value in rows.items():
            if key in ['ID']:
                continue
            if key in floatList:
                sets += f'{key} = {float(value)},'
            elif key in intList:
                sets += f'{key} = {int(value)},'
            
            elif key in dateTimeList:
                sets += f'{key} = CAST("{value}" AS datetime ),' 
            
            else:
                sets += f'{key} = "{value}",'

        sets = sets[:-1]

        # values_placeholder_format = ', '.join(my_list)
        query = f'UPDATE {tableName} SET {sets} WHERE {where}'
        # query = f"INSERT INTO {tableName} ({fields_format}) " \
        print(query)

        def a(session):
            session.transaction(ydb.SerializableReadWrite()).execute(
                query,
                commit_tx=True,
            )
        return pool.retry_operation_sync(a)

    def plus_query_user(self, tableName: str, rows: dict, where: str):
        # 'where id > 20 '
        """складывает предыдущие значения row с новыми"""
        get = self.select_query(tableName, where)[0]
        row = 0
        try:
            get = {'all_price': float(get['all_price']), 'all_token': int(get['all_token']), 'all_messages':int(get['all_messages'])}
        except Exception as e:
            print('e', e)
            get = {'all_price': 0, 'all_token': 0, 'all_messages': 0}
        try:
            row = sum_dict_values(get, rows)
        except Exception as e:
            print('ошибка',e)
            row = rows
        print(f'{get=}') 
        print(f'{row=}') 
        self.update_query(tableName, row, where)

    def delete_query(self, tableName: str, where: str):
        # 'where id > 20 '
        query = f"DELETE FROM `{tableName}` WHERE {where}"
        #print(query)

        def a(session):
            session.transaction(ydb.SerializableReadWrite()).execute(
                query,
                commit_tx=True,
            )
        return pool.retry_operation_sync(a)

    def create_table(self, tableName: str, fields: dict):
        # fields = {'id': 'Uint64', 'name': 'String', 'age': 'Uint64'}
        query = f"CREATE TABLE `{tableName}` ("
        for key, value in fields.items():
            query += f'{key} {value},'

        query = query[:-1] + ', PRIMARY KEY (id) ) '
        #print('CREATE TABLE',tableName)
        print(query)
        def a(session):
            session.execute_scheme(
                query,
                )
        return pool.retry_operation_sync(a)


    def insert_query(self, tableNameUserID: str, rows: dict):
        field_names = rows.keys()
        fields_format = ", ".join(field_names)
        my_list = list(rows.values())
    
        value = '('
        #for i in my_list:
        for key, value1 in rows.items():
            try:
                value1 = value1.replace('"',"'")    
            except:
                1 + 0
            
            #TODO переделать под разные форматы
            value1 = truncate_string(str(value1), 2000)            
            if key == 'id':
                value += f'{value1},'

            elif key in ['all_token', 'all_messages', 'time_epoch', 'token',]:
                value += f'{int(value1)},'
            
            elif key in ['token_price']:
                value += f'{float(value1)},'
            else:
                value += f'"{value1}",'
            
        value = value[:-1] + ')'
        # values_placeholder_format = ', '.join(my_list)
        query = f"INSERT INTO `{tableNameUserID}` ({fields_format}) VALUES {value}"
        print(query)
        def a(session):
            session.transaction(ydb.SerializableReadWrite()).execute(
            #session(ydb.SerializableReadWrite()).execute(
                query,
                commit_tx=True,
            )
        return pool.retry_operation_sync(a)

    def get_context(self, tableNameUserID: str, whereModelDialog: str):
        query = f"""SELECT * FROM `{tableNameUserID}` where MODEL_DIALOG = "{whereModelDialog}" """
        #print(query)
        def a(session):
            return session.transaction().execute(
                query,
                commit_tx=True,
            )
        b = pool.retry_operation_sync(a)
        # string = b_string.decode('utf-8')
        # IndexError: list index out of range если нет данныйх
        #print('b',b)
        rez = b[0].rows
        #print('rez',rez)
        context = ''
        for i in rez:
            context += i['TEXT'].decode('utf-8')+ '\n'
        print('context',context)
        return context
    
    def set_payload(self, userID: int, entity:str):
        query = f'UPDATE user SET payload = "{entity}" WHERE id = {userID}'
        #print(query)
        def a(session):
            session.transaction(ydb.SerializableReadWrite()).execute(
                query,
                commit_tx=True,
            )
        return pool.retry_operation_sync(a)


    def get_payload(self, whereID: int):
        query = f'SELECT payload FROM user WHERE id = {whereID}'
        print(query)

        def a(session):
            return session.transaction().execute(
                query,
                commit_tx=True,
            )
        b = pool.retry_operation_sync(a)
        if b[0].rows == []:
            return ''
        else:
            rez = b[0].rows[0]['payload'].decode()
        
        return rez
    
    def get_leadID(self, whereID: int):
        query = f'SELECT lead_id FROM user WHERE id = {whereID}'
        print(query)

        def a(session):
            return session.transaction().execute(
                query,
                commit_tx=True,
            )
        b = pool.retry_operation_sync(a)
        rez = b[0].rows[0]['lead_id']
        return rez
    
    
    def select_query(self,tableName: str, where: str):
        # 'where id > 20 '
        query = f'SELECT * FROM {tableName} WHERE {where}'
        print(query)

        def a(session):
            return session.transaction().execute(
                query,
                commit_tx=True,
            )
        b = pool.retry_operation_sync(a)
        # string = b_string.decode('utf-8')
        # IndexError: list index out of range если нет данныйх
        #print('b',b)
        rez = b[0].rows
        print('rez',rez)
        return rez

    
def handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }