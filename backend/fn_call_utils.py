import functools
import json
from typing import Callable

import openai

def jsonify_output(fn: Callable) -> Callable:
    """casts function output to json format"""
    @functools.wraps(fn)
    def jsoned_fn(*args, **kwargs):
        return json.dumps(fn(*args, **kwargs))
    return jsoned_fn



def create_fn_dict(name: str, description: str, arguments: dict) -> dict:
    """parses fn name, description and arguments into OpenAI's schema.
    
    Parameters
    ----------
    name : str
        Name of the function, typically, variable name.
    description: str
        a brief description of the function.
    arguments: dict
        a dictionary of arguments for the function interest.

    Returns
    -------
    dict
        Dictionary in OpenAI format for the tools iterable.
    """

    return {
        "type": "function",
        "function":{
            "name": name,
            "description": description,
            "parameters":
                {
                    "type": "object",
                    "properties": arguments,
                    },
            "required": list(arguments.keys()),
            }}


def simple_message_loop(messages: list, tools: list, fn_dict: dict) -> list:
    """Handles messaging OpenAI service and any subsequent tool calls

        
    Parameters
    ----------
    messages : list[dict]
        the conversation in the of a list of dictionaries, where each, dict represents a message.
    tools: str
        A list of dicts in OpenAI format for the tools iterable.
    fn_dict: dict[str, Callable]
        a dictionary of name, function pairs for each of the tools passed to OpenAI.

    Returns
    -------
    list
        the conversation in the of a list of dictionaries, where each, dict represents a message.
       
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message

    if response_message.tool_calls:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:

            function_response =  fn_dict[tool_call.function.name](
                **json.loads(tool_call.function.arguments)
            )

            print(f"Calling:        {tool_call.function.name}")
            print(f"Arguments:      {tool_call.function.arguments}")
            print(f"Returned:       {function_response}")

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": function_response,
                }
            ) 

        second_response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )
        
        print(f"Agent:        {second_response.choices[0].message.content}")
    else:
        print(f"Agent:        {response.choices[0].message.content}")
    return messages

    
def run_chatbot(prompt: str, tools: list[...], fn_dict: list[Callable]) -> None:
    """simple runner that collects inputs and returns messages from OpenAI service
    
    Parameters
    ----------
    messages : list[dict]
        the conversation in the of a list of dictionaries, where each, dict represents a message.
    tools: str
        A list of dicts in OpenAI format for the tools iterable.
    fn_dict: dict[str, Callable]
        a dictionary of name, function pairs for each of the tools passed to OpenAI.

    Returns
    -------
    None

    """

    _input = input("Insert your message here (type exit to leave the chat): ")
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": _input}
    ]
   
    while _input != "exit":
        _ = simple_message_loop(messages, tools, fn_dict)
        _input = input("Insert your message here (type exit to leave the chat): ")
        messages.append({"role": "user", "content": _input})
        

