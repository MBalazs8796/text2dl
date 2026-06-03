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

    Your task is transform queries from natural language to {query_type} queries.
    Translate it to {query_type} query in the form of a mapping.
    Use the unary and binary predicates alongside the constants defined above.
    A term is either a variable or a constant. Variables can either be free or existentially quantified (possibly with counting).
    Binary predicates can be quantified with counting, to express this use the < sign for "less then", the > for the "more than" sign, le for the "less or equal" sign and ge for "greater or equal" sign.
    Each sign must be followed by a natural number and they must precede the relevant atom.
    In cases where the question contains statements such as "(at least) K different friends", you can use ge K friend(x,y), as this kind of counting implies that the elements involved are different.
    If you need to use any logical operator, use it's English equivalent instead, for example "and" for \u2227 and "exists" for \u2203.
    An atom is of the form A(t) where A is a unary predicate and t is a term or of the form A(t1, t2) where A is a binary predicate and t1 and t2 are terms.
    If you do not know how to translate parts of the user query, indicate this in the mapping.
    In cases where additional assumptions need to be made, for example, a "large elephant", if you have no predicate or combination of predicates that without a doubt combines to "large" do not make an assumption based on external knowledge, instead map "large" to UNKNOWN.
    "Which area", "What day", "Find a city", or "Who" should not be translated into predicates.
    Instead, map the entity being asked for to the distinguished output variable ?x.

    #Format: 
    a mapping between relevant parts of the query and parts of the {query_type} query is in the form:

    [(part of the user query, atom OR term OR predicate OR UNKNOWN),
    ...
    (part of the user query, atom OR term OR predicate OR UNKNOWN)]
    """
    return prompt_base

def wikidata_parts_should_nothingelse(question):
    base = f'''
    Your task is the following:
    Create a set of binary and unary predicates that are able to express the following question, when combined in a query:
    {question}
    Some predicates should be irrelevant.
    Restrict yourself to only using WikiData classes and relations as the basis of your predicates.
    If this restriction does not allow parts of the sentence to be expressed directly, it is acceptable for them to be expressed as a combination of predicates.
    You are allowed to assume the use of numerical and existential quantifiers (exists, less/more than X), but nothing else.
    Alongside the predicates, return a mapping of the form (part_of_sentence, part_of_query) where you highlight which predicates correspond to which parts of the sentence.
    Use the following JSON format:
    "Question": your_task_question,
    "Unary": [{{ predicate_name : [ wiki_data_PID, reason_for_inclusion ]}}, ...],
    "Binary": [{{ predicate_name : [ wiki_data_PID, reason_for_inclusion ]}}, ...],
    "Mapping": {{ part_of_sentence: predicate_combination }}
    Here is a concrete example without distractors:
    "Question": "Give me schools that over 1000 students attended.",
    "Unary": [{{ "school" : [ "Q3914", "Express school" ]}}],
    "Binary": [{{ "educated at" : [ "P69", "Express attended" ]}}],
    "Mapping": {{ "schools": "school(x)", "over 1000 student attended": ">1000educated at(y,x)" }}
    '''
    return base
    
def wikidata_parts_may(question):
    base = f'''
    Your task is the following:
    Create a set of binary and unary predicates that are able to express the following question, when combined in a query:
    {question}
    Some predicates may be irrelevant.
    Restrict yourself to only using WikiData classes and relations as the basis of your predicates.
    If this restriction does not allow parts of the sentence to be expressed directly, it is acceptable for them to be expressed as a combination of predicates.
    You are allowed to assume the use of numerical and existential quantifiers (exists, less/more than X).
    Alongside the predicates, return a mapping of the form (part_of_sentence, part_of_query) where you highlight which predicates correspond to which parts of the sentence.
    Use the following JSON format:
    "Question": your_task_question,
    "Unary": [{{ predicate_name : [ wiki_data_PID, reason_for_inclusion ]}}, ...],
    "Binary": [{{ predicate_name : [ wiki_data_PID, reason_for_inclusion ]}}, ...],
    "Mapping": {{ part_of_sentence: predicate_combination }}
    Here is a concrete example without distractors:
    "Question": "Give me schools that over 1000 students attended.",
    "Unary": [{{ "school" : [ "Q3914", "Express school" ]}}],
    "Binary": [{{ "educated at" : [ "P69", "Express attended" ]}}],
    "Mapping": {{ "schools": "school(x)", "over 1000 student attended": ">1000educated at(y,x)" }}
    '''
    return base
