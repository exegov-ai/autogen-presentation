---
marp: true
---

# What is autogen and ag2?

It's framework to build autonomus multi agent systems.

---

# Autogen and ag2

Autogen statred as open source project by microsoft, hosted as [microsoft/autogen](https://github.com/microsoft/autogen) but now Autogen2 is separate organization called [ag2](https://github.com/ag2ai/ag2). Python package is pyauthogen or simply ag2.

---

# Some of coolest features

- **Conversation Patterns**: Autogen provides a set of conversation patterns that can be used to model the interactions between agents. It's main topic of today's presentation.

- **Code executors**: Autogen agents can both call only pre-defined registered functions, or just write the code and execute it. It's very powerful but risky feature.

- **Human in the loop**: User can be part of the conversation, and can be asked to provide some information or make a decision.

---

# Multi agent and multimodel

Autogen was started in Microsoft, but it's open source.
Documentation of ag2 provides a lot of examples how to use ag2 with Azure, but it's not limited to Azure. It can be used with any other cloud provider or even on-premises. There are instructions for [Non-Open AI Models](https://ag2ai.github.io/ag2/docs/topics/non-openai-models/about-using-nonopenai-models/), [Anthropic Claude](https://ag2ai.github.io/ag2/docs/topics/non-openai-models/cloud-anthropic/), [Amazon Bedrock](https://ag2ai.github.io/ag2/docs/topics/non-openai-models/cloud-bedrock/), [Google Gemini](https://ag2ai.github.io/ag2/docs/topics/non-openai-models/cloud-gemini/) as well as [locally ran open source models with ollama](https://ag2ai.github.io/ag2/docs/topics/non-openai-models/local-ollama/) 

---

# That's right, you can run multi agent system on your laptop

You can experiment with multi agent system on your laptop.
You don't need to pay for any external APIs.
You don't need to pay for any cloud services.
Some models consume surprisingly low amount of resources (for example gemma2).