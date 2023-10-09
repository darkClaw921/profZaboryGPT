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

task1=''

text = user_proxy.initiate_chat(assistant, message=task1)
article_text = assistant.chat_messages[user_proxy]#[-3]['content']