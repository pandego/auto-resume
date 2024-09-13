import os
from typing import Any, Optional, List

from dotenv import load_dotenv, find_dotenv
from langchain.llms.base import LLM
from openai import OpenAI
from pydantic import Field
from rich import print as rprint


def load_env():
    _ = load_dotenv(find_dotenv(), override=True)


def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key


# ------------------------- #
# --- Get OpenAI Client --- #
# ------------------------- #


def get_client(
    client_type: str = "openai",
):
    if client_type == "openai":
        client = OpenAI()
    elif client_type == "groq":
        client = OpenAI(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url=os.environ.get("GROQ_API_BASE_URL"),
        )
    elif client_type == "openrouter":
        client = OpenAI(
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            base_url=os.environ.get("OPENROUTER_API_BASE_URL"),
        )
    elif client_type == "ollama":
        client = OpenAI(
            api_key=os.environ.get("OLLAMA_API_KEY"),
            base_url=os.environ.get("OLLAMA_API_BASE_URL"),
        )
    return client


# ------------------------- #
# --- OpenAI Structured --- #
# ------------------------- #

# class StructuredResponse(OpenAI):
#     event: CalendarEvent
#     model_name: str = Field(..., description="The name of the model to use")
#     client: Any = Field(..., description="The OpenAI client")

#     def __init__(self, model_name: str, client: Any):
#         super().__init__(model_name=model_name, client=client)

#     def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
#     event: CalendarEvent

# completion = client.beta.chat.completions.parse(
#     model="gpt-4o-mini-2024-07-18",
#     model="gpt-4o-2024-08-06"
#     messages=[
#         {"role": "system", "content": "Extract the event information."},
#         {"role": "user", "content":prompt}
#         ],
#     response_format=ResponseFormat,
# )

# return completion.choices[0].message.parsed


# ------------------------ #
# --- Agent Compatible --- #
# ------------------------ #


class OpenRouterLLM(LLM):
    """
    OpenRouterLLM class for using OpenRouter's API with LangChain.

    Parameters
    ----------
    model_name : str
        The name of the model to use.
    client : Any
        The OpenAI client instance configured for OpenRouter.

    Attributes
    ----------
    model_name : str
        The name of the model being used.
    client : Any
        The OpenAI client instance.

    Methods
    -------
    _call(prompt: str, stop: Optional[List[str]] = None) -> str
        Internal method to call the OpenRouter API.

    Examples
    --------
    >>> from openai import OpenAI
    >>> import os
    >>> client = OpenAI(
    ...     base_url="https://openrouter.ai/api/v1/",
    ...     api_key=os.environ.get("OPENROUTER_API_KEY")
    ... )
    >>> llm = OpenRouterLLM(
    ...     model_name="meta-llama/llama-3.1-8b-instruct:free",
    ...     client=client
    ... )
    >>> response = llm.invoke("What is the capital of France?")
    >>> print(response)
    The capital of France is Paris.

    """

    model_name: str = Field(..., description="The name of the model to use")
    client: Any = Field(..., description="The OpenAI client")

    def __init__(self, model_name: str, client: Any):
        """
        Initialize the OpenRouterLLM instance.

        Parameters
        ----------
        model_name : str
            The name of the model to use.
        client : Any
            The OpenAI client instance configured for OpenRouter.

        """
        super().__init__(model_name=model_name, client=client)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Internal method to call the OpenRouter API.

        Parameters
        ----------
        prompt : str
            The input prompt to send to the model.
        stop : Optional[List[str]], optional
            A list of strings that, if encountered, will stop the API call.

        Returns
        -------
        str
            The generated response from the model.

        Examples
        --------
        >>> llm = OpenRouterLLM(model_name="example-model", client=example_client)
        >>> response = llm.invoke("Tell me a joke.")
        >>> print(response)
        Why don't scientists trust atoms? Because they make up everything!

        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            max_tokens=512,
            temperature=0.0,
            seed=42,
        )
        return response.choices[0].message.content

    @property
    def _llm_type(self) -> str:
        """
        Get the type of the LLM.

        Returns
        -------
        str
            The type of the LLM, which is "OpenRouter".

        """
        return "OpenRouter"


