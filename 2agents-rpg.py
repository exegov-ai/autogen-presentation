#!/usr/bin/env python
# coding: utf-8

# ## Setup

# In[ ]:

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

# ## Define an AutoGen agent

# In[ ]:


from autogen import ConversableAgent

agent = ConversableAgent(
    name="chatbot",
    llm_config=llm_config,
    human_input_mode="NEVER",
)


# In[ ]:


reply = agent.generate_reply(
    messages=[{"content": "Let's start the rpg game of monster of the week!", "role": "user"}]
)
print(reply)


# In[ ]:


reply = agent.generate_reply(
    messages=[{"content": "Let's continue the game!", "role": "user"}]
)
print(reply)


# ## Conversation
# 
# Setting up a conversation between two agents, Player and Game master, where the memory of their interactions is retained.

# In[ ]:


player = ConversableAgent(
    name="player",
    system_message=
    "You play monster of the week role-playing game. Your character is orc barbarian. \
    You don't remember your name.\
    You have big stone axe with you.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

game_master = ConversableAgent(
    name="game_master",
    system_message=
    "You are game master in rpg game monster of the week. You lead players through the story."
    "Game Master is referred to as the “Keeper” (short for “Keeper of Monsters and Mysteries”)."
    "The Keeper’s primary responsibility is to create and narrate the game world,"
    "its inhabitants, and the supernatural threats (monsters) that the players, or Hunters, must confront.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)



# In[ ]:


chat_result = game_master.initiate_chat(
    recipient=player, 
    message="You wake up inside volcano and see a big stone axe next to you. What do you do?",
    max_turns=2,
)


# ## Printing results
# 
# 1. Chat history
# 2. Cost
# 3. Summary of the conversation

# In[ ]:


import pprint

pprint.pprint(chat_result.chat_history)


# In[ ]:


pprint.pprint(chat_result.cost)


# In[ ]:


pprint.pprint(chat_result.summary)