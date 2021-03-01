# -*- coding: utf-8 -*-
"""Lab06_Rezolutie_Skel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LBmwrrnoK0Fq7xAF1AcqDDQ-QwHLb1Nu

# Logica cu predicate (2). Rezoluție
 - Andrei Olaru
 - Tudor Berariu

## Scopul laboratorului

Familiarizarea cu mecanismul rezoluției și cu strategiile de rezoluție.

#### Resurse

Cursul 5 de IA slides 34-44.

### Cerința 1

* din notebook-ul de la Laboratorul 5 faceți Download as &rarr; Python și salvați fișierul ca `Lab05.py`, în acest director.
* adăugați de asemenea în acest director fișierul `Lab05tester.py` (**descărcați din nou** de pe site).
"""

# TODO
from LPTester import *
from Lab05 import *

from copy import deepcopy
from functools import reduce

# în această celulă se găsesc câteva funcții utilizate intern

dummy = make_atom("P")
[and_name, or_name, neg_name] = [get_head(s) for s in [make_and(dummy, dummy), make_or(dummy, dummy), make_neg(dummy)]]
def pFail(message, f):
    print(message + " <" + str(f) + ">")
    return False
def check_term(T):
    if is_constant(T):
        return (get_value(T) is not None) or pFail("The value of the constant is None", T)
    if is_variable(T):
        return (get_name(T) is not None) or pFail("The name of the variable is None", T)
    if is_function_call(T):
        return not [t for t in get_args(T) if not check_term(t)] and \
            (get_head(T) is not None or pFail("Function is not callable", T))
    return pFail("Term is not one of constant, variable or function call", T)
def check_atom(A):
    if is_atom(A):
        return not [t for t in get_args(A) if not check_term(t)] and \
            (get_head(A) is not None or pFail("Predicate name is None", A))
    return pFail("Is not an atom", A)
def check_sentence(S):
    if is_atom(S):
        return check_atom(S)
    if is_sentence(S):
        if get_head(S) in [and_name, or_name]:
            return (len(get_args(S)) >= 2 or pFail("Sentence has too few operands", S)) \
                and not [s for s in get_args(S) if not check_sentence(s)]
        if get_head(S) == neg_name:
            return (len(get_args(S)) == 1 or pFail("Negative sentence has not just 1 operand", S)) \
                and check_sentence(get_args(S)[0])
    return pFail("Not sentence or unknown type", S)

def add_statement(kb, conclusion, *hypotheses):
    s = conclusion if not hypotheses else make_or(*([make_neg(s) for s in hypotheses] + [conclusion]))
    if check_sentence(s):
        kb.append(s)
        print("OK: Added statement " + print_formula(s, True))
        return True
    print("-- FAILED CHECK: Sentence does not check out <"+print_formula(s, True)+"><" + str(s) + ">")
    return False

var_no = 0;

def assign_next_var_name():
    global var_no
    var_no += 1
    return "v" + str(var_no)

def gather_vars(S):
    return [get_name(S)] if is_variable(S) else \
        [] if not has_args(S) else reduce(lambda res, a: res + gather_vars(a), get_args(S), [])

def make_unique_var_names(KB):
    global var_no
    var_no = 0
    return [substitute(S, {var: make_var(assign_next_var_name()) for var in gather_vars(S)}) for S in KB]           
            
def print_KB(KB):
    print("KB now:")
    for s in KB:
        print("\t\t\t" + print_formula(s, True))

# KB 1
# based on an example in Artificial Intelligence - A Modern Approach
KB_America = []
#0 Mr West is a US general
add_statement(KB_America, make_atom("USGeneral", make_const("West")))
#1 General Awesome is also a US general
add_statement(KB_America, make_atom("USGeneral", make_const("General_Awesome")))
#2 General Awesome is Awesome
add_statement(KB_America, make_atom("Awesome", make_const("General_Awesome")))
#3 Nono is an enemy of America
add_statement(KB_America, make_atom("Enemy", make_const("Nono"), make_const("America")))
#4 M1 is a type of missile
add_statement(KB_America, make_atom("Missile", make_const("M1")))
#5 Nono has the M1 missile
add_statement(KB_America, make_atom("Owns", make_const("Nono"), make_const("M1")))

#6 any US general is an American
add_statement(KB_America, make_atom("American", make_var("x")), make_atom("USGeneral", make_var("x")))
#7 any missle is a weapon
add_statement(KB_America, make_atom("Weapon", make_var("x")), make_atom("Missile", make_var("x")))
#8 if anyone owns a missile, it is General West that sold them that missile
add_statement(KB_America, make_atom("Sells", make_const("West"), make_var("y"), make_var("x")), make_atom("Owns", make_var("x"), make_var("y")), make_atom("Missile", make_var("y")))
#9 any American who sells weapons to a hostile is a criminal
add_statement(KB_America, make_atom("Criminal", make_var("x")), make_atom("Weapon", make_var("y")), make_atom("Sells", make_var("x"), make_var("y"), make_var("z")), make_atom("Hostile", make_var("z")), make_atom("American", make_var("x")))
#10 any enemy of America is called a hostile
add_statement(KB_America, make_atom("Hostile", make_var("x")), make_atom("Enemy", make_var("x"), make_const("America")))
#11 America is awesome if at least an American is awesome
add_statement(KB_America, make_atom("Awesome", make_const("America")), make_atom("American", make_var("x")), make_atom("Awesome", make_var("x")))

