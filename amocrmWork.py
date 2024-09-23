from amocrm.v2 import tokens
from pprint import pprint
from dotenv import load_dotenv
import os
load_dotenv()

tokens.default_token_manager(
    client_id = os.environ.get('client_id_amocrm'),
    client_secret = os.environ.get('client_secret_amocrm'),
    # subdomain = "darkclaw921",
    subdomain = "profzabor",
    redirect_url = "https://functions.yandexcloud.net/d4e4rh9tdbt4igqcj37q",

    storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
)

tokens.default_token_manager.get_access_token()
# tokens.default_token_manager.init(code=os.environ.get('long_code'), skip_error=True)

from amocrm.v2 import Contact as _Contact, Company, Lead as _Lead, custom_field, filters, interaction, Event
# Event.
# a = interaction.BaseInteraction()
# row ={
#     'conversation_id':'12',
#     'source':{'external_id': '123'},
#     'user':{'id':'55', 'ref_id':'10167014','name':'testName',"profile": {
#             "phone": "79151112233",
#             "email": "example.client@example.com"
#         },}}
# row2= {
#     ''
# }
# b = a.request('/api/v4/leads','leads',)
# print(b)
# 1/0



class Lead(_Lead):
    record_text = custom_field.TextAreaCustomField("record text")
    # noAnswerBot = custom_field.CheckboxCustomField('Не отвечать ботом',code='391359')
    urlChatRoom = custom_field.UrlCustomField('Чат с клиентом',code='776947')
    trafickPath = custom_field.TextAreaCustomField('Источник трафика',code='317031')
    calcUrl = custom_field.UrlCustomField('Документ расчета',code='784929')
    # phone1 = custom_field.ContactPhoneField('phone')


class Contact(_Contact):
    phone = custom_field.ContactPhoneField('phone')
    # dealID = custom_field('linked_leads')


def create_lead(userName, userID):
    # data = {'name'}

    lead = Lead()
    lead.name = f'Клиент {userName} из Telegram'
    # lead.record_text = f'http://myservice.ai-akedemi.ru/room/{userID}'
    lead.urlChatRoom = f'http://159.223.37.145:5004/room/{userID}'
    lead.trafickPath = 'Telegram'
    lead.pipeline=7810518
    # status=66443482 # не завершил просчет
    leadID = lead.save()
    return leadID.id
    # Lead.create(name=userName)
    # Lead.save()

def create_contact(userName, phone:str):
    # data = {'name'}
    contact=Contact.objects.get(query=phone)
    if contact is not None:
        return contact.id
    contact = Contact()
    # contact.name = f'Клиент {userName} из Telegram'
    contact.name = f'{userName}'
    contact.phone= phone
    # lead.record_text = f'http://myservice.ai-akedemi.ru/room/{userID}'
    
    contactID = contact.save()
    return contactID.id

def get_leadID_from_contact(phone:str):
    conta = Contact.objects.get(query=phone)
    try:
        leadID = conta.leads._data[0]['id']
    except:
        leadID=0
    # leadID = conta.leads._data
    return leadID
    # lead = Lead.objects.get(f'{leadID}')


def update_lead_contact(leadID, contactID):

    # conta = Contact.objects.get(query='89308316687')
    # conta = Contact.objects.get(query=phone)
    # leadID = conta.leads._data[0]['id']
    # leadID = conta.leads._data[0]['id']
    lead = Lead.objects.get(f'{leadID}')
    # print(lead)

    # lead.lead_card_budget=12448222
    # lead.record_text = """Менеджер провел успешный разговор с клиентом, который интересуется установкой забора между соседями. Он предложил разные варианты и предоставил информацию о материалах и ценах.
    # pprint(lead.__dict__)
    # lead.__dict__['_data']['_embedded']['contacts'] = [contactID]
    # contact = Contact.objects.get(f'{contactID}')
    contact = Contact.objects.get(f'{contactID}')
    # pprint(contact.__dict__)
    contact.leads.append(lead)
    # lead.company = Company(name="Amocrm")
    # lead.contacts=[contactID]

    # lead.record_text = text
    lead.save()



def update_status_lead(leadID, statusID):
    """66443482 - не завершил просчет
    64333482 - посчитан с контактом"""
    lead = Lead.objects.get(f'{leadID}')
    lead.status = statusID
    lead.save()

def update_pipeline_lead(leadID, pipelineID):
    """
    7810518 - чат боты
    1724242 - клиенты
    """
    lead = Lead.objects.get(f'{leadID}')
    lead.pipeline = pipelineID
    lead.save()

def check_need_answered_for(leadID:int):
    lead = Lead.objects.get(f'{leadID}')
    if lead.noAnswerBot is None:
        return True 
    else:
        return False

def update_lead_url_to_calc(leadID:int, url:str):
    lead = Lead.objects.get(f'{leadID}')
    lead.calcUrl = url
    lead.save()

if __name__ ==  '__main__':
    # update_lead('640073', 'test text2')
    # a = get_leadID_from_contact('79636201537')
    # print(a)
    pass
    # create_lead('igor',12414245)
    # update_status_lead('26613047', 64333482)
    # update_lead_contact(26615083, 42615427)
    # contact_add_lead(42615427, 26615083)
    # a = check_need_answered_for(leadID=435263)
    # print(a)
    # lead.record_text = 'text'
    # lead.save()