class GroqLLM(LLM):
    """
    A class representing the Groq Language Model (LLM) integration.

    This class provides an interface to interact with Groq's LLM using the OpenAI-compatible API.

    Parameters
    ----------
    model_name : str
        The name of the Groq model to use.
    client : Any
        The OpenAI client instance configured for Groq.

    Attributes
    ----------
    model_name : str
        The name of the model being used.
    client : Any
        The OpenAI client instance.

    Methods
    -------
    _call(prompt: str, stop: Optional[List[str]] = None) -> str
        Internal method to call the Groq API.

    Examples
    --------
    >>> from openai import OpenAI
    >>> import os
    >>> client = OpenAI(
    ...     base_url="https://api.groq.com/openai/v1/",
    ...     api_key=os.environ.get("GROQ_API_KEY")
    ... )
    >>> llm = GroqLLM(
    ...     model_name="llama-3.1-70b-versatile",
    ...     client=client
    ... )
    >>> response = llm.invoke("Tell me a joke.")
    >>> print(response)
    Why don't scientists trust atoms? Because they make up everything!

    """

    model_name: str = Field(..., description="The name of the model to use")
    client: Any = Field(..., description="The Groq client")

    def __init__(self, model_name: str, client: Any):
        """
        Initialize the GroqLLM instance.

        Parameters
        ----------
        model_name : str
            The name of the Groq model to use.
        client : Any
            The OpenAI client instance configured for Groq.

        """
        super().__init__(model_name=model_name, client=client)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Internal method to call the Groq API.

        Parameters
        ----------
        prompt : str
            The input prompt to send to the model.
        stop : Optional[List[str]], optional
            A list of strings that, if encountered, will stop the generation.

        Returns
        -------
        str
            The generated response from the model.

        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            max_tokens=512,
            temperature=0.0,
            seed=42,
        )
        return response.choices[0].message.content

    @property
    def _llm_type(self) -> str:
        """
        Get the type of the LLM.

        Returns
        -------
        str
            The type of the LLM, which is "Groq".

        """
        return "Groq"


class Ollama(LLM):
    """
    A class representing the Ollama Language Model (LLM) integration.

    This class provides an interface to interact with Ollama's LLM using the OpenAI-compatible API.

    Parameters
    ----------
    model_name : str
        The name of the Ollama model to use.
    client : Any
        The OpenAI client instance configured for Ollama.

    Attributes
    ----------
    model_name : str
        The name of the model being used.
    client : Any
        The OpenAI client instance.

    Methods
    -------
    _call(prompt: str, stop: Optional[List[str]] = None) -> str
        Internal method to call the Ollama API.

    Examples
    --------
    >>> from openai import OpenAI
    >>> import os
    >>> client = OpenAI(
    ...     base_url="http://localhost:11434/v1",
    ...     api_key="ollama"
    ... )
    >>> llm = Ollama(
    ...     model_name="llama3.1:latest",
    ...     client=client
    ... )
    >>> response = llm.invoke("Tell me a joke.")
    >>> print(response)
    Why don't scientists trust atoms? Because they make up everything!

    """

    model_name: str = Field(..., description="The name of the model to use")
    client: Any = Field(..., description="The Ollama client")

    def __init__(self, model_name: str, client: Any):
        """
        Initialize the Ollama instance.

        Parameters
        ----------
        model_name : str
            The name of the Ollama model to use.
        client : Any
            The OpenAI client instance configured for Ollama.

        """
        super().__init__(model_name=model_name, client=client)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Internal method to call the Ollama API.

        Parameters
        ----------
        prompt : str
            The input prompt to send to the model.
        stop : Optional[List[str]], optional
            A list of strings that, if encountered, will stop the generation.

        Returns
        -------
        str
            The generated response from the model.

        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            max_tokens=512,
            temperature=0.0,
            seed=42,
        )
        return response.choices[0].message.content

    @property
    def _llm_type(self) -> str:
        """
        Get the type of the LLM.

        Returns
        -------
        str
            The type of the LLM, which is "Ollama".

        """
        return "Ollama"


if __name__ == "__main__":
    prompt = "Tell me a joke."

    # Test OpenAI
    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.0,
        seed=42,
    )

    print("# -------------- #")
    print("# --- OpenAI --- #")
    print("# -------------- #")
    rprint(f"\n'''\n{response.choices[0].message.content}\n'''\n")

    # Test OpenRouter
    client = get_client(
        base_url="https://openrouter.ai/api/v1/",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
    )
    llm = OpenRouterLLM(
        model_name="meta-llama/llama-3.1-8b-instruct:free", client=client
    )
    response = llm.invoke(prompt)

    print("# ------------------ #")
    print("# --- OpenRouter --- #")
    print("# ------------------ #")
    rprint(f"\n'''\n{response}\n'''\n")

    # Test Groq
    client = get_client(
        base_url="https://api.groq.com/openai/v1/",
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    llm = GroqLLM(model_name="llama-3.1-70b-versatile", client=client)
    response = llm.invoke(prompt)

    print("# ------------ #")
    print("# --- Groq --- #")
    print("# ------------ #")
    rprint(f"\n'''\n{response}\n'''\n")

    # Test Ollama
    client = get_client(base_url="http://localhost:11434/v1", api_key="ollama")
    llm = Ollama(model_name="llama3.1:latest", client=client)
    response = llm.invoke(prompt)
    print("# -------------- #")
    print("# --- Ollama --- #")
    print("# -------------- #")
    rprint(f"\n'''\n{response}\n'''\n")
