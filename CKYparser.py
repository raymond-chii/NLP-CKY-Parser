def get_grammar(cnfFile):
    grammar = {'nonterminal': {}, 'terminal': {}}
    with open(cnfFile, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                lhs, rhs = line.split(' --> ')
                lhs = lhs.strip()
                rhs = rhs.split()
                if len(rhs) == 1 and rhs[0][0].islower():
                    if lhs not in grammar['terminal']:
                        grammar['terminal'][lhs] = []
                    grammar['terminal'][lhs].append(rhs[0])
                else:
                    if lhs not in grammar['nonterminal']:
                        grammar['nonterminal'][lhs] = []
                    grammar['nonterminal'][lhs].append(rhs)
            
    return grammar

def cky_setup(sentence, grammar):
    words = sentence.split()
    n = len(words)
    mat = []
    for i in range(n):
        mat.append([])
        for j in range(n):
            mat[i].append([])

    for i in range(n):
        word = words[i]
        for lhs, rhsList in grammar['terminal'].items():
            if word in rhsList:
                mat[i][i].append(lhs)

    for span in range(2, n + 1):
        for i in range(n - span + 1): 
            j = i + span - 1  
            for k in range(i, j): 
                for lhs, rhsList in grammar['nonterminal'].items():
                    for rhs in rhsList:
                        if len(rhs) == 2 and rhs[0] in mat[i][k] and rhs[1] in mat[k + 1][j]:
                            mat[i][j].append(lhs)

    return mat

def parse(mat, grammar, i, j, symbol, words):
    if i == j:
        if symbol in mat[i][j]:
            return [[symbol, words[i]]]
        else:
            return []

    parse_trees = []
    for k in range(i, j):
        for rhs in grammar['nonterminal'].get(symbol, []):
            if len(rhs) == 2 and rhs[0] in mat[i][k] and rhs[1] in mat[k + 1][j]:
                leftTrees = parse(mat, grammar, i, k, rhs[0], words)
                rightTrees = parse(mat, grammar, k + 1, j, rhs[1], words)
                for leftTree in leftTrees:
                    for rightTree in rightTrees:
                        parse_trees.append([symbol, leftTree, rightTree])

    return parse_trees

def main():
    cnfFile = input("Enter the path to the CNF grammar file: ")
    grammar = get_grammar(cnfFile)
    print("Loading grammar...")

    displayTrees = input("Do you want textual parse trees to be displayed (y/n)?: ").strip().lower() == 'y'

    while True:
        sentence = input("Enter a sentence (or 'quit' to exit): ")
        if sentence.lower() == 'quit':
            print("Goodbye!")
            break

        words = sentence.split()
        mat = cky_setup(sentence, grammar)
        if not mat[0][-1]:
            print("NO VALID PARSES")
        else:
            parses = parse(mat, grammar, 0, len(words) - 1, 'S', words)
            print("VALID SENTENCE\n")
            print(f"Number of valid parses: {len(parses)}\n")
            for idx, parseTree in enumerate(parses, 1):
                print(f"Valid parse #{idx}:")
                if displayTrees:
                    print(format_parse_tree(parseTree))
                    print_parse_tree(parseTree)
                else:
                    print(format_parse_tree(parseTree))
                print()

def format_parse_tree(tree):
    if isinstance(tree, str):
        return tree
    else:
        formatted = ' '.join(format_parse_tree(subTree) for subTree in tree[1:])
        return f"[{tree[0]} {formatted}]"

def print_parse_tree(tree, level=0):
    indent = ' ' * (level * 2)  
    if isinstance(tree, str):
        print(indent + tree)
    else:
        if len(tree) == 2 and isinstance(tree[1], str):  
            print(f"{indent}[{tree[0]} {tree[1]}]")  
        else:
            print(indent + '[' + tree[0]) 
            for subTree in tree[1:]:
                print_parse_tree(subTree, level + 1)
            print(indent + ']')


if __name__ == "__main__":
    main()


