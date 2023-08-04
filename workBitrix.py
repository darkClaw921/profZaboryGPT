from fast_bitrix24  import Bitrix
from dotenv import load_dotenv
import os
from pprint import pprint
from loguru import logger
from helper import *
import base64
from dataclasses import dataclass
load_dotenv()
webHook = os.environ.get('webHook')
bit = Bitrix(webHook)

class CRM():
    class lead():
        fileTelegram: str = 'UF_CRM_1690904694646'
        commentTelegram:str = 'UF_CRM_1689546544'

def deal_history():

    row = { 
        'entityTypeId': 2,
        'order': { "ID": "ASC" },
        'filter': { "OWNER_ID": 4089 },
        'select': [ "ID", "STAGE_ID", "CREATED_TIME",'STAGE_SEMANTIC_ID' ],
        'start': 2,
    }
    dealHist = bit.call("crm.stagehistory.list", row)
    pprint(dealHist)

def create_lead(items:dict):
    dealID = bit.call('crm.lead.add', items=items,raw=True)
    return dealID

def serch_lead_for_name(nicname:str)->int:
    """_summary_

    Args:
        nicname (str): _description_

    Returns:
        int: id лида
    """

    leads = bit.get_all(
    'crm.lead.list',
    params={
        #'select': ['*', 'UF_*'],
        'filter': {'NAME': nicname}
    })   
    if leads == []:
        return 0 
    else:
        return leads[0]['ID'] 


def update_deal(phone:str, text:str, nicname:str = 'Клиент из Telegram'):
    phone = phone.replace('8','+7',1)
    leads = bit.get_all(
    'crm.lead.list',
    params={
        #'select': ['*', 'UF_*'],
        'filter': {'PHONE': phone}
    })
    logger.info(f'{len(leads)=}')
    if len(leads) >= 1:
        params = {"ID": leads[0]['ID'], "fields": {CRM.lead.commentTelegram: text}}
        bit.call('crm.lead.update', params, raw=True)
    else:
        params = {"NAME": nicname, 
                  "fields": {CRM.lead.commentTelegram: text,
                             "PHONE":[{ "VALUE": phone, "VALUE_TYPE": "WORK" }]}}
        create_lead(params)
# добавить комментарий к задаче
    print(f'{leads=}')
    pass

def create_contact():
    pass

def get_lead(leadID):
    #lidID = 25957
    param = {'ID':leadID}
    a = bit.call('crm.lead.get',param)
    logger.info(a)
    return a

def update_lead(params):
    bit.call('crm.lead.update', params, raw=True)

def download_files_bitrix(lst:list):
    files = []
    for l in lst:
        filebit = download_file(f"https://scandiecodom.bitrix24.ru{l['downloadUrl']}")
        logger.error(filebit)
        file_base64 = read_file_as_base64(filebit)
        files.append({'fileData':[filebit, file_base64]})

def create_lead_and_attach_file(files:list, nicname:str):
    #downloadFolder = 'downloadsProject/'
    
    # if not os.path.exists(downloadFolder):
    #     os.makedirs(downloadFolder)
    uploadFiles = []
    for fileName in files:
        file_path = f'{fileName}'
        file_base64 = read_file_as_base64(file_path)
        uploadFiles.append({'fileData':[fileName, file_base64]})
    leadID = serch_lead_for_name(nicname) 
    print(leadID)
    if leadID == 0:
        params = {
        
        'fields': {
            "NAME": nicname,
        #'UF_CRM_1690904694646': [{'fileData':["Задача_Запрос_в_СТП__Доступ_РДП.png", file_base64]}]
            CRM.lead.fileTelegram: uploadFiles}
        }
        lid = create_lead(params)
        logger.error(f'создан лид {lid}')
    else:
        
        lead = get_lead(leadID)
        fileTelegram = lead[CRM.lead.fileTelegram]
        if fileTelegram != []:
            #a = download_files_bitrix(fileTelegram)
            #logger.error(a)
            uploadFiles.extend(fileTelegram)

        params = {
            "ID": f'{leadID}',

        #"NAME": nicname,
            'fields': {
                "NAME": nicname,
                #'UF_CRM_1690904694646': [{'fileData':[["Задача_Запрос_в_СТП__Доступ_РДП.png", file_base64],
                #                                      ["Задача_Запрос_в_СТП__Доступ_РДП2.png", file_base64]]}]}
                CRM.lead.fileTelegram: uploadFiles}
            } 
        update_lead(params)
        logger.error(f'обновлен лид {leadID}')

if __name__ == '__main__':
    #isk.file.get
    #fil = bit.call('disk.file.get', {'id':'169947'})
    #print(fil)
    #pass
    # file1 = bit.call(
    #     'disk.file.get',
    #     [{"id": 169947}])
    # print(file1)
    a = get_lead(25975)
    pprint(a)
    pass
   # create_lead_and_attach_file(['downloadsProject/file_14.png', 'downloadsProject/file_13.png'],'darkClaw921')
    
    #phone = '+79308316655'
#params = {"NAME": 'nicname', 
#                  "fields": {"UF_CRM_1689546544": 'text',
#                             "PHONE":[{'VALUE': phone, 'VALUE_TYPE': 'WORK'}]}}
                  
#create_lead(params)
#deal_history()
