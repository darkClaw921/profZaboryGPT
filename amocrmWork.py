from amocrm.v2 import tokens
from pprint import pprint
from dotenv import load_dotenv
import os
load_dotenv()

tokens.default_token_manager(
    client_id = os.environ.get('client_id_amocrm'),
    client_secret = os.environ.get('client_secret_amocrm'),
    subdomain = "darkclaw921",
    redirect_url = "https://functions.yandexcloud.net/d4e4rh9tdbt4igqcj37q",

    storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
)
# tokens.default_token_manager.init(code="12", skip_error=True)
tokens.default_token_manager.get_access_token()
from amocrm.v2 import Contact as _Contact, Company, Lead as _Lead, custom_field, filters
class Lead(_Lead):
    record_text = custom_field.TextAreaCustomField("record text")
    # phone1 = custom_field.ContactPhoneField('phone')

class Contact(_Contact):
    phone1 = custom_field.ContactPhoneField('phone')
    # dealID = custom_field('linked_leads')


# lead = Lead.objects.filter(phone='',{'phone':'89308316687'})
# filters.Filter('phone')('89308316687')
# filter='phone:8908316655'
# lead = Lead.objects.get(query='phone_number:89308316687')
conta = Contact.objects.get(query='89308316687')
# a = Contact._get_embedded_fields()
# pprint(a)
# pprint(conta.name)
# pprint(conta.linked_leads)
leadID = conta.leads._data[0]['id']
lead = Lead.objects.get(f'{leadID}')
# lead = Lead.objects.filter(filters=filters.Filter(Contact.phone1)('89308316687'))
# lead = Lead.objects.filter(filters=(filters.MultiFilter('contacts')('custom_fields_values')('field_code')('PHONE')('values')('89308316687'),filters.MultiFilter('custom_fields_values')('field_code')))
print(lead)
# for l in lead:
#     print(l)
# print(lead[0])

lead.lead_card_budget=12448222
lead.record_text = """Менеджер провел успешный разговор с клиентом, который интересуется установкой забора между соседями. Он предложил разные варианты и предоставил информацию о материалах и ценах.

Что было сделано хорошо:

Менеджер вежливо и профессионально представил себя и компанию.

Он внимательно выслушал потребности клиента и задал уточняющие вопросы.

Менеджер предложил разные варианты забора и предоставил ценовые расчеты.

Он уточнил местоположение участка и рассчитал стоимость с учетом доставки.

Менеджер объяснил процесс замера и подготовки к установке.

Он был готов скинуть расчеты и визитку компании через WhatsApp для дальнейшего обсуждения.

Что можно улучшить:

Менеджер мог бы уточнить у клиента его контактные данные (номер телефона) для более удобной связи и отправки информации.

Необходимо следить за четкостью и точностью предоставляемой информации, чтобы избежать недоразумений.

Менеджер мог бы предоставить более подробную информацию о сроках и гарантиях выполнения работ.

В целом, менеджер продемонстрировал хорошее внимание к клиенту и его потребностям, а также готовность предоставить информацию для принятия решения."""
lead.save()
# print(a)


