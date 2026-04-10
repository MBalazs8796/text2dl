import argparse
import os
import json
from pathlib import Path
import time
import itertools

import hashlib

from openai import OpenAI
from src.config import model_config
from src.utils import *


def new_directory(path):
    if path and not os.path.exists(path):
        os.makedirs(path)


# print(json.dumps(model_config, indent=4))


cnt_debug  = 0
def debug_cnt():
    global cnt_debug
    cnt_debug += 1
    return cnt_debug

def api_request(messages, engine, client, backend, use_cache = True, **kwargs):
    """
    Calls the underlying LLM endpoint depending on the 'backend'.
    """
    focus_debug = 1000
    

    temperature = kwargs.get("temperature", 1)
    frequency_penalty = kwargs.get("frequency_penalty", 1.5)
    presence_penalty = kwargs.get("presence_penalty", 0)
    attempts = kwargs.get("attempts", 1)
    stop = kwargs.get("stop", None)
    prompt_dir = kwargs.get("cache_output_path", "./cache/")
    reasoning_effort = kwargs.get("reasoning_effort", "medium")
    is_reasoning = kwargs.get("is_reasoning", False)
 
 
    debug_cnt()
    if focus_debug == cnt_debug:
        print(attempts)
        for message in messages:
            print(f"message: {message['role']}")            
            print(f"--------------------------------")
            print("-->" + green(message["content"]) +"<---")
            print(f"--------------------------------")
            print("\n")
        
        

        #exit()
    # print_line("Setting", "Engine", engine, nb_tabs = 0, color = yellow) 
    # print_line("Setting", "Backend", backend, nb_tabs = 0, color = yellow) 
    # print_line("Setting", "Use Cache", use_cache, nb_tabs = 0, color = yellow) 
    # print_line("Setting", "Attempts", attempts, nb_tabs = 0, color = yellow) 
    # print_line("Setting", "Temperature", temperature, nb_tabs = 0, color = yellow) 
    # print_line("Setting", "Frequency Penalty",frequency_penalty, nb_tabs = 0, color = yellow) 
    # print_line("Setting", "Presence Penalty", presence_penalty, nb_tabs = 0, color = yellow) 
    # print_line("Setting", "Stop", stop, nb_tabs = 0, color = yellow) 
    # print_line("Setting", "Prompt Dir", prompt_dir, nb_tabs = 0, color = yellow) 


    hashing = json.dumps({"messages": messages,
                              "engine": engine,
                              "backend": backend,
                              "attempts": attempts,
                              "temperature": temperature,
                              "reasoning_effort": reasoning_effort,
                              "frequency_penalty":frequency_penalty,
                              "presence_penalty":presence_penalty}).encode('utf-8')
    
    
    hashing_key = hashlib.sha256(hashing).hexdigest()
    #print(hashing_key)
    prompt_filename = f"prompt_{hashing_key}.json"
    result = {}

    try:
        #print(os.path.join(prompt_dir, prompt_filename))
        if  use_cache:
                #print("~~~~~~~~~~~~~~~~~")
                # print_header("<--------- cached prompt ----------------->", color = red)                
            try:
                #print(1)

                with open(os.path.join(prompt_dir, prompt_filename), 'r') as f:
                    #print(2)
                    #print("-cashing-")

                    result = json.load(f)
                    #print("done")
                #print("-->", result["completions"])
                    #exit()
                if focus_debug == cnt_debug:
                    print(attempts)                    
                    print(grey(result["completion"]) + "\n")
                    #exit()
                #print(result["completion"])
               # exit()
                return result["completion"]
            except Exception as e:
                #print(3)
                #print(f"{e}")
                pass
    except Exception as e:
            print(f"{e}")
            pass


    while True:
        #print(f"{'backend': <20} {backend}, {engine}")
        try:
            if backend == "openai":
                if is_reasoning and (engine.find("o4-mini") != -1 or engine.find("gpt-5-mini") != -1):
                    completion = client.chat.completions.create(
                        model=engine,
                        messages=messages,
                        reasoning_effort= reasoning_effort,                        
                    )
                    # for choice in completion.choices:
                    #     print(choice.message.content)
                else:
                    #print(engine, len(str(messages)))
                    completion = client.chat.completions.create(
                        model=engine,
                        messages=messages,
                        reasoning_effort= reasoning_effort)
                #print("done")
                #print(completion.choices[0].message.content)
                #exit()

                result["messages"] = messages
                result["engine"] = engine
                result["backend"] = backend
                result["attempts"] =  attempts
                result["frequency_penalty"] = kwargs.get("frequency_penalty", 0)
                result["presence_penalty"] = kwargs.get("presence_penalty", 0)
                result["temperature"] = kwargs.get("temperature", 1)

                result["completion"] = {}

                result["completion"] = completion.choices[0].message.content
                with open(os.path.join(prompt_dir, prompt_filename), 'w') as out_file:
                    json.dump(result, out_file)

                return completion.choices[0].message.content

            elif backend == "anthropic":
                max_tokens = kwargs.get("max_tokens", 64000)
                if engine.find("claude-3-5-haiku-latest") != -1:
                    max_tokens = 8000
                message = client.messages.create(
                    model=engine,
                    messages=messages,
                    max_tokens= max_tokens,
                    top_p=kwargs.get("top_p", 1),
                    stop_sequences=kwargs.get("stop", None),
                )
                result["messages"] = messages
                result["engine"] = engine
                result["backend"] = backend
                result["attempts"] =  attempts
                result["frequency_penalty"] = kwargs.get("frequency_penalty", 0)
                result["presence_penalty"] = kwargs.get("presence_penalty", 0)
                result["temperature"] = kwargs.get("temperature", 1)

                result["completion"] = {}

                result["completion"] = message.content[0].text
                
                with open(os.path.join(prompt_dir, prompt_filename), 'w') as out_file:
                    json.dump(result, out_file)      

                print(message.usage.output_tokens)   
                print(message.usage.input_tokens)   
                #exit()
                return message.content[0].text

        except Exception as e:
            print(e)
            time.sleep(1)


            


def call_api_model(
    messages,
    model_name,
    cache_output_path,
    temperature=0,
    max_tokens=64000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    timeout=10,
    attempts = 1,
    is_reasoning=False,
    reasoning_effort="high",
    stop=None,
    use_cache=True
):

    """
    Sets up the correct backend client + model engine, then calls 'api_request'.
    """
    #print(cache_output_path)
    if "gpt" in model_name or "o1" in model_name or "o3" in model_name or "o4" in model_name:
        engine = model_name
        try:
            client = OpenAI(
                base_url=model_config[model_name]["base_url"],
                api_key=model_config[model_name]["api_key"],
            )
        except Exception as e:
            print(f"Error: {e}")
            exit()
        backend = "openai"
        #exit(0)
    elif "claude" in model_name:
        engine = model_name
        client = anthropic.Anthropic(
            api_key=model_config[model_name],
        )
        backend = "anthropic"

    elif "gemini" in model_name:
        engine = model_name
        client = genai.GenerativeModel(engine)
        genai.configure(api_key=GEMINI_API_KEYS[1])
        backend = "genai"

    else:
        print(f"Unsupported model name: {model_name}")
        raise ValueError(f"Unsupported model name: {model_name}")

    kwargs = {
        "reasoning_effort": reasoning_effort,
        "is_reasoning": is_reasoning,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "attempts": attempts, 
        "stop": stop,
        "cache_output_path": cache_output_path,
    }
    return api_request(messages, engine, client, backend, use_cache,  **kwargs)

