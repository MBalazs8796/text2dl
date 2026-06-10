import argparse
import os
import json
import random

from src.call_api import call_api_model
from src.prompts import system_base, wikidata_parts_should_nothingelse, wikidata_parts_may
from src.utils import form_messages, PROMPT_ROLE_SYSTEM_USER, yellow

def compute_breakdown(questions, res_name):
    results_l = list()
    for question in questions:
        current_subres = dict()
        unary = [list(x.keys())[0] for x in question['Unary']]
        binary = [list(x.keys())[0] for x in question['Binary']]
        random.shuffle(unary)
        random.shuffle(binary)
        system_base_prompt =  system_base (question["Question"], ', '.join(unary), ', '.join(binary), ', '.join(''), "conjunctive")
        current_subres['prompt'] = system_base_prompt
        #exit()
        messages = form_messages(role_user=system_base_prompt, role_system=PROMPT_ROLE_SYSTEM_USER)

        os.makedirs(args.output_path, exist_ok=True)
        cache_output_path = args.output_path
        result  = call_api_model(messages, args.model_name, cache_output_path, use_cache=False)
        #print(yellow(result))
        current_subres['result'] = result
        results_l.append(current_subres)
    with open(f'{res_name}.json','w',encoding='utf8') as fp:
        json.dump(results_l, fp, indent=1)

if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--prompt_path", type=str)
    args_parser.add_argument("--output_path", type=str, default="./cache/")
    args_parser.add_argument("--model_name", type=str, default="gpt-5.2")
    args_parser.add_argument("--user_question", type=str, default="")
    args = args_parser.parse_args()
    random.seed(42)
    with open('./prev_results/res_may.json','r',encoding='utf8') as fp:
       may = json.load(fp)

    with open('./prev_results/res_may_ambig.json','r',encoding='utf8') as fp:
        may_ambig = json.load(fp)
    compute_breakdown(may_ambig, 'ambigous_matches')

    compute_breakdown(may, 'unambigous_matches')