
import workYDB 
from createKeyboard import *

pokrytie = {1:'Одностороннее', 
        2:'Двухстороннее',
        3:'Оцинкованное',
        4:'Имитация дерева/односторонняя',
        5:'Имитация дерева/двухсторонняя',
    }
porydok = {1:'Обычный', 
        2:'Шахматный',
    }

questionProfNastil = {
    1: {'text':'Общая длина забора',
        'keyboard': None},
    
    2: {'text':'Высота забора',
          'keyboard':{1:'1.5m', 
                    2:'1.8m',
                    3:'2m',
                    4:'2.2m',
                    5:'2.5m',
                    6:'3m',
                    }},
    
    3: {'text': 'Выберите толщину:',
        'keyboard':{1:'0.3mm', 
                    2:'0.35mm',
                    3:'0.4mm',
                    4:'0.45mm',
                    5:'0.5mm',
                    }},
    4: {'text': 'Выберите покрытие:',
        'keyboard':{1:'Одностороннее', 
                    2:'Двухстороннее',
                    3:'Оцинкованное',
                    4:'Имитация дерева/односторонняя',
                    5:'Имитация дерева/двухсторонняя',
                    }},

    5: {'text': 'Количество ворот',
        'keyboard': None},
    
    6: {'text': 'Количество калиток',
        'keyboard': None},

    7: {'text': 'Расстояние от МКАД',
        'keyboard': None},
}

questionEvroShtak = {
    1: {'text':'Общая длина забора',
        'keyboard': None},
    
    2: {'text':'Высота забора',
          'keyboard':{1:'1.5m', 
                        2:'1.8m',
                        3:'2m',
                        4:'2.2m',
                        5:'2.5m',
                        6:'3m',
                        }},
    
    3: {'text': 'Порядок штакетин в заборе из евроштакетника:',
        'keyboard':{1:'Обычный', 
                    2:'Шахматный',
                    }},
    # '3': {'text': 'Выберите толщину:',
    #     'keyboard':create_inlinekeyboard_is_row({'0.3mm':'evroShtak_0.3', 
    #                                              '0.35mm':'evroShtak_0.35',
    #                                              '0.4mm':'evroShtak_0.4',
    #                                              '0.45mm':'evroShtak_0.45',
    #                                              '0.5mm':'evroShtak_0.5',
    #                                              })},

    4: {'text': 'Выберите покрытие:',
        'keyboard':{1:'Одностороннее', 
                    2:'Двухстороннее',
                    3:'Имитация дерева/односторонняя',
                    4:'Имитация дерева/двухсторонняя',
                    }},

    5: {'text': 'Количество ворот',
        'keyboard': None},
    
    6: {'text': 'Количество калиток',
        'keyboard': None},

    7: {'text': 'Расстояние от МКАД',
        'keyboard': None},
}
questionTypeMaterial = {
    1: 'Профнастил',
    2: 'Евроштакетник',
}
