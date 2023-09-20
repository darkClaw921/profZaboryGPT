
import workYDB 
from createKeyboard import *
sql = workYDB.Ydb()

questionProfNastil = {
    '1': {'text':'Общая длина забора',
        'keyboard': None},
    
    '2': {'text':'Высота забора',
          'keyboard': None},
    
    '3': {'text': 'Выберите толщину и покрытие:',
        'keyboard':create_inlinekeyboard_is_row({'0.2mm':'profNastil_0.2', 
                                                 '0.6mm':'profNastil_0.6'})},
    '4': {'text': 'Количество ворот',
        'keyboard': None},
    
    '5': {'text': 'Количество калиток',
        'keyboard': None},

    '6': {'text': 'Расстояние от МКАД',
        'keyboard': None},
}