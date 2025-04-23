from pyswip import Prolog
import re 

class FamilyChatbot:
    def __init__(self):
        self.prolog = Prolog()
        #self.prolog.consult("knowledge_base.pl")
        self.prolog.consult("test2.pl")
        
        self.statement_patterns = {
            r"(.+) and (.+) are siblings\.": self.handle_siblings,
            r"(.+) is (?:a|the) sister of (.+)\.": self.handle_sister,
            r"(.+) is the mother of (.+)\.": self.handle_mother,
            r"(.+) is (?:a|the) grandmother of (.+)\.": self.handle_grandmother,
            r"(.+) is (?:a|the) child of (.+)\.": self.handle_child,
            r"(.+) is (?:a|the) daughter of (.+)\.": self.handle_daughter,

            r"(.+) is (?:a|the) brother of (.+)\.": self.handle_brother,
            r"(.+) is the father of (.+)\.": self.handle_father,
            r"(.+) and (.+) are the parents of (.+)\.": self.handle_parents,
            r"(.+) is (?:a|the) grandfather of (.+)\.": self.handle_grandfather,
            r"([a-zA-Z\s]+(?:, [a-zA-Z\s]+)*(?:\s+and\s+[a-zA-Z\s]+)*)(?: are children of )(.+)\.": self.handle_children,
            r"(.+) is (?:a|the) son of (.+)\.": self.handle_son,
            r"(.+) is (?:an|the) aunt of (.+)\.": self.handle_aunt,

            # EVERYTHING BELOW THIS ARE EXTRA QUESTION PROMPTS/NOT IN SPECS
            r"(.+) is (?:an|the) uncle of (.+)\.": self.handle_uncle,       # EXTRA
            r"(.+) is male\.": self.create_male,                            # EXTRA
            r"(.+) is female\.": self.create_female                         # EXTRA
        }
        
        self.query_patterns = {
            r"are (.+) and (.+) siblings\?": self.query_siblings, # _ and _ are siblings
            r"is (.+) (?:a|the) sister of (.+)\?": self.query_sister, # works
            r"is (.+) (?:a|the) brother of (.+)\?": self.query_brother, # doesn't work TODO
            r"is (.+) the mother of (.+)\?": self.query_mother, # works
            r"is (.+) the father of (.+)\?": self.query_father, # works
            r"are (.+) and (.+) the parents of (.+)\?": self.query_parents, # works
            r"is (.+) (?:a|the) grandmother of (.+)\?": self.query_grandmother, # TODO test
            r"is (.+) (?:a|the) daughter of (.+)\?": self.query_daughter, # works
            r"is (.+) (?:a|the) son of (.+)\?": self.query_son, # works!!!! yiypyipipee
            r"is (.+) (?:a|the) child of (.+)\?": self.query_child, # works!!!! yiypyipipee
            # MISSING are _, _, and _ the children of _? - SEE are_children_of() in pl (one for 2 kids, one for 3 kids)
            r"is (.+) (?:an|the) uncle of (.+)\?": self.query_uncle, # TODO MAKE uncle/2
            
            r"who are the siblings of (.+)\?": self.query_siblings_of, # working
            r"who are the sisters of (.+)\?": self.query_sisters_of, # TODO test
            r"who are the brothers of (.+)\?": self.query_brothers_of, # TODO test
            r"who is the mother of (.+)\?": self.query_mother_of, # working
            r"who is the father of (.+)\?": self.query_father_of, # working
            r"who are the parents of (.+)\?": self.query_parents_of,
            r"is (.+) the grandfather of (.+)\?": self.query_grandfather, # TODO MAKE is_gfather_of/2
            r"who are the daughters of (.+)\?": self.query_daughters_of, # semi working
            r"who are the sons of (.+)\?": self.query_sons_of, # semi working
            r"who are the children of (.+)\?": self.query_children_of, # working
            r"is (.+) (?:an|the) aunt of (.+)\?": self.query_aunt, # TODO MAKE aunt/2
            # MISSING are _ and _ relatives?

            # EVERYTHING BELOW THIS ARE EXTRA QUESTION PROMPTS/NOT IN SPECS
            r"who is the grandmother of (.+)\?": self.query_grandmother_of, # semi working
            r"who is the grandfather of (.+)\?": self.query_grandfather_of, # semi working
            r"who is the aunt of (.+)\?": self.query_aunt_of # wrong wording is _ an aunt of _?
        }

    def validate_gender(self, name, relationship_type):
        """Validate gender-specific relationships"""
        male_predicates = ['father', 'brother', 'son', 'uncle', 'grandfather']
        female_predicates = ['mother', 'sister', 'daughter', 'aunt', 'grandmother']
        
        try:
            if any(pred in relationship_type for pred in male_predicates):
                return bool(list(self.prolog.query(f"male({name})")))
            
            if any(pred in relationship_type for pred in female_predicates):
                return bool(list(self.prolog.query(f"female({name})")))
            
            return True
        except Exception:
            return False
