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
# tokens.default_token_manager.init(code="", skip_error=True)

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
    noAnswerBot = custom_field.CheckboxCustomField('Не отвечать ботом',code='391359')
    # phone1 = custom_field.ContactPhoneField('phone')

class Contact(_Contact):
    phone = custom_field.ContactPhoneField('phone')
    # dealID = custom_field('linked_leads')

def get_leadID_from_contact(phone:str):
    conta = Contact.objects.get(query=phone)
    leadID = conta.leads._data[0]['id']
    return leadID
    # lead = Lead.objects.get(f'{leadID}')


def update_lead(phone:str, text:str):

    # conta = Contact.objects.get(query='89308316687')
    conta = Contact.objects.get(query=phone)
    leadID = conta.leads._data[0]['id']
    lead = Lead.objects.get(f'{leadID}')
    # print(lead)

    # lead.lead_card_budget=12448222
    # lead.record_text = """Менеджер провел успешный разговор с клиентом, который интересуется установкой забора между соседями. Он предложил разные варианты и предоставил информацию о материалах и ценах.
    lead.record_text = text
    lead.save()

def check_need_answered_for(leadID:int):
    lead = Lead.objects.get(f'{leadID}')
    if lead.noAnswerBot is None:
        return True 
    else:
        return False




if __name__ ==  '__main__':
    # update_lead('640073', 'test text2')
    a = check_need_answered_for(leadID=435263)
    print(a)
    # lead.record_text = 'text'
    # lead.save()
