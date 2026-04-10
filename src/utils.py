

import json
import sys
import pycparser
import sqlparse
import textwrap

PROMPT_ROLE_SYSTEM_USER = "You are a smart assistant that can help me understand the user query ."


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   GREY = '\033[90m'
   END = '\033[0m'


def normal(text : str) -> str:
   return text

def bold(text : str) -> str:
   return color.BOLD + text + color.END

def red(text : str) -> str:
   return color.RED + text + color.END

def blue(text : str) -> str:
   return color.BLUE + text + color.END

def green(text : str) -> str:
   return color.GREEN + text + color.END

def yellow(text : str) -> str:
   return color.YELLOW + text + color.END

def purple(text : str) -> str:
   return color.PURPLE + text + color.END

def cyan(text : str) -> str:  
   return color.CYAN + text + color.END

def darkcyan(text : str) -> str:  
   return color.DARKCYAN + text + color.END

def grey(text : str) -> str:
   return color.GREY + text + color.END


def form_messages(role_user, role_system=PROMPT_ROLE_SYSTEM_USER):
    messages = [
                {"role": "user", "content": f"{role_user}"},
            ]
    return  messages


