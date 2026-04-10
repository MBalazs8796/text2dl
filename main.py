import argparse
import os
from unittest import result

from src.call_api import call_api_model
from src.prompts import system_base
from src.utils import form_messages, PROMPT_ROLE_SYSTEM_USER, yellow


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--prompt_path", type=str)
    args_parser.add_argument("--output_path", type=str, default="./cache/")
    args_parser.add_argument("--model_name", type=str, default="gpt-5.2")
    args_parser.add_argument("--user_question", type=str, default="")
    args = args_parser.parse_args()
    
    user_question = \
    "Give me monuments designed by Gustave Eiffel in France."
    #"what are the coordinates of gibraltar cross of sacrifice" 
    #"where can one find estela de luz"

    #args.user_question
    knowledge = ""
    schema = ""
    query_type = "conjunctive"
    unary = """
Monument
"""
# """
# dbo_location
# """
    binary =\
"""
designedBy
"""

# """
# georss_point
# """
    constants = \
"""
GustaveEiffel
"""
# """
# dbr_Gibraltar_Cross_of_Sacrifice
# """
# """
# dbr_Estela_de_Luz
# """

    system_base_prompt =  system_base (user_question, unary, binary, constants, query_type)
    print(system_base_prompt)
    #exit()
    messages = form_messages(role_user=system_base_prompt, role_system=PROMPT_ROLE_SYSTEM_USER)

    os.makedirs(args.output_path, exist_ok=True)
    cache_output_path = args.output_path
    result  = call_api_model(messages, args.model_name, cache_output_path, use_cache=False)
    print(yellow(result))