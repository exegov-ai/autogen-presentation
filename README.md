# 2Agents RPG Setup

## Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Optional
- `conda` (Anaconda package manager - recommended by [Autogen Studio team](https://autogen-studio.com/autogen-studio-ui) however only some examples in this repo were created using it)

## Installation

1. Clone the repo:

    ```sh
    git clone git@github.com:exegov-ai/autogen-presentation.git
    ```

2. Create a virtual environment:

    ```sh
    conda create --name autogen-presentation python=3.8
    conda activate autogen-presentation
    ```

    Using `venv`:

    ```sh
    python -m venv autogen-presentation
    source autogen-presentation
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

## 2Agents RPG

In this example 2 agents play role playing game. One agent is the player and the other is the game master.

```sh
python 2agents-rpg.py
```