# =================================================================================================  
# -------------------- wait wait wait wait -------------------- #
    def create_male(self, name):
        try:
            if list(self.prolog.query(f"male({name})")):
                print(f"{name} is already recorded as male.")
            else:
                self.prolog.assertz(f"male({name})")
                print(f"OK! I added {name} as a male.")
        except Exception as e:
            print(f"Error creating male person: {e}")

    def create_female(self, name):
        try:
            if list(self.prolog.query(f"female({name})")):
                print(f"{name} is already recorded as female.")
            else:
                self.prolog.assertz(f"female({name})")
                print(f"OK! I added {name} as a female.")
        except Exception as e:
            print(f"Error creating female person: {e}")
        
# =================================================================================================  
# -------------------- Handler Methods -------------------- #
    def handle_siblings(self, person1, person2):
        """Handle sibling statement"""
        try:
            # Check if they aren't the same person
            if person1 == person2:
                print("That's impossible! A person cannot be their own sibling.")
                return
            
            # First, ensure both exist in the knowledge base
            self.prolog.assertz(f"sibling({person1}, {person2})")
            self.prolog.assertz(f"sibling({person2}, {person1})")
            print(f"OK! I learned that {person1} and {person2} are siblings.")
        except Exception as e:
            print(f"Error adding sibling relationship: {e}")

    def handle_brother(self, brother, person):
        """Handle brother statement"""
        if not self.validate_gender(brother, 'brother'):
            print(f"That's impossible! {brother} cannot be a brother.")
            return
        
        try:
            self.prolog.assertz(f"sibling({brother}, {person})")
            self.prolog.assertz(f"male({brother})")
            print(f"OK! I learned that {brother} is the brother of {person}.")
        except Exception as e:
            print(f"Error adding brother relationship: {e}")

    def handle_sister(self, sister, person):
        """Handle sister statement"""
        if not self.validate_gender(sister, 'sister'):
            print(f"That's impossible! {sister} cannot be a sister.")
            return
        
        try:
            self.prolog.assertz(f"sister({sister}, {person})")
            self.prolog.assertz(f"sibling({sister}, {person})")
            self.prolog.assertz(f"female({sister})")
            print(f"OK! I learned that {sister} is the sister of {person}.")
        except Exception as e:
            print(f"Error adding sister relationship: {e}")

    def handle_mother(self, mother, child):
        """Handle mother statement"""
        if not self.validate_gender(mother, 'mother'):
            print(f"That's impossible! {mother} cannot be a mother.")
            return
        
        try:
            self.prolog.assertz(f"mother({mother}, {child})")
            self.prolog.assertz(f"female({mother})")
            print(f"OK! I learned that {mother} is the mother of {child}.")
        except Exception as e:
            print(f"Error adding mother relationship: {e}")
            
    def handle_father(self, father, child):
        """Handle father statement"""
        if not self.validate_gender(father, 'father'):
            print(f"That's impossible! {father} cannot be a father.")
            return
        
        try:
            self.prolog.assertz(f"father({father}, {child})")
            self.prolog.assertz(f"male({father})")
            print(f"OK! I learned that {father} is the father of {child}.")
        except Exception as e:
            print(f"Error adding father relationship: {e}")

    def handle_parents(self, father, mother, child):
        """Handle parents statement"""
        try:
            # First validate both parents
            if not self.validate_gender(father, 'father') or not self.validate_gender(mother, 'mother'):
                print("That's impossible! Invalid parent relationship.")
                return
            
            self.prolog.assertz(f"father({father}, {child})")
            self.prolog.assertz(f"mother({mother}, {child})")
            self.prolog.assertz(f"male({father})")
            self.prolog.assertz(f"female({mother})")
            print(f"OK! I learned that {father} and {mother} are the parents of {child}.")
        except Exception as e:
            print(f"Error adding parents relationship: {e}")
            
    def handle_grandmother(self, grandmother, child):
        if not self.validate_gender(grandmother, "grandmother"):
            print(f"That's impossible! {grandmother} cannot be a grandmother.")
            return
        try:
            self.prolog.assertz(f"grandparent({grandmother}, {child})")
            self.prolog.assertz(f"female({grandmother})")
            print(f"OK! I learned that {grandmother} is the grandmother of {child}.")
        except Exception as e:
            print(f"Error adding grandmother relationship: {e}")

    def handle_grandfather(self, grandfather, child):
        if not self.validate_gender(grandfather, "grandfather"):
            print(f"That's impossible! {grandfather} cannot be a grandfather.")
            return
        try:
            self.prolog.assertz(f"grandparent({grandfather}, {child})")
            self.prolog.assertz(f"male({grandfather})")
            print(f"OK! I learned that {grandfather} is the grandfather of {child}.")
        except Exception as e:
            print(f"Error adding grandfather relationship: {e}")

    def handle_child(self, child, parent):
        try:
            # Assert the parent relationship
            self.prolog.assertz(f"parent({parent}, {child})")
            
            # If the parent is male, assert father relationship
            male_check = list(self.prolog.query(f"male({parent})"))
            if male_check:
                self.prolog.assertz(f"father({parent}, {child})")
            
            # If the parent is female, assert mother relationship
            female_check = list(self.prolog.query(f"female({parent})"))
            if female_check:
                self.prolog.assertz(f"mother({parent}, {child})")

            # Assert sibling relationships by checking other parents
            siblings = list(self.prolog.query(f"parent({parent}, X), X \\= {child}"))
            for sibling in siblings:
                self.prolog.assertz(f"sibling({child}, {sibling['X']})")
                self.prolog.assertz(f"sibling({sibling['X']}, {child})")

            print(f"OK! I learned that {child} is the child of {parent}.")
        except Exception as e:
            print(f"Error adding child relationship: {e}")

    def handle_children(self, children, parent):
        try:
            children = children.split(", ") 
            print(children, parent)
            if children:
                last = children.pop()
                add = [child.strip() for child in last.split("and ")]
                children.extend(add)  # add parsed names ("x and y") back to the list
            
            children = [child for child in children if child.strip()] # removes " " as elem
            
            for child in children:
                print(f"parent({parent}, {child})")
                self.prolog.assertz(f"parent({parent}, {child})")
                
            # make output sentence
            if len(children) == 2:
                # if two children
                sentence = f"OK! I learned that {children[0]} and {children[1]} are children of {parent}."
            else:
                # three or more 
                formatted_children = ", ".join(children[:-1]) + f", and {children[-1]}"
                sentence = f"OK! I learned that {formatted_children} are children of {parent}."
            print(sentence)
        except Exception as e:
            print(f"Error adding multiple children relationship: {e}")

    def handle_son(self, son, parent):
        if not self.validate_gender(son, "son"):
            print(f"That's impossible! {son} cannot be a son.")
            return
        try:
            self.prolog.assertz(f"parent({parent}, {son})")
            self.prolog.assertz(f"male({son})")
            print(f"OK! I learned that {son} is the son of {parent}.")
        except Exception as e:
            print(f"Error adding son relationship: {e}")

    def handle_daughter(self, daughter, parent):
        if not self.validate_gender(daughter, "daughter"):
            print(f"That's impossible! {daughter} cannot be a daughter.")
            return
        try:
            self.prolog.assertz(f"parent({parent}, {daughter})")
            self.prolog.assertz(f"female({daughter})")
            print(f"OK! I learned that {daughter} is the daughter of {parent}.")
        except Exception as e:
            print(f"Error adding daughter relationship: {e}")

    def handle_uncle(self, uncle, child):
        if not self.validate_gender(uncle, "uncle"):
            print(f"That's impossible! {uncle} cannot be an uncle.")
            return
        try:
            self.prolog.assertz(f"uncle({uncle}, {child})")
            print(f"OK! I learned that {uncle} is the uncle of {child}.")
        except Exception as e:
            print(f"Error adding uncle relationship: {e}")

    def handle_aunt(self, aunt, child):
        if not self.validate_gender(aunt, "aunt"):
            print(f"That's impossible! {aunt} cannot be an aunt.")
            return
        try:
            self.prolog.assertz(f"aunt({aunt}, {child})")
            print(f"OK! I learned that {aunt} is the aunt of {child}.")
        except Exception as e:
            print(f"Error adding aunt relationship: {e}")

