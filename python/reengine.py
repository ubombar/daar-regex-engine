import copy

class Token():
    CHAR = 0
    CONCAT = 1
    OR = 2
    RP = 3
    LP = 4
    STAR = 5
    ANY = 6
    PLUS = 7

    def __init__(self, ttype, data) -> None:
        self.ttype = ttype
        self.data = data
    
    def __str__(self) -> str:
        if self.ttype == Token.CHAR:
            return f"CHAR({self.data})"
        elif self.ttype == Token.CONCAT:
            return "CONCAT"
        elif self.ttype == Token.OR:
            return "OR"
        elif self.ttype == Token.RP:
            return "RP"
        elif self.ttype == Token.LP:
            return "LP"
        elif self.ttype == Token.STAR:
            return "STAR"
        elif self.ttype == Token.ANY:
            return "ANY"
        elif self.ttype == Token.PLUS:
            return "PLUS"

    def __repr__(self) -> str:
        return str(self)
    
def char_token(data):
    return Token(Token.CHAR, data)

def concat_token():
    return Token(Token.CONCAT, None)

def or_token():
    return Token(Token.OR, None)

def lp_token():
    return Token(Token.LP, None)

def rp_token():
    return Token(Token.RP, None)

def star_token():
    return Token(Token.STAR, None)

def plus_token():
    return Token(Token.PLUS, None)

def any_token():
    return Token(Token.ANY, ".")

def tokenize(regex) -> list[Token]:
    # Step 1: convert it to 
    char_list = list(regex)

    # Step 2: Tokenized
    token_list = []
    for char in char_list:
        if char == '(':
            token_list.append(lp_token())
        elif char == ')':
            token_list.append(rp_token())
        elif char == '.':
            token_list.append(any_token())
        elif char == '*':
            token_list.append(star_token())
        elif char == '|':
            token_list.append(or_token())
        elif char == '+':
            token_list.append(plus_token())
        else:
            token_list.append(char_token(char))
    
    return token_list

def merge_tokenized(tokenized_list: list[Token]):
    def merge_tokens(token_list: list[Token]):
        return char_token(''.join([t.data for t in token_list]))
     
    merged_tokenized_list: list[Token] = []
    i = 0
    while i < len(tokenized_list):
        currnet_token = tokenized_list[i]

        # If the current one is a char token
        if currnet_token.ttype in {Token.CHAR}:
            j = i + 1
            while j < len(tokenized_list):
                if tokenized_list[j].ttype not in {Token.CHAR}: break
                j += 1

            # 
            if j == len(tokenized_list):
                slice_to_merge = tokenized_list[i:j]
                one_token = merge_tokens(slice_to_merge)
                merged_tokenized_list.append(one_token)
                break
            elif tokenized_list[j].ttype in {Token.STAR, Token.PLUS}:
                slice_to_merge = tokenized_list[i:j - 1]
                one_token = merge_tokens(slice_to_merge)
                second_token = tokenized_list[j - 1]
                merged_tokenized_list.append(one_token)
                merged_tokenized_list.append(second_token)
                i = j - 1
            else:
                slice_to_merge = tokenized_list[i:j]
                one_token = merge_tokens(slice_to_merge)
                merged_tokenized_list.append(one_token)
                i = j - 1
        else:
            merged_tokenized_list.append(currnet_token)
        i += 1
                
    return [x for x in merged_tokenized_list if not (x.ttype == Token.CHAR and len(x.data) == 0)]

def add_concat_symbol(token_list: list[Token]):
    def get_token_value(token: Token):
        if token.ttype in {Token.CHAR, Token.ANY}:
            return 1
        elif token.ttype == Token.LP:
            return 2
        elif token.ttype == Token.RP:
            return 3
        elif token.ttype in {Token.PLUS, Token.STAR}:
            return 4
        return 0
    
    i = 0
    out = copy.deepcopy(token_list)
    while i < len(out) - 1:
        tok1 = get_token_value(out[i])
        tok2 = get_token_value(out[i + 1])

        if tok1 != 0 and tok2 != 0: 
            if (tok1, tok2) in {(1, 1), (3, 1), (1, 2), (3, 2), (4, 1), (4, 2)}:
                out = out[:i+1] + [concat_token()] + out[i+1:]
                i += 1
        i += 1
        
    return out