KB_America = make_unique_var_names(KB_America)

print_KB(KB_America)

# KB 2
# din cursul de IA
KB_Faster = []

def the_greyhound():
    return make_const("Greg")

#0 horses are faster than dogs
add_statement(KB_Faster, make_atom("Faster", make_var("x"), make_var("y")), make_atom("Horse", make_var("x")), make_atom("Dog", make_var("y")))
#1 there is a greyhound that is faster than any rabbit
add_statement(KB_Faster, make_atom("Faster", make_function_call(the_greyhound), make_var("z")), make_atom("Rabbit", make_var("z")))
#2 Harry is a horse
add_statement(KB_Faster, make_atom("Horse", make_const("Harry")))
#3 Ralph is a rabbit
add_statement(KB_Faster, make_atom("Rabbit", make_const("Ralph")))
#4 Greg is a greyhound
add_statement(KB_Faster, make_atom("Greyhound", make_function_call(the_greyhound)))
#5 A greyhound is a dog
add_statement(KB_Faster, make_atom("Dog", make_var("y")), make_atom("Greyhound", make_var("y")))
#6 transitivity
add_statement(KB_Faster, make_atom("Faster", make_var("x"), make_var("z")),
              make_atom("Faster", make_var("x"), make_var("y")), make_atom("Faster", make_var("y"), make_var("z")))

KB_Faster = make_unique_var_names(KB_Faster)

print_KB(KB_Faster)

KB_test = []
add_statement(KB_test, make_atom("Q", make_var("x")), make_atom("P", make_var("x")))
add_statement(KB_test, make_atom("P", make_const("A")))

KB_test = make_unique_var_names(KB_test)
print_KB(KB_test)

"""### Cerința 2

* Implementați funcția `resolves`, care primește două clauze (literali sau disjuncții de literali) și întoarce `False` dacă cele două clauze nu rezolvă, altfel un tuplu care conține literalii care rezolvă, din cele două clauze, și substituția sub care aceștia rezolvă.

* Două clauze rezolvă dacă se găsește un literal pozitiv într-o clauză și un literal negativ în cealaltă, iar atomii celor doi literali unifică.
"""

def is_positive_literal(L):
    return is_atom(L)
def is_negative_literal(L):
    global neg_name
    return get_head(L) == neg_name and is_positive_literal(get_args(L)[0])
def is_literal(L):
    return is_positive_literal(L) or is_negative_literal(L)

def aux_literals(L1, L2):
  if (is_positive_literal(L1) and is_positive_literal(L2)) or (not is_positive_literal(L1) and not is_positive_literal(L2)):
    return False
  if is_positive_literal(L1) and not is_positive_literal(L2):
    return unify(make_neg(L1), L2)
  if not is_positive_literal(L1) and is_positive_literal(L2):
    return unify(L1, make_neg(L2))
  return False


def resolves(C1, C2):
    #print("testing " + print_formula(C1, True) + " and " + print_formula(C2, True))
    #ambii sunt literali => fac unificare
    if is_literal(C1) and is_literal(C2):
      aux = aux_literals(C1, C2)
      if aux != False:
        return (C1,C2,aux)

    #doar unul e literal => ciclez prin literalii celuilalt si incerc sa unific
    if is_literal(C1) and not is_literal(C2):
      for L in get_args(C2):
        aux = aux_literals(C1, L)
        if aux != False:
          return (C1, L, aux)

    if not is_literal(C1) and is_literal(C2):
      for L in get_args(C1):
        aux = aux_literals(L, C2)
        if aux != False:
          return (L, C2, aux)
  
    #niciunul nu e literal => ciclez prin literalii ambilor si incerc sa unific
    if not is_literal(C1) and not(is_literal(C2)):
      for L1 in get_args(C1):
        for L2 in get_args(C2):
          aux = aux_literals(L1, L2)
          if aux != False:
            return (L1, L2, aux)
    # întoarce un tuplu (literal-din-C1, literal-din-C2, substituție)
    # unde literal-din-C1 și literal-din-C2 unifică sub substituție
    return False

# Test!
test_batch(4, globals())

# prints a 5-tuple resolvent representation (see below)
def print_r(R):
    if R is None:
        print("no resolvent")
    else:
        print("resolvent: " + print_formula(R[2], True) + "/" + print_formula(R[3], True) \
              + " {" + ", ".join([(k + ": " + str(R[4][k])) for k in R[4]]) + "}" \
              + "\n\t\t in " + print_formula(R[0], True) + "\n\t\t and " + print_formula(R[1], True))

