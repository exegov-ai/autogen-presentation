#!/usr/bin/env python
# coding: utf-8

# ## NOTE This is not actual code used by exegov.ai
# This is simplified version to present the
# concept of sequential conversation between agents in autogen
# ## Setup

# In[]:
from utils import get_azure_openai_api_key, get_openai_base_url, get_openai_model, get_openai_api_version

AZURE_OPENAI_API_KEY = get_azure_openai_api_key()
OPENAI_BASE_URL = get_openai_base_url()
OPENAI_MODEL = get_openai_model()
OPENAI_API_VERSION = get_openai_api_version()

llm_config = {
    "model": OPENAI_MODEL,
    "api_key": AZURE_OPENAI_API_KEY,
    "base_url": OPENAI_BASE_URL,
    "api_version": OPENAI_API_VERSION,
    "api_type": "azure"
}

# In[]:


from autogen import ConversableAgent


# ## Creating the needed agents

# In[]:


everyday_assistant_agent = ConversableAgent(
    name="Everyday Assistant Agent",
    system_message='''You are a helpful everyday assistant for exegov.ai user.
    You ask user to remind you what is company name, stage and industry.
    Your job is to gather customer's process on his/her OKR(s) (Objective Key Results), \
    current priorities ask if we are aligned with roadmap.
    Do not ask for other information. Return 'TERMINATE' 
    when you have gathered all the information.''',
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)


# In[]:


strategy_agent = ConversableAgent(
    name="Strategy Agent",
    system_message='''You are a helpful strategy assistant for exegov.ai user.
    User is C-level person in a company.
    You ask customer if he/she want to update business plan, OKRs, \
    roadmap, lean canvas, 5 porter forces or any other information. \
    Do not ask for other information.
    Return 'TERMINATE' when you have gathered all the information.''',
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)


# In[]:


domains_agent = ConversableAgent(
    name="Domains Agent",
    system_message='''You are a helpful domains agent
    here to cheer up customer \
    while his/her documents are being updated by exegov.ai agents. \
    You can ask customer about what is the next domain we will talk about\
    You only allow customer to talk about: Strategy, HR, Legal and Finance. \
    Each domain has subcategories, for example Strategys has \
    Business Plan, OKRs, Roadmap, Lean Canvas, 5 Porter Forces. \
    Return 'TERMINATE' when you are done.''',
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
)


# In[]:


customer_proxy_agent = ConversableAgent(
    name="customer_proxy_agent",
    llm_config=False,
    code_execution_config=False,
    human_input_mode="ALWAYS",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
)


# ## Creating tasks
# 
# Now, you can see more or less how everyday conversation looks with sequence of agents.

# In[]:


chats = [
    {
        "sender": everyday_assistant_agent,
        "recipient": customer_proxy_agent,
        "message": "Could you also remind me name, stage, and industry we are in?",
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt" : "Return the customer information "
                             "into as JSON object only: "
                             "{'name': '', 'stage': '', 'industry': ''}",
        },
        "max_turns": 2,
        "clear_history" : True
    },
    {
        "sender": strategy_agent,
        "recipient": customer_proxy_agent,
        "message": 
            "Hi, could you provide me some updates how business is going?"
                "Shall we update our strategy?",
        "summary_method": "reflection_with_llm",
        "max_turns": 1,
        "clear_history" : False
    },
    {
        "sender": customer_proxy_agent,
        "recipient": domains_agent,
        "message": "Let's take a look at other domains",
        "max_turns": 1,
        "summary_method": "reflection_with_llm",
    },
]


# ## User was already onboarded in exegov.ai before,
# ## User logs in to update progress on the project, AI agents are here to help


# In[]:


from autogen import initiate_chats

chat_results = initiate_chats(chats)


# ## Print out the summary

# In[]:


for chat_result in chat_results:
    print(chat_result.summary)
    print("\n")


# ## Print out the cost

# In[]:


for chat_result in chat_results:
    print(chat_result.cost)
    print("\n")
