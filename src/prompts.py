def system_base(user_question, unary, binary, constants, query_type):
    prompt_base =  \
f"""
We define a set predicates and constants:

#Unary predicates 
{unary}

#Binary predicates
{binary}

#Constants
{constants}


# User Query:
{user_question}


# Instructions:

You are a translator form natural language to {query_type} queries.
Translate it to {query_type} query in the form of a mapping. 
Use predicates and constants defined above.
A term is either a variable or a constant. Variables can either be free or existentially quantified.
An atom is of the form A(t) where A is a predicate and t is a term or of the form A(t1, t2) where A is a binary predicate and t1 and t2 are terms.
If you do not know how to translate parts of the user query, indicate in the mapping 

#Format: 
a mapping between relevant parts of the query and parts of the {query_type} query in the form:

[(part of the user query, atom OR term OR predicate OR UNKNOWN),
...
(part of the user query, atom OR term OR predicate OR UNKNOWN)]
"""
    return prompt_base

