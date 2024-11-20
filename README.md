# GenAI Cracow #9 Autogen Conversation Patterns

This is presentation repository for [GenAI Cracow #9 meetup on 2024/11/25](https://lu.ma/67h2lt7k?tk=DtPGDy).

## Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Optional
- `conda` (Anaconda package manager - recommended by [Autogen Studio team](https://autogen-studio.com/autogen-studio-ui) however only some examples in this repo don't require this ui)

## Installation

1. Clone the repo:

    ```sh
    git clone git@github.com:exegov-ai/autogen-presentation.git
    ```

2. Create a virtual environment:

    ```sh
    conda create --name autogenstudio python=3.11.10
    conda activate autogenstudio
    ```

    Using `venv`:

    ```sh
    python -m venv autogenstudio
    source autogenstudio
    ```
3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Install `autogen` version 0.2:

    ```sh
    pip install autogen==0.2
    ```

    > Note: The [stable documentation refers to version 0.2](https://microsoft.github.io/autogen/0.2/). According to the [autogen repository README](https://github.com/microsoft/autogen), version 0.2 will be maintained for some time, but version 0.4, which has some breaking changes, will replace it.

## Configuration

1. Copy the example environment file and update it with your API key:

    ```sh
    cp .env.example .env
    ```

    Edit the [.env](http://_vscodecontentref_/0) file and replace `YOUR_API_KEY_1234567890` with your actual Azure OpenAI API key.

2. Locally at time of writing I have file `model_gpt-4o-mini.json` in the project directory that contains configuration for the OpenAI model deployed in Azure.
Autogen allows both Open AI models and Azure Open AI as well as [custom models to be used](https://microsoft.github.io/autogen/0.2/blog/2024/01/26/Custom-Models/). The json used in this example was created by Autogen Studio and is not included in this repository it matches [autogen studio syntax](https://microsoft.github.io/autogen/0.2/blog/2023/12/01/AutoGenStudio/).

# Running Examples

## 2Agents RPG 🤖🎲🤖

In this example 2 agents play role playing game. One agent is the player and the other is the game master.

```sh
python 2agents-rpg.py
```

## Sequential Everyday chat 👤💬➡️📝➡️📊➡️🌐➡️👤

This example assumes that user has some data about their company and wants to update their business strategy. User talks to the AI about the company and then agents are summoned in sequential way to collect requirements.

```sh
python sequential-everyday-chat.py
```

## Nested Startup Idea Valuation 💡➡️🤖➡️👨‍👩‍👧‍👦

In this example first agent receives a task which is very early stage blurry description of startup.
Then the agent takes the idea to multiple other specialized agents to get feedback on the idea.
Then prepare some roadmap for the idea.

```sh
python nested-startup-idea-valuation.py
```

## Group Networking 👤💬🤖💬👥🤖💬🤖💬👥🤖💬

Imagine being in discord channel, this is a simulation of group networking where agents are talking to each other and to the user.
The user is admin of chat, there's also moderator agent, newsman agent that uses function calling to fetch news from rss feeds, 2 agents that are interested in certain topics and one that just tries to troll other chat members.

# Running with local model

In the example local ran gemma2 ran using ollama was used and config is provided in `model_gemma2.json` file.


## IMPORTANT Note, gemma2 model cannot call functions, so not all examples will work with it.

## Installation of ollama and gemma2 (or any other open source model you wish)

Instal ollama locally

```sh
curl -fsSL https://ollama.com/install.sh | sh\n
```

Pull gemma2 model (or if you want to play with different model, pull the one you with to use from ollama directory).

```sh
ollama pull gemma2
```

Test if it works with curl (or import it to postman or whatever is your favourite tool for rest apis).

```sh
curl http://localhost:11434/v1/chat/completions \\n    -H "Content-Type: application/json" \\n    -d '{\n        "model": "gemma2",\n        "messages": [\n            {\n                "role": "system",\n                "content": "You are a helpful assistant."\n            },\n            {\n                "role": "user",\n                "content": "Hello!"\n            }\n        ]\n    }'\n
```