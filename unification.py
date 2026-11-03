import re
def parse_term(tokens, pos):
    name = tokens[pos]
    pos += 1
    if pos < len(tokens) and tokens[pos] == '(':
        pos += 1
        args = []
        while pos < len(tokens) and tokens[pos] != ')':
            term, pos = parse_term(tokens, pos)
            args.append(term)
            if pos < len(tokens) and tokens[pos] == ',':
                pos += 1
        pos += 1
        return ('func', name, args), pos
    if name[0].islower():
        return ('var', name), pos
    return ('const', name), pos
def parse_predicate(expression):
    tokens = re.findall(r'[A-Za-z_]\w*|[(),]', expression.replace(' ', ''))
    name = tokens[0]
    pos = 2
    args = []
    while pos < len(tokens) and tokens[pos] != ')':
        term, pos = parse_term(tokens, pos)
        args.append(term)

        if pos < len(tokens) and tokens[pos] == ',':
            pos += 1
    return name, args
def apply_substitution(term, subst):
    if term[0] == 'var':
        name = term[1]
        if name in subst:
            return apply_substitution(subst[name], subst)
        return term
    if term[0] == 'func':
        return ('func', term[1],
                [apply_substitution(t, subst) for t in term[2]])
    return term
def occurs(variable, term, subst):
    term = apply_substitution(term, subst)
    if term[0] == 'var':
        return term[1] == variable
    if term[0] == 'func':
        return any(occurs(variable, t, subst) for t in term[2])
    return False
def unify_terms(t1, t2, subst):
    t1 = apply_substitution(t1, subst)
    t2 = apply_substitution(t2, subst)
    if t1 == t2:
        return True
    if t1[0] == 'var':
        if occurs(t1[1], t2, subst):
            return False
        subst[t1[1]] = t2
        return True
    if t2[0] == 'var':
        if occurs(t2[1], t1, subst):
            return False
        subst[t2[1]] = t1
        return True
    if t1[0] == 'const' and t2[0] == 'const':
        return t1[1] == t2[1]
    if t1[0] == 'func' and t2[0] == 'func':
        if t1[1] != t2[1] or len(t1[2]) != len(t2[2]):
            return False
        for a, b in zip(t1[2], t2[2]):
            if not unify_terms(a, b, subst):
                return False
        return True
    return False
def display(term):
    if term[0] in ('var', 'const'):
        return term[1]
    return term[1] + '(' + ', '.join(display(t) for t in term[2]) + ')'
def unify(p1, p2):
    if p1[0] != p2[0]:
        return None
    if len(p1[1]) != len(p2[1]):
        return None
    subst = {}
    for a, b in zip(p1[1], p2[1]):
        if not unify_terms(a, b, subst):
            return None
    return subst
print("FIRST ORDER LOGIC - UNIFICATION")
p1 = input("Enter first predicate: ")
p2 = input("Enter second predicate: ")
try:
    predicate1 = parse_predicate(p1)
    predicate2 = parse_predicate(p2)
    result = unify(predicate1, predicate2)
    if result is None:
        print("\nUnification Failed!")
    else:
        print("\nUnification Successful!")

        if result:
            print("Most General Unifier (MGU):")
            for variable, value in result.items():
                print(variable, "->", display(
                    apply_substitution(value, result)))
        else:
            print("No substitution required (MGU = {}).")
except (IndexError, ValueError):
    print("Invalid predicate format!")