def regex_to_postfix(token_list: list[Token]):
    precedence = {Token.STAR: 5, Token.PLUS: 4, Token.CONCAT: 2, Token.OR: 1}
    stack: list[Token] = []
    postfix = []

    for tok in token_list:
        if tok.ttype in {Token.CHAR, Token.ANY}:
            postfix.append(tok)
        elif tok.ttype == Token.LP:
            stack.append(tok)
        elif tok.ttype == Token.RP:
            while stack and stack[-1].ttype != Token.LP:
                postfix.append(stack.pop())
            stack.pop()  # Pop the opening parenthesis
        else:
            while stack and precedence.get(stack[-1].ttype, 0) >= precedence.get(tok.ttype, 0):
                postfix.append(stack.pop())
            stack.append(tok)

    while stack:
        postfix.append(stack.pop())

    return postfix

class SyntaxTreeNode:
    def __init__(self, value, left=None, right=None):
        self.value: Token = value
        self.left = left
        self.right = right

def print_syntax_tree(node: SyntaxTreeNode, level=0):
    if not node:
        return
    space = "\t" * level 
    print(space, f"'{node.value}'")
    print_syntax_tree(node.left, level + 1)
    print_syntax_tree(node.right, level + 1)

def build_expression_tree(postfix_token_list: list[Token]):
    stack = []

    for tok in postfix_token_list:
        if tok.ttype in {Token.CHAR, Token.ANY}:
            node = SyntaxTreeNode(tok)
            stack.append(node)
        elif tok.ttype in {Token.CONCAT, Token.OR}:
            right = stack.pop()
            left = stack.pop()
            node = SyntaxTreeNode(tok)
            node.left = left
            node.right = right
            stack.append(node)
        elif tok.ttype in {Token.PLUS, Token.STAR}:
            child = stack.pop()
            node = SyntaxTreeNode(tok)
            node.left = child
            stack.append(node)

    return stack[0]


class NDFA():
    def __init__(self) -> None:
        # default is to have only one state without accepting
        self.starting_state = 0
        self.__last_generated_state = 0
        self.accepting_states = set()
        self.graph_dict = {self.starting_state: []}
        
    def __gen_state(self) -> int:
        self.__last_generated_state += 1
        return self.__last_generated_state
    
    def get_alphabet(self) -> set[str]:
        alphabet_set: set[str] = set()
        for _, transition_list in self.graph_dict.items():
            for (_, token) in transition_list:
                alphabet_set.add(token)
        return alphabet_set
    
    def epsilon_closure_of(self, states: set[int]) -> set[int]:
        '''Calculates the epsilon closure plus the given string. Returns them as a sorted list'''
        epsilon_visited_states = set()
        queue = list(states)

        # First find the epsilon transition states
        while queue:
            c_state = queue.pop()
            epsilon_visited_states.add(c_state)

            for (next_state, match_string) in self.graph_dict[c_state]:
                if match_string == "" and (next_state not in epsilon_visited_states): # Means this is an epsilon transition
                    queue.append(next_state)

        return epsilon_visited_states
    
    def input_closure_of(self, states: int, string: str) -> set[int]:
        '''Calculates the epsilon closure plus the given string. Returns them as a sorted list'''
        visited_states = set()

        # First find the epsilon transition states
        for state in states:
            for (next_state, match_string) in self.graph_dict[state]:
                if match_string == string: # Means this is an epsilon transition
                    visited_states.add(next_state)

        return visited_states
    
    def get_closure_of(self, state: int, string: int) -> tuple[int]:
        a = self.epsilon_closure_of({state})
        b = self.input_closure_of(a, string)
        c = self.epsilon_closure_of(b)

        return tuple(sorted(c))
    
    def new_state(self) -> int:
        generated_state = self.__gen_state()
        self.graph_dict[generated_state] = []
        return generated_state
    
    def merge_ndfa(self, ndfa):
        '''Merges the state diagram of another NDFA while chaning the state names to enable multiple mergers of the same NDFA.'''

        # Copy the states except the starting state from the old ndfa since we will be merging it.
        name_translations = {old_state: self.new_state() for old_state in ndfa.graph_dict.keys()}

        for from_old_state, transition_list in ndfa.graph_dict.items():
            from_new_state = name_translations[from_old_state]
            for (to_old_state, symbol) in transition_list:
                to_new_state = name_translations[to_old_state]
                self.add_transition(from_new_state, to_new_state, symbol)
        
        return name_translations
    
    def add_transition(self, from_state: int, to_state: int, symbol):
        '''For e-transitions add empty string. Not testing the validity of the incoming states!'''
        self.graph_dict[from_state].append((to_state, symbol))

    def add_ndfa(self, from_state, to_state, ndfa):
        '''Adds the given ndfa to the current one with the symbol/epsilon'''
        # Concatinate the graphs
        name_translations = self.merge_ndfa(ndfa)
        
        # Connect the from_state to the starting state of the child ndfa
        self.add_transition(from_state, name_translations[ndfa.starting_state], "")

        # Connect the accepting states of the child ndfa to the to_state, 
        # note that this connection is an epsilon transition
        for accepting_state in ndfa.accepting_states:
            self.add_transition(name_translations[accepting_state], to_state, "")

    def new_symbol_matcher(symbol):
        '''Match any given symbol'''
        ndfa = NDFA()
        accepting_state = ndfa.new_state()

        ndfa.add_transition(ndfa.starting_state, accepting_state, symbol)
        ndfa.accepting_states.add(accepting_state)

        return ndfa
    
    def new_or_ndfa(ndfa1, ndfa2):
        ndfa = NDFA()
        accepting_state = ndfa.new_state()

        ndfa.add_ndfa(ndfa.starting_state, accepting_state, ndfa1)
        ndfa.add_ndfa(ndfa.starting_state, accepting_state, ndfa2)

        ndfa.accepting_states.add(accepting_state)

        return ndfa
    
    def new_plus_ndfa(ndfa1):
        ndfa = NDFA()
        accepting_state = ndfa.new_state()

        ndfa.add_ndfa(ndfa.starting_state, accepting_state, ndfa1)
        ndfa.add_ndfa(accepting_state, accepting_state, ndfa1)

        ndfa.accepting_states.add(accepting_state)

        return ndfa
    
    def new_star_ndfa(ndfa1):
        ndfa = NDFA()
        accepting_state = ndfa.new_state()

        ndfa.add_transition(ndfa.starting_state, accepting_state,  "") # epsilon trans
        ndfa.add_ndfa(accepting_state, accepting_state, ndfa1)

        ndfa.accepting_states.add(accepting_state)

        return ndfa
    
    def new_concat_ndfa(ndfa1, ndfa2):
        ndfa = NDFA()
        middle_state = ndfa.new_state()
        accepting_state = ndfa.new_state()

        ndfa.add_ndfa(ndfa.starting_state, middle_state, ndfa1)
        ndfa.add_ndfa(middle_state, accepting_state, ndfa2)

        ndfa.accepting_states.add(accepting_state)

        return ndfa