# =================================================================================================  
# -------------------- Query Methods -------------------- #
    def query_siblings(self, person1, person2):
        """Check if two people are siblings"""
        result = list(self.prolog.query(f"sibling({person1}, {person2})"))
        print("Yes" if result else "No")

    def query_brother(self, person1, person2):
        """Check if person1 is the brother of person2"""
        result = list(self.prolog.query(f"is_brother_of({person1}, {person2})"))
        print("Yes" if result else "No")

    def query_sister(self, person1, person2):
        """Check if person1 is the sister of person2"""
        result = list(self.prolog.query(f"is_sister_of({person1}, {person2})"))
        print("Yes" if result else "No")

    def query_mother(self, person1, person2):
        """Check if person1 is the mother of person2"""
        result = list(self.prolog.query(f"is_mother_of({person1}, {person2})"))
        print("Yes" if result else "No")

    def query_father(self, person1, person2):
        """Check if person1 is the father of person2"""
        result = list(self.prolog.query(f"is_father_of({person1}, {person2})"))
        print("Yes" if result else "No")

    def query_parents(self, person1, person2, person3):
        """Check if person1 and person2 are parents of person3"""
        result = list(self.prolog.query(f"parent({person1}, {person3}), parent({person2}, {person3})"))
        print("Yes" if result else "No")
    
    def query_siblings_of(self, person):
        """Find siblings of a person"""
        result = list(self.prolog.query(f"is_sibling_of({person}"))
        if result:
            siblings = [x['X'] for x in result if x['X'] != person]
            if siblings:
                print(f"Siblings of {person}: {', '.join(siblings)}")
            else:
                print(f"{person} has no siblings.")
        else:
            print(f"{person} has no siblings.")

    def query_sisters_of(self, person):
        """"Find sisters of a person"""
        result = list(self.prolog.query(f"is_sister_of({person})"))
        if result:
            sisters = [x['X'] for x in result if x['X'] != person]
            if sisters:
                print(f"Sisters of {person}: {', '.join(sisters)}")
            else:
                print(f"{person} has no sisters.")
        else:
            print(f"{person} has no sisters.")
            
    def query_brothers_of(self, person):
        """"Find brothers of a person"""
        result = list(self.prolog.query(f"is_brother_of({person})"))
        if result:
            brothers = [x['X'] for x in result if x['X'] != person]
            if brothers:
                print(f"Brothers of {person}: {', '.join(brothers)}")
            else:
                print(f"{person} has no brothers.")
        else:
            print(f"{person} has no brothers.")
        
    
    def query_mother_of(self, person):
        """Find mother of a person"""
        result = list(self.prolog.query(f"is_mother_of({person})"))
        if result:
            print(f"Mother of {person}: {result[0]['X']}")
        else:
            print(f"No mother found for {person}")

    def query_father_of(self, person):
        """Find father of a person"""
        result = list(self.prolog.query(f"is_father_of({person})"))
        if result:
            print(f"Father of {person}: {result[0]['X']}")
        else:
            print(f"No father found for {person}")
            
    def query_parents_of(self, person):
        """Find parents of a person"""
        result = list(self.prolog.query(f"are_parents_of({person})"))
        if result:
            print(f"parents of {person}: {result[0]['X']} and {result[0]['Y']}")
        else:
            print(f"No parents found for {person}")
            
    def query_grandmother_of(self, person):
        """Find grandmother of a person"""
        result = list(self.prolog.query(f"is_grandmother_of({person})"))
        if result:
            print(f"Grandmother of {person}: {result[0]['X']}")
        else:
            print(f"No grandmother found for {person}.")

    def query_grandmother(self, person1, person2):
        """Check if person1 is the grandmother of person2"""
        result = list(self.prolog.query(f"is_grandmother_of({person1}, {person2})")) 
        print("Yes" if result else "No")
    
    def query_grandfather_of(self, person):
        """Find grandfather of a person"""
        result = list(self.prolog.query(f"is_grandfather_of({person})"))
        if result:
            print(f"Grandfather of {person}: {result[0]['X']}")
        else:
            print(f"No grandfather found for {person}.")

    def query_daughter(self, person1, person2):
        """Check if person1 is the daughter of person2"""
        result = list(self.prolog.query(f"is_daughter_of({person1}, {person2})")) 
        print("Yes" if result else "No")
        
    def query_son(self, person1, person2):
        """Check if person1 is the son of person2"""
        result = list(self.prolog.query(f"is_son_of({person1}, {person2})")) 
        print("Yes" if result else "No")
    
    def query_child(self, person1, person2):
        """Check if person1 is the child of person2"""
        result = list(self.prolog.query(f"is_child_of({person1}, {person2})")) 
        print("Yes" if result else "No")

    def query_children_of(self, person):
        """Find the children of a person"""
        result = list(self.prolog.query(f"is_children_of({person})."))
        children = [res["X"] for res in result]
        print(f"Children of {person}: {', '.join(children)}" if children else f"{person} has no children.")

    def query_aunt(self, person1, person2):
        """Check if person1 is the aunt of person2"""
        result = list(self.prolog.query(f"is_aunt_of({person1}, {person2})")) 
        print("Yes" if result else "No")
    
    def query_grandfather(self, person1, person2):
        """Check if person1 is the grandfather of person2"""
        result = list(self.prolog.query(f"is_grandfather_of({person1}, {person2})")) 
        print("Yes" if result else "No")
    
    def query_daughters_of(self, person):
        result = list(self.prolog.query(f"is_daughter_of({person})"))
        daughters = [res["X"] for res in result]
        print(f"Daughters of {person}: {', '.join(daughters)}" if daughters else f"{person} has no daughters.")

    def query_sons_of(self, person):
        result = list(self.prolog.query(f"is_son_of({person})"))
        sons = [res["X"] for res in result]
        print(f"Sons of {person}: {', '.join(sons)}" if sons else f"{person} has no sons.")

    def query_uncle(self, person1, person2):
        """Check if person1 is the uncle of person2"""
        result = list(self.prolog.query(f"is_uncle_of({person1}, {person2})")) 
        print("Yes" if result else "No")

    def query_aunt_of(self, person):
        result = list(self.prolog.query(f"aunt(X, {person})."))
        aunts = [res["X"] for res in result]
        print(f"Aunts of {person}: {', '.join(aunts)}" if aunts else f"{person} has no aunts.")
        
           
# =================================================================================================            
    # Process a statement about family relationships
    def process_statement(self, statement):
        for pattern, handler in self.statement_patterns.items():
            match = re.match(pattern, statement)
            if match:
                groups = match.groups()
                handler(*groups)
                return
        print("I did not understand that statement. Try something else!")

    # Process a query about family relationships
    def process_query(self, query):
        for pattern, handler in self.query_patterns.items():
            match = re.match(pattern, query)
            if match:
                groups = match.groups()
                handler(*groups)
                return
        print("I did not understand that question. Try again!")
        
# =================================================================================================
# -------------------- Main Function -------------------- #  
def main():
    chatbot = FamilyChatbot()
    print("Family Relationship Chatbot")
    print("Enter statements or questions about family relationships.")
    print("Type 'goodbye' to exit.")
    
    while True:
        user_input = input("> ").strip()
        
        if user_input.lower() in ['goodbye', 'exit']:
            print("Goodbye!")
            break
        
        try:
            if user_input.endswith('?'):
                chatbot.process_query(user_input)
            elif user_input.endswith('.'):
                chatbot.process_statement(user_input)
            else:
                print("Please end your input with '?' or '.'")
        
        except Exception as e:
            print(f"Error processing input: {e}")

if __name__ == '__main__':
    main()