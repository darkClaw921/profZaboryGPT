

from pyclm.logging import Logger
import os
from dotenv import load_dotenv
load_dotenv()

service_account_id = os.environ.get('LOGGER_SERCICE_ACCOUNT_ID')
key_id = os.environ.get('LOGGER_KEY_ID')
private_key = os.environ.get('LOGGER_PRIVATE_KEY')


def logg(nameDir:str, nameFile:str,):
    log = Logger(
        resource_type=nameDir,
        resource_id=nameFile,

        log_group_id='e23o1p6m0l0s0cqiagqo',
        credentials={
            "service_account_key": {
                "service_account_id": service_account_id,
                "id": key_id,
                "private_key": private_key
            }
        }
    )
    return log
# Logger(
#     resource_type='application',
#     resource_id='testLogg',

#     log_group_id='e23o1p6m0l0s0cqiagqo',
#     credentials={
#         "service_account_key": {
#             "service_account_id": service_account_id,
#             "id": key_id,
#             "private_key": private_key
#         }
#     }
# )

# log.critical("critical")
# log.warning('warning')
# log.debug('debug')
# log.trace('trace')
# log.error('error')
# log.debug('debug1',any_json={"ch_ru": "Яндекс", "ch_en": "Yandex", "cloud": {"logging": 5, "service": 0}},any_list=["А", "B", 0, 1, 0.123, None] )
