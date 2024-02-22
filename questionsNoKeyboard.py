
import workYDB 
from createKeyboard import *

pokrytie = {'0':'Одностороннее', 
        '1':'Двухстороннее',
        '2':'Оцинкованное',
        '3':'Имитация дерева/односторонняя',
        '4':'Имитация дерева/двухсторонняя',
    }
porydok = {'0':'Обычный', 
        '1':'Шахматный',
    }
LAST_QUESTION = 'Это конец вопросов секции'
questionProfNastil = {
    '1': {'text':'Длина (m)',
        'keyboard': None},
    
    '2': {'text':'Высота (m)',
          'keyboard':{'1.5':'profNastil_0', 
                    '1.8':'profNastil_1',
                    '2':'profNastil_2',
                    '2.2':'profNastil_3',
                    '2.5':'profNastil_4',
                    '3':'profNastil_5',
                    }},
    
    '3': {'text': 'Выберите толщину (mm)',
        'keyboard':{'0.3':'profNastil_0', 
                    '0.35':'profNastil_1',
                    '0.4':'profNastil_2',
                    '0.45':'profNastil_3',
                    '0.5':'profNastil_4',
                    }},
    '4': {'text': 'Выберите покрытие:',
        'keyboard':{'Одностороннее':'profNastil_0', 
                    'Двухстороннее':'profNastil_1',
                    'Оцинкованное':'profNastil_2',
                    'Имитация дерева/односторонняя':'profNastil_3',
                    'Имитация дерева/двухсторонняя':'profNastil_4',
                    }},

    '5': {'text': 'Количество ворот',
        'keyboard': None},
    
    '6': {'text': 'Количество калиток',
        'keyboard': None},

    '7': {'text': LAST_QUESTION,
        'keyboard': None},
}

questionGridRabit = {
    '1': {'text':'Длина (m)',
        'keyboard': None},
    
    '2': {'text':'Высота (m)',
          'keyboard':{'1.5':'GridRabit_0', 
                    '1.8':'GridRabit_1',
                    '2':'GridRabit_2',
                    }},
    
    '3': {'text': 'Количество протяжек арматуры:',
        'keyboard':{'1':'GridRabit_0', 
                    '2':'GridRabit_1',                                                
                    '0':'GridRabit_2',                                                
                    }},

    '4': {'text': 'Количество ворот',
        'keyboard': None},
    
    '5': {'text': 'Количество калиток',
        'keyboard': None},

    '6': {'text': LAST_QUESTION,
        'keyboard': None},
}

question3d = {
    '1': {'text':'Длина (m)',
        'keyboard': None},
    
    '2': {'text':'Высота (m)',
          'keyboard':{'1.53':'3d_0', 
                    '1.73':'3d_1',
                    '2.03':'3d_2',
                    }},

    '3': {'text': 'Количество ворот',
        'keyboard': None},
    
    '4': {'text': 'Количество калиток',
        'keyboard': None},

    # '5': {'text': 'Расстояние от МКАД',
    '5': {'text': LAST_QUESTION,
        'keyboard': None},
}

questionZaluzi = {
    '1': {'text':'Длина (m)',
        'keyboard': None},
    
    '2': {'text':'Высота (m)',
          'keyboard':{'1.5':'Zaluzi_0', 
                    '1.8':'Zaluzi_1',
                    '2':'Zaluzi_2',
                    '2.2':'Zaluzi_3',
                    '2.5':'Zaluzi_4',
                    }},

    '3': {'text': 'Количество ворот',
        'keyboard': None},
    
    '4': {'text': 'Количество калиток',
        'keyboard': None},

    '5': {'text': LAST_QUESTION,
        'keyboard': None},
}

questionEvroShtak = {
    '1': {'text':'Длина (m)',
        'keyboard': None},
    
    '2': {'text':'Высота (m)',
          'keyboard':{'1.5':'evroShtak_0', 
                    '1.8':'evroShtak_1',
                    '2':'evroShtak_2',
                    '2.2':'evroShtak_3',
                    '2.5':'evroShtak_4',
                #  '3m':'evroShtak_3',
                    }},
    
    '3': {'text': 'Порядок штакетин в заборе из евроштакетника:',
        'keyboard':{'Обычный':'evroShtak_0', 
                    'Шахматный':'evroShtak_1',
                    }},

    '4': {'text': 'Выберите покрытие:',
        'keyboard':{'Одностороннее':'evroShtak_0', 
                    'Двухстороннее':'evroShtak_1',
                    'Имитация дерева/односторонняя':'evroShtak_2',
                    'Имитация дерева/двухсторонняя':'evroShtak_3',
                    }},
    '5': {'text': 'Выберите зазор (mm)',
        'keyboard':{'0':'evroShtak_0', 
                    '1':'evroShtak_1',
                    '2':'evroShtak_2',
                    '3':'evroShtak_3',
                    '4':'evroShtak_4',
                    '5':'evroShtak_5',
                    '6':'evroShtak_6',
                    '7':'evroShtak_7',
                    '8':'evroShtak_8',
                    '9':'evroShtak_9',
                    '10':'evroShtak_10',
                    }},

    '6': {'text': 'Количество ворот',
        'keyboard': None},
    
    '7': {'text': 'Количество калиток',
        'keyboard': None},

    '8': {'text': LAST_QUESTION,
        'keyboard': None},
}

keys = list(questionProfNastil['2']['keyboard'].keys())
print(keys[0])