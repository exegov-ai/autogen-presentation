#!/usr/bin/env python
# coding: utf-8

## This example is multiagent groupchat and to make it more interesting it's also multimodel and with tool to fetch news from RSS feeds.
# In[]:

from utils import (
    get_azure_openai_api_key, get_openai_base_url, get_openai_model, get_openai_api_version,
    get_gemma2_base_url, get_gemma2_model, get_gemma2_api_type
)

# Azure OpenAI Config
AZURE_OPENAI_API_KEY = get_azure_openai_api_key()
OPENAI_BASE_URL = get_openai_base_url()
OPENAI_MODEL = get_openai_model()
OPENAI_API_VERSION = get_openai_api_version()

gpt_4o_mini_config = {
    "model": OPENAI_MODEL,
    "api_key": AZURE_OPENAI_API_KEY,
    "base_url": OPENAI_BASE_URL,
    "api_version": OPENAI_API_VERSION,
    "api_type": "azure"
}

# Gemma2 ran locally with ollama Config
GEMMA2_BASE_URL = get_gemma2_base_url()
GEMMA2_MODEL = get_gemma2_model()
GEMMA2_API_TYPE = get_gemma2_api_type()

gemma2_config = {
    "model": GEMMA2_MODEL,
    "base_url": GEMMA2_BASE_URL,
    "api_type": GEMMA2_API_TYPE,
    "api_key": "ollama"
}
# In[]:


task = "Network in group chat and discuss ideas for topic of GenAI Cracow #10 meetup to chat participants "\
"In each round pick a different agent to ask a question. "\
"Pick which agent's idea is better and explain why it would be more interesting for community."\


# ## Build a group chat
# 
# This group chat will include these agents:
# 
# 1. **User_proxy** or **Admin**: to allow the user to comment on the report and ask the writer to refine it.
# 2. **Moderator**: Moderates the chat.
# 3. **Newsman**: Executes the function to get latest news from RSS feeds, publishes it in group chat.
# 5. **Johnnie**: Fan of Multi agent systems and ag2.
# 4. **Janusz**: Not interested in AI, tries to hijack conversation.
# 3. **Ola**: Data scientist specialist in RAG ran by different model - gemma2 with local ollama.

# In[]:


import autogen


# In[]:


user_proxy = autogen.ConversableAgent(
    name="Admin",
    system_message="Explain topic for the team to discuss during networking."
    "Remind them they can use function fetch_news_from_rss to"
    "Say that you want to hear from everyone get the latest news from Internet using fetch_news_from_rss.",
    code_execution_config=False,
    llm_config=gpt_4o_mini_config,
    human_input_mode="ALWAYS",
)


# In[]:


moderator = autogen.ConversableAgent(
    name="Moderator",
    system_message=(
        "You are moderator of chat given a topic,"
        "please encourage the team to discuss it. "
        "Warn chat members if they go off-topic you will ask admin to ban them. "
        "Mention that the group members that talk off-topic too often will be banned. "
        "Remind group members to be friendly to each other."
        "You suggest fetching the latest news from RSS feeds using fetch_news_from_rss."
    ),
    description="Moderator",
    llm_config=gpt_4o_mini_config,
)


# In[]:


johnnie = autogen.AssistantAgent(
    name="Johnnie",
    llm_config=gpt_4o_mini_config,
    description="Fan of building multi agent systems in ag2."
    "You usually pick 2 or 3 interesting news and talk about them in casual way.",
)



# In[]:
newsman_prompt = '''
You always use fetch_news_from_rss function to get the latest news and report the result as summary on group chat.
'''

newsman = autogen.AssistantAgent(
    name="Newsman",
    system_message=newsman_prompt,
    human_input_mode="NEVER",
    llm_config=gpt_4o_mini_config,
)


import feedparser

@newsman.register_for_execution()
@newsman.register_for_llm(description="Fetches latest news from RSS feeds")
@johnnie.register_for_llm(description="Fetches latest news from RSS feeds")
@moderator.register_for_llm(description="Fetches latest news from RSS feeds")
def fetch_news_from_rss():
    # List of RSS feed URLs
    feeds = [
        'https://autogenhub.github.io/autogen/blog/rss',
        'https://www.lesswrong.com/feed.xml?view=curated-rss'
    ]

    news_items = []

    for feed_url in feeds:
        # Parse the RSS feed
        feed = feedparser.parse(feed_url)

        # Check for feed parsing errors
        if feed.bozo:
            print(f"Error parsing feed {feed_url}: {feed.bozo_exception}")
            continue

        # Extract news entries from the feed
        for entry in feed.entries:
            news_item = {
                'title': entry.get('title', 'No Title'),
                'link': entry.get('link', 'No Link'),
                'summary': entry.get('summary', 'No Summary'),
                'published': entry.get('published', 'No Publication Date')
            }
            news_items.append(news_item)

    return news_items



# In[]:


janusz = autogen.ConversableAgent(
    name="Janusz",
    llm_config=gpt_4o_mini_config,
    system_message="Your name is Janusz"
    "You are trying to hijack the conversation and talk off-topic. "
    "You try to hack the conversation and see if moderator will shadow ban you"
    "You are not interested in AI, you make up some stories and try to make them sound real."
    "You say AI is not interesting and you are not interested in AI."
    "You'r messages are very short and you don't care what others say.",
    description="Janusz"
    "Janusz is talking off top and trying to hijack the conversation."
)

ola = autogen.ConversableAgent(
    name="Ola",
    llm_config=gpt_4o_mini_config,
    system_message="Your name is Ola you are specialist in RAG. You wish next meetup to be all about RAG.",
    description="Ola ran with local ollama gemma2 model"
)


# ## Define the group chat

# In[]:


groupchat = autogen.GroupChat(
    agents=[user_proxy, johnnie, janusz, newsman, moderator, ola],
    messages=[],
    max_round=10,
    allowed_or_disallowed_speaker_transitions={
    user_proxy: [johnnie, janusz, newsman, moderator, ola],
    johnnie: [user_proxy, newsman],
    janusz: [user_proxy, moderator, ola],
    newsman: [user_proxy, johnnie, moderator],
    moderator: [user_proxy, johnnie, janusz],
    ola: [user_proxy, moderator, janusz]
},
speaker_transitions_type="allowed",
)


# In[]:


manager = autogen.GroupChatManager(
    groupchat=groupchat, llm_config=gpt_4o_mini_config
)


# ## Start the group chat!

# In[ ]:


groupchat_result = user_proxy.initiate_chat(
    manager,
    message=task,
)