# def draw_graph(ndfa: NDFA):
#     g = nx.DiGraph()
#     color_map = []

#     for state in ndfa.graph_dict.keys():
#         g.add_node(state)

#         if state == ndfa.starting_state:
#             color_map.append("green")
#         elif state in ndfa.accepting_states:
#             color_map.append("red")
#         else:
#             color_map.append("blue")

#     # g.add_nodes_from(ndfa.graph_dict.keys())
#     edge_labels = {}

#     for from_state, to_state_list in ndfa.graph_dict.items():
#         for to_state, label in to_state_list:
#             g.add_edge(from_state, to_state)
#             edge_labels[(from_state, to_state)] = label if label != "" else "ϵ"

#     # print("starting state", ndfa.starting_state)
#     # print("acceping states", ndfa.accepting_states)

#     layout = nx.circular_layout(g)
#     nx.draw_networkx(g, with_labels=True, pos=layout, node_color=color_map)

#     nx.draw_networkx_edge_labels(
#         g,
#         pos=layout,
#         edge_labels=edge_labels,
#         # node_color=color_map,
#         # node_color=range(24),
#     )

#     plt.show()


def create_non_epsilon_ndfa(old_ndfa: NDFA):
   new_ndfa = NDFA()
   
   # Copy the states of the old ndfa to the new one without any transitions / accepting states.
   for state in old_ndfa.graph_dict.keys():
       if state == old_ndfa.starting_state: continue # Default constructor alreadyt adds starting state
       new_ndfa.graph_dict[state] = []

   for string in old_ndfa.get_alphabet():
      if string == "": continue # Skip the epsilon transition
      for state in old_ndfa.graph_dict.keys():
         # Does a bfs to find the closure of the reachable states.
         epsilon_closure = old_ndfa.epsilon_closure_of({state}) # Get the null-closure
         input_closure = old_ndfa.input_closure_of(epsilon_closure, string)
         transitioned_states = old_ndfa.epsilon_closure_of(input_closure) # Get full transitions
         # transition_tupled = tuple(sorted(transition)) # Convert into a sorted tuple for hashing

         # If the intersaction is not empty then this state should be marked as accepting state.
         if old_ndfa.accepting_states.intersection(epsilon_closure):
            new_ndfa.accepting_states.add(state)
         
         # Connect the transitions
         for transtion_state in transitioned_states:
             new_ndfa.add_transition(state, transtion_state, string)
   
   return new_ndfa

