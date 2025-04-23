from pyswip import Prolog # pip install -U pyswip
import re

# dict to map statement patterns (from specs)
statement_pattern = {
    r"(.+) and (.+) are siblings\.": lambda m: f"siblings({m.group(1)}, {m.group(2)}).",
    r"(.+) is (?:a|the) brother of (.+)\.": lambda m: f"brother({m.group(1)}, {m.group(2)}).",
    r"(.+) is (?:a|the) sister of (.+)\.": lambda m: f"sister({m.group(1)}, {m.group(2)}).",
    r"(.+) is the mother of (.+)\.": lambda m: f"mother({m.group(1)}, {m.group(2)}).",
    r"(.+) is the father of (.+)\.": lambda m: f"father({m.group(1)}, {m.group(2)}).",
    r"(.+) and (.+) are the parents of (.+)\.": lambda m: f"parents({m.group(1)}, {m.group(2)}, {m.group(3)}).",
    r"(.+) is (?:a|the) grandmother of (.+)\.": lambda m: f"grandmother({m.group(1)}, {m.group(2)}).",
    r"(.+) is (?:a|the) grandfather of (.+)\.": lambda m: f"grandfather({m.group(1)}, {m.group(2)}).",
    r"(.+) is (?:a|the) child of (.+)\.": lambda m: f"child({m.group(1)}, {m.group(2)}).",
    r"(.+), (.+), and (.+) are children of (.+)\.": lambda m: f"children().", # handle properly 
    r"(.+) is (?:a|the) daughter of (.+)\.": lambda m: f"daughter({m.group(1)}, {m.group(2)}).",
    r"(.+) is (?:a|the) son of (.+)\.": lambda m: f"son({m.group(1)}, {m.group(2)}).",
    r"(.+) is (?:an|the) uncle of (.+)\.": lambda m: f"uncle({m.group(1)}, {m.group(2)}).",
    r"(.+) is (?:an|the) aunt of (.+)\.": lambda m: f"aunt({m.group(1)}, {m.group(2)})."
    # TODO: add the "one, two, ..., and n are _ of... capability"
}

question_pattern = {
    # TODO: fix the format prolog string to actual for query
    r"are (.+) and (.+) siblings\?": lambda m: f"sibling().",
    r"is (.+) a sister of (.+)\?": lambda m: f"sister().",
    r"is (.+) a brother of (.+)\?": lambda m: f"brother().",
    r"is (.+) the mother of (.+)\?": lambda m: f"mother().",
    r"is (.+) the father of (.+)\?": lambda m: f"father().",
    r"are (.+) and (.+) the parents of (.+)\?": lambda m: f"parents().",
    r"is (.+) a grandmother of (.+)\?": lambda m: f"grandmother().",
    r"is (.+) a grandfather of (.+)\?": lambda m: f"grandfather().",
    r"is (.+) a daughter of (.+)\?": lambda m: f"daughter().",
    r"is (.+) a son of (.+)\?": lambda m: f"son().",
    r"is (.+) a child of (.+)\?": lambda m: f"child().",
    r"are (.+), and (.+) children of (.+)\?": lambda m: f"children().",
    r"is (.+) an aunt of (.+)\?": lambda m: f"aunt().",
    r"who are the siblings of (.+)\?": lambda m: f"is_sibling_of().",
    r"who are the sisters of (.+)\?": lambda m: f"is_sister_of().",
    r"who are the brothers of (.+)\?": lambda m: f"is_brother_of().",
    r"who is the mother of (.+)\?": lambda m: f"is_mother_of().",
    r"who is the father of (.+)\?": lambda m: f"father_of().",
    r"who are the parents of (.+)\?": lambda m: f"parents_of().",
    r"who are the daughters of (.+)\?": lambda m: f"daughters_of().",
    r"who are the sons of (.+)\?": lambda m: f"sons_of().",
    r"who are the children of (.+)\?": lambda m: f"children_of().",
    r"is (.+) an uncle of (.+)\?": lambda m: f"uncle().",
    r"are (.+) and (.+) relatives\?": lambda m: f"relative()."
}

def statement(user_input):
    # TODO: implement for making facts
    
    # match string pattern with sentence
    for pattern, prolog_format in statement_pattern.items():
        match = re.match(pattern, user_input)
        if match:
            print("statement:", prolog_format(match))
            # TODO: handle fact adding to knowledge base
            # Okay! I learned something  if fact is ok
            # That's impossible!  if violates kb
            return
        
    # if not matched to any statement pattern
    print("I did not understand that statement. Try something else!")
    
        
def query(user_input):
    # match string pattern with sentence
    for pattern, prolog_format in question_pattern.items():
        match = re.match(pattern, user_input)
        if match:
            print("query:", prolog_format(match))
            # TODO: handle fact adding to knowledge base
            return
        
    # if not matched to any statement pattern
    print("I did not understand that question. Try again!")

# test area, abolish this later
def test():
    p = Prolog()
    p.consult("test2.pl")
    
    # facts
    # p.asserta("father(don, olivia)")
    # p.asserta("father(don, elliot)")
    # p.asserta("female(olivia)")
    # p.asserta("male(elliot)")
    
    # query
    for soln in p.query("grandparent(X, Y)"):
        print(soln["X"], "is the grandparent of", soln["Y"])
        
    result = list(p.query("male(X)")) # may have duplicates so set might be needed in future
    print(result)

if __name__ == '__main__': 
    print("Welcome!\n")
    
    # process each input as statement or query
    while True:
        user_input = input("> ").lower().strip()
        
        if "goodbye chat" in user_input or "exit" in user_input:
            print("Goodbye!")
            break # end conversation
        
        elif user_input.endswith("?"):
            query(user_input) # process as query (ALWAYS ENDS WITH ?)
            
        elif user_input.endswith("."):
            statement(user_input) # process as statement (ALWAYS ENDS WITH .)
            
        elif "test" == user_input:
            test()
        else:
            print("A little more punctuation marks would be nice!")
        


