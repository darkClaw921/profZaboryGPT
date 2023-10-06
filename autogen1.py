# from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from flaml import autogen
# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample.json
# config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
# assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
# user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
# user_proxy.initiate_chat(assistant, message="Создай лид в crm bitrix24")
# This initiates an automated chat between the two agents to solve the task
llm_config = {
    'config_list': [{
        "model": "gpt-3.5-turbo-16k",
        'api_key': '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'
    }]
}
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
)
user_proxy = autogen.UserProxyAgent(
    name='user_proxy',
    human_input_mode='NEVER',
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
    max_consecutive_auto_reply=6,
    code_execution_config={
        "work_dir": "work_dir",
        "use_docker": False,
    }
)

# task1 = 'Создай лида в crm Bitrix24 с именем Игорь. Вот webhook https://dlatesta.bitrix24.ru/rest/1/jgakucc6m4awl9dr/'
# task1 = 'Загугли какой длиной маршрут от Липецк, улица Каменный Лог, 48 до Липецк, Советская улица, 64 на машине в киллометрах'
# task1 = 'создай локальное серверное приложение на python для Bitrix24 для отправки сообщений в открытую линию. Вот данные client_id=local.651d3df11b1b29.23428491 client_secret=IaIyw4ymXC14eWW3mc1zQeTtHKJCZmktl92WrxmJkE8yhNi72v,webhook=https://dlatesta.bitrix24.ru/rest/1/jgakucc6m4awl9dr/'
# task1 = 'создай таблицу с доступными акциями в клиниках Липецка с сайта https://prodoctorov.ru/lipeck/'

# task1 = 'получи баланс пользователя с биржи mexc вот данные api_key=mx0vglVu8XDFeIDUjk,secret_key=3c3b108ee0f545f095b87c136589330e'
# task1 = 'Напиши flask приложение которое получает данный из Mysql и строит графики на странице с возможностью выбирать диапозон данных'
# task1 = 'python используй библиотеку flask напиши локальное приложение которое строит графики на странице с возможностью выбирать диапозон данных'
task1 = """создай новую сделку в crm amocrm с именем Игорь. Вот данные client_id="2c736992-c61e-4e68-8d84-d59ebaeed215",
    client_secret="GOtwNCSeWtyRzl4CQcLHty5AhFV97SN1N6kcNNEkC4gNpxXfKgKlK1WmRQUnJMfJ",
    subdomain="darkclaw921",
    redirect_url="https://functions.yandexcloud.net/d4e4rh9tdbt4igqcj37q" """
text = user_proxy.initiate_chat(assistant, message=task1)
article_text = assistant.chat_messages[user_proxy]#[-3]['content']