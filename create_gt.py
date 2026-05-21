import argparse
import os
import json
import random
from unittest import result

from src.call_api import call_api_model
from src.prompts import system_base, wikidata_parts_should_nothingelse, wikidata_parts_may
from src.utils import form_messages, PROMPT_ROLE_SYSTEM_USER, yellow


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--prompt_path", type=str)
    args_parser.add_argument("--output_path", type=str, default="./cache/")
    args_parser.add_argument("--model_name", type=str, default="gpt-5.2")
    args_parser.add_argument("--user_question", type=str, default="")
    args = args_parser.parse_args()
    random.seed(42)
    results_may_list = list()
    results_should_list = list()
    with open('query.json', 'r', encoding='utf8') as fp:
        questions = json.load(fp)
    for question in questions:
        q = question['Question']
        system_should_prompt = wikidata_parts_should_nothingelse(q)
        system_may_prompt = wikidata_parts_may(q)
        messages_should = form_messages(role_user=system_should_prompt, role_system=PROMPT_ROLE_SYSTEM_USER)
        messages_may= form_messages(role_user=system_may_prompt, role_system=PROMPT_ROLE_SYSTEM_USER)
        os.makedirs(args.output_path, exist_ok=True)
        cache_output_path = args.output_path
        result_should  = call_api_model(messages_should, args.model_name, cache_output_path, use_cache=False)
        result_may  = call_api_model(messages_may, args.model_name, cache_output_path, use_cache=False)
        results_may_list.append(json.loads(result_should.split('```')[1].split('json')[1]))
        results_should_list.append(json.loads(result_should.split('```')[1].split('json')[1]))

    with open('res_should.json','w',encoding='utf8') as fp:
        json.dump(results_should_list, fp, indent=1)
    with open('res_may.json','w',encoding='utf8') as fp:
        json.dump(results_may_list, fp, indent=1)