"""### Cerința 3
* implementați funcția `new_clause`, care întoarce o nouă clauză pe baza unui rezolvent, reprezentat ca un tuplu de 5 elemente:
  * cele 2 clauze care rezolvă;
  * cei 2 literali, unul din prima clauză, și unul din a doua clauză, care rezolvă (dați așa cum sunt ei în cele 2 clauze);
  * substituția sub care rezolvă cei doi literali.
* dacă rezultatul pasului de rezoluție este clauza vidă, funcția trebuie să întoarcă `VOID_CLAUSE`.
* altfel, rezultatul trebuie să fie o clauză care:
  * conține toți literalii din clauzele care au rezolvat, dar
  * nu conține literalii care au rezolvat, și
  * are substituția aplicată (este deja implementată funcția `substitute` în laboratorul 5), și
  * nu conține același literal de mai multe ori.
"""

VOID_CLAUSE = "The void clause"

def new_clause(resolvent):
    new_C=None
    C1, C2, L1, L2, s = resolvent
    
    # TODO
    if is_literal(C1) and is_literal(C2):
      print('a')
      new_C=VOID_CLAUSE
    #doar C2 nu e literal => din C2 scot L2, inlocuiesc argumentele si fac subst
    if is_literal(C1) and not is_literal(C2):
      print('b')
      C2_a=get_args(C2)
      C2_a.remove(L2)
      C2_new=replace_args(C2, C2_a)
      C2_new=substitute(C2_new, s)
      if C2_new[1] == OR:
        args = get_args(C2_new)
      else:
        args = [C2_new]
      if len(args) > 1:
        new_C = make_or(*args)
      elif len(args)==1:
        new_C = args[0]
    #doar C1 nu e literal => din C1 scot L1, inlocuiesc si fac substitutie
    if not is_literal(C1) and is_literal(C2):
      print('c')
      C1_a=get_args(C1)
      C1_a.remove(L1)
      C1_new=replace_args(C1, C1_a)
      C1_new=substitute(C1_new, s)
      if C1_new[1] == OR:
        args = get_args(C1_new)
      else:
        args = [C1_new]
      if len(args) > 1:
        new_C = make_or(*args)
      elif len(args)==1:
        new_C = args[0]
    #ambele sunt compuse => probabil fac la fel, dar concatenez rezultatele 
    if not is_literal(C1) and not is_literal(C2):
      print('d')
      C1_a=get_args(C1)
      C1_a.remove(L1)
      C1_new=replace_args(C1, C1_a)
      C1_new=substitute(C1_new, s)
      
      C2_a=get_args(C2)
      C2_a.remove(L2)
      C2_new=replace_args(C2, C2_a)
      C2_new=substitute(C2_new, s)

      if C1_new[1] == OR:
        args_C1 = get_args(C1_new)
      else:
        args_C1 = [C1_new]

      if C2_new[1] == OR:
        args_C2 = get_args(C2_new)
      else:
        args_C2 = [C2_new]

      args_final = args_C1 + args_C2
      new_C = make_or(*args_final)
    return new_C

# Test!
test_batch(5, globals())

"""### Cerința 4

* implementați partea lipsă din funcția `solve_problem`, utilizând o strategie de rezoluție la alegere pentru a alege două clauze care rezolvă, și adăugând rezultatul pasului de rezoluție la baza de cunoștințe.
"""

def solve_problem(hypotheses, conclusion):
    KB = hypotheses[:]
    KB = [make_neg(conclusion)] + KB # puteți adăuga și la sfârșit (în funcție de strategie)
    Effort = 50 # puteți crește efortul dacă este necesar
    
    while Effort > 0:
        Effort -= 1
      
        # Se aleg două clauze Clauza1 și Clauza2, care nu au mai fost alese anterior
        
        # Se calculează un rezolvent, ca tuplu (Clauza1, Clauza2, Literal-din-clauza1, Literal-din-clauza2, substituție)
        resolvent = None # TODO
        flag = False
        for C1 in KB:
          for C2 in KB:
            flag2 = resolves(C1, C2)
            if flag2 != False:
              flag = True
              (L1, L2, res) = flag2
              resolvent = (C1,C2,L1,L2,res)
          if flag:
            break
        print_r(resolvent)
        if resolvent is None:
            print("Failed. No resolving clauses. Effort left " + str(Effort))
            return False
        
        # Se calculează noua clauză de adăugat și se adaugă la baza de cunoștințe
        
        C = new_clause(resolvent)
        
        if C == VOID_CLAUSE:
            print("Done (effort left " + str(Effort) + ")")
            return True
        
        # update KB
        print("Added: " + print_formula(C, True))
        KB = [C] + KB

        print_KB(KB)
    print("Failed. Effort exhausted.")
                
        
#print_KB(KB_test)
solve_problem(deepcopy(KB_test), make_atom("Q", make_const("A")))
print("==========================================")

#print_KB(KB_America)
# solve_problem(deepcopy(KB_America), make_atom("Criminal", make_const("West")))
print("==========================================")

#print_KB(KB_Faster)
# solve_problem(deepcopy(KB_Faster), make_atom("Faster", make_const("Harry"), make_const("Ralph")))
print("==========================================")
