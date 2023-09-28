
import workYDB 
from createKeyboard import *

pokrytie = {'odnostoronee':'Одностороннее', 
        'dvystoronee':'Двухстороннее',
        'otsincovonoe':'Оцинкованное',
        'woodOdnostoronee':'Имитация дерева/односторонняя',
        'woodDvystoronee':'Имитация дерева/двухсторонняя',
    }
porydok = {'normal':'Обычный', 
        'chees':'Шахматный',
    }

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
    
    '3': {'text': 'Выберите толщину:',
        'keyboard':create_inlinekeyboard_is_row({'0.3mm':'profNastil_0.3', 
                                                 '0.35mm':'profNastil_0.35',
                                                 '0.4mm':'profNastil_0.4',
                                                 '0.45mm':'profNastil_0.45',
                                                 '0.5mm':'profNastil_0.5',
                                                 })},
    '4': {'text': 'Выберите покрытие:',
        'keyboard':create_inlinekeyboard_is_row({'Одностороннее':'profNastil_odnostoronee', 
                                                 'Двухстороннее':'profNastil_dvystoronee',
                                                 'Оцинкованное':'profNastil_otsincovonoe',
                                                 'Имитация дерева/односторонняя':'profNastil_woodOdnostoronee',
                                                 'Имитация дерева/двухсторонняя':'profNastil_woodDvystoronee',
                                                 })},

    '5': {'text': 'Количество ворот',
        'keyboard': None},
    
    '6': {'text': 'Количество калиток',
        'keyboard': None},

    '7': {'text': 'Расстояние от МКАД',
        'keyboard': None},
}

questionEvroShtak = {
    '1': {'text':'Общая длина забора',
        'keyboard': None},
    
    '2': {'text':'Высота забора',
          'keyboard':create_inlinekeyboard_is_row({'1.5m':'evroShtak_1.5', 
                                                 '1.8m':'evroShtak_1.8',
                                                 '2m':'evroShtak_2',
                                                 '2.2m':'evroShtak_2.2',
                                                 '2.5m':'evroShtak_2.5',
                                                 '3m':'evroShtak_3',
                                                 })},
    
    '3': {'text': 'Порядок штакетин в заборе из евроштакетника:',
        'keyboard':create_inlinekeyboard_is_row({'Обычный':'evroShtak_normal', 
                                                 'Шахматный':'evroShtak_chees',
                                            
                                                 })},
    # '3': {'text': 'Выберите толщину:',
    #     'keyboard':create_inlinekeyboard_is_row({'0.3mm':'evroShtak_0.3', 
    #                                              '0.35mm':'evroShtak_0.35',
    #                                              '0.4mm':'evroShtak_0.4',
    #                                              '0.45mm':'evroShtak_0.45',
    #                                              '0.5mm':'evroShtak_0.5',
    #                                              })},

    '4': {'text': 'Выберите покрытие:',
        'keyboard':create_inlinekeyboard_is_row({'Одностороннее':'evroShtak_odnostoronee', 
                                                 'Двухстороннее':'evroShtak_dvystoronee',
                                                 'Имитация дерева/односторонняя':'evroShtak_woodOdnostoronee',
                                                 'Имитация дерева/двухсторонняя':'evroShtak_woodDvystoronee',
                                                 })},

    '5': {'text': 'Количество ворот',
        'keyboard': None},
    
    '6': {'text': 'Количество калиток',
        'keyboard': None},

    '7': {'text': 'Расстояние от МКАД',
        'keyboard': None},
}