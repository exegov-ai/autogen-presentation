#!/usr/bin/env python
# coding: utf-8

# Nested roadmap creation for a new startup
# ## Setup

# In[]:

from utils import get_azure_openai_api_key, get_openai_base_url, get_openai_model, get_openai_api_version

AZURE_OPENAI_API_KEY = get_azure_openai_api_key()
OPENAI_BASE_URL = get_openai_base_url()
OPENAI_MODEL = get_openai_model()
OPENAI_API_VERSION = get_openai_api_version()

lightweight_llm_config = {
    "model": OPENAI_MODEL,
    "api_key": AZURE_OPENAI_API_KEY,
    "base_url": OPENAI_BASE_URL,
    "api_version": OPENAI_API_VERSION,
    "api_type": "azure"
}


# ## The task is the idea for startup, you can modify it to your idea.

# In[]:


task = '''
        Describe the idea for new gaming startup.
        The idea should be about creating company that will do only 8 Player games.
        Focus on couch co-op games that can be played on a single screen.
        Online multiplayer is secondary priority.
        The idea should be to bring people back together to one room.
        Let them socialize IRL, and have fun together.
        The idea is to use games to cure depression and anxiety after lockdowns and isolation.
        Think of the name of company, legal entity, where will company be registered.
        Create a roadmap for company, predict required budget.
        Prepare plan how many people to hire and what will be predicted revenue.
        Create idea of the first game that will be developed.
        The description should include the target audience,
        the unique selling point, and the revenue model.        
       '''


# ## Create a founder agent

# In[]:


import autogen

founder = autogen.AssistantAgent(
    name="Founder",
    system_message="You are an optimistic founder." 
    "You receive an loosely written idea for new startup"
    "Your goal is to clarify this idea and create a detailed "
    "plan for the startup."
    "You should think about the name of the company, "
    "legal entity, where the company will be registered, "
    "create a roadmap, predict the required budget, "
    "prepare a plan for how many people to hire, "
    "and predict the revenue."
    "You will then receive feedback from experts."
    "You should update the roadmap based on the feedback."
    "Only return your final roadmap in form of presentation."
    "Presentation should be in MARKDOWN used by marp.",
    llm_config=lightweight_llm_config,
)


# In[]:


reply = founder.generate_reply(messages=[{"content": task, "role": "user"}])


# In[]:


print(reply)


# ## Adding feedback 
# 
# Create a team lead to create a team and provide feedback on the idea.

# In[]:


team_lead_analyst = autogen.AssistantAgent(
    name="Team Lead Analyst",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=lightweight_llm_config,
    system_message="You are a team lead analyst agent at exegov.ai."
    "You tell the founder that you are responsible for creating a team and providing feedback on the idea."
    "You should provide feedback on the idea and update the roadmap."
    "You should provide feedback on the idea and update the roadmap."
    "You should also provide feedback on the team and update the roadmap."
    "At the end you create a comment that the feedback was provided by agents of exegov.ai created in autogen."
    "Only return your final roadmap in form of MARP presentation im markdown."
)


# In[]:

res = team_lead_analyst.initiate_chat(
    recipient=founder,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)


# ## Nested chat

# In[]:


premortem_analyst = autogen.AssistantAgent(
    name="Pre Mortem Analyst",
    llm_config=lightweight_llm_config,
    system_message=
    "You are a pre-mortem analyst. You review idea of "
    "the founder and provide pre-mortem analysis."
    "Basically you present a scenario where the idea failed."
    "It could be because of various reasons like market, legal, ethical, etc."
    "Premortem technique raises awareness of possibilities, including their likely consequences, to enrich planning."
    "Your goal is to pin point all the weaknesses of the idea"
    "and provide feedback to make it better and more realistic.",
)


# In[]:


lawyer = autogen.AssistantAgent(
    name="Lawyer",
    llm_config=lightweight_llm_config,
    system_message=
    "You are a seasoned legal advisor specializing in startups. "
    "Known for your strategic insights and practical solutions, you help new businesses ensure legal compliance,"
    "tax strategies, and identify opportunities for raising capital. "
    "You provide concise (within 5 bullet points), concrete, and actionable advice. "
    "You also suggest favorable jurisdictions with startup-friendly laws and attractive tax benefits. "
    "Begin each review by stating your role."
)


# In[]:


investor = autogen.AssistantAgent(
    name="Potential Investor",
    llm_config=lightweight_llm_config,
    system_message=
        "You are a seasoned investor with a track record of funding successful startups. "
        "You provide insightful feedback on business ideas, drawing on examples of real life companies and their playbooks . "
        "You evaluate proposals by discussing what factors would make you invest or decline. "
        "You advise on equity distribution, suggesting appropriate shares for founders and investors. "
        "You recommend fundraising strategies such as crowdfunding, venture capital rounds, and outline potential funding stages. "
        "You advise weather to do IPO, ICO or IDO etc."
        "Begin each review by stating your role.",
)


# In[]:


chief_editor = autogen.AssistantAgent(
    name="Chief Editor",
    llm_config=lightweight_llm_config,
    system_message=(
        "You are the Chief Editor who aggregates and synthesizes feedback from other reviewers, such as legal advisors and potential investors. "
        "You provide a final, comprehensive recommendation on the content, ensuring all critical points are addressed and the overall quality is optimized. "
        "Begin each review by stating your role."
    ),
)



# ## Orchestrate the nested chats to solve the task

# In[]:


def reflection_message(recipient, messages, sender, config):
    return f'''Review the following startup idea. 
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''

review_chats = [
    {
     "recipient": premortem_analyst, 
     "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'Reviewer': '', 'Review': ''}. Here Reviewer should be your role",},
     "max_turns": 1},
    {
    "recipient": lawyer, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'Reviewer': '', 'Review': ''}.",},
     "max_turns": 1},
    {"recipient": investor, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'reviewer': '', 'review': ''}",},
     "max_turns": 1},
     {"recipient": chief_editor, 
      "message": "Aggregrate feedback from all reviewers and give final suggestions on the roadmap.", 
     "max_turns": 1},
]


# In[]:


team_lead_analyst.register_nested_chats(
    review_chats,
    trigger=founder,
)



# In[]:


res = team_lead_analyst.initiate_chat(
    recipient=founder,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)


# ## Get the summary

# In[]:

print(res.summary)