def delete_unreachable_states(old_ndfa):
   new_ndfa: NDFA = copy.deepcopy(old_ndfa)

   all_states_without_incoming = {state for state in new_ndfa.graph_dict.keys()} # starting state has incoming by nature
   all_states_without_incoming.remove(new_ndfa.starting_state)

   for _, transition_list in new_ndfa.graph_dict.items():
      for to_state, _ in transition_list:
         if to_state in all_states_without_incoming:
            all_states_without_incoming.remove(to_state)

   # print(all_states_without_incoming)

   for state_to_be_removed in all_states_without_incoming:
      # Remove the transition table
      new_ndfa.graph_dict.pop(state_to_be_removed)

      # Remove the state information from the accepting states
      if state_to_be_removed in new_ndfa.accepting_states:
         new_ndfa.accepting_states.remove(state_to_be_removed)
   return new_ndfa


def match(ndfa: NDFA, remaning_string: str, current_state: int=None) -> bool:
    if not current_state:
        current_state = ndfa.starting_state

    # if the remaning_string is empty
    if not remaning_string:
        # If this is the case, check if the current state is in the accepting state
        return current_state in ndfa.accepting_states 
    else:
        # run for each transition of the current state
        for to_state, matcher_string in ndfa.graph_dict[current_state]:
            if remaning_string.startswith(matcher_string): # this can be optimized
                reduced_string = remaning_string[len(matcher_string):]
                if match(ndfa, reduced_string, to_state):
                    return True
    return False

def generate_ndfa(node: SyntaxTreeNode):
    if not node:
        return None 
    
    # if leaf?
    if not node.left and not node.right:
        if node.value.ttype == Token.ANY:
            return NDFA.new_symbol_matcher(".")
        else:
            return NDFA.new_symbol_matcher(node.value.data)
    # is binary operator?
    elif node.left and node.right:
        if node.value.ttype == Token.OR: # or type operand
            generated_ndfa_left = generate_ndfa(node.left)
            generated_ndfa_right = generate_ndfa(node.right)
            return NDFA.new_or_ndfa(generated_ndfa_left, generated_ndfa_right)
        elif node.value.ttype == Token.CONCAT: # concat type operand
            generated_ndfa_left = generate_ndfa(node.left)
            generated_ndfa_right = generate_ndfa(node.right)
            return NDFA.new_concat_ndfa(generated_ndfa_left, generated_ndfa_right)
        else:
            raise Exception(f"unknown binary operand '{node.value}'")
    # is unary operator?
    elif node.left and not node.right: 
        if node.value.ttype == Token.STAR: # 
            generated_ndfa = generate_ndfa(node.left) 
            return NDFA.new_star_ndfa(generated_ndfa)
        elif node.value.ttype == Token.PLUS: # 
            generated_ndfa = generate_ndfa(node.left) 
            return NDFA.new_plus_ndfa(generated_ndfa)
    else:
        raise Exception("syntax tree node cannot have a unary operator with left side null")

class REEngine:
    def __init__(self, regex: str) -> None:
        # The pipeline
        tokenized_list = tokenize(regex)
        merged_tokenized_list = merge_tokenized(tokenized_list)
        concated_and_merged_token_list = add_concat_symbol(merged_tokenized_list)
        postfix_token_list = regex_to_postfix(concated_and_merged_token_list)
        root = build_expression_tree(postfix_token_list)
        ndfa = generate_ndfa(root)
        nonep_ndfa = create_non_epsilon_ndfa(ndfa)
        nonep_minimized_ndfa = delete_unreachable_states(nonep_ndfa)

        self.__ndfa = nonep_minimized_ndfa
    
    def match_line(self, line: str) -> bool:
        return match(self.__ndfa, line)

def compile(regex: str) -> REEngine:
    return REEngine(regex)
