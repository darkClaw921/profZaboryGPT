
import workYDB 
from createKeyboard import *
sql = workYDB.Ydb()

questionProfNastil = {
    '1': {'text':'Общая длина забора',
        'keyboard': None},
    
    '2': {'text':'Высота забора',
          'keyboard':create_inlinekeyboard_is_row({'1.5m':'profNastil_1.5', 
                                                 '1.8m':'profNastil_1.8',
                                                 '2m':'profNastil_2',
                                                 '2.2m':'profNastil_2.2',
                                                 '2.5m':'profNastil_2.5',
                                                 '3m':'profNastil_3',
                                                 })},
    
    '3': {'text': 'Выберите толщину и покрытие:',
        'keyboard':create_inlinekeyboard_is_row({'0.3mm':'profNastil_0.3', 
                                                 '0.35mm':'profNastil_0.35',
                                                 '0.4mm':'profNastil_0.4',
                                                 '0.45mm':'profNastil_0.45',
                                                 '0.5mm':'profNastil_0.5',
                                                 })},
    '4': {'text': 'Количество ворот',
        'keyboard': None},
    
    '5': {'text': 'Количество калиток',
        'keyboard': None},

    '6': {'text': 'Расстояние от МКАД',
        'keyboard': None},
}