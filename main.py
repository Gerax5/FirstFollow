import os
from typing import List, Union
from first import First
from follow import Follow

def processProd(prod: str) -> List[str]:
    tokens = []
    i = 0
    while i < len(prod):

        if prod[i].islower():
            buffer = prod[i]
            i += 1
            while i < len(prod) and prod[i].islower():
                buffer += prod[i]
                i += 1
            tokens.append(buffer)

        elif prod[i].isupper():
            buffer = prod[i]
            i += 1

            while i < len(prod) and prod[i] == "'":
                buffer += prod[i]
                i += 1
            tokens.append(buffer)
        elif prod[i] == "'":

            tokens.append("'")
            i += 1
        else:
            tokens.append(prod[i])
            i += 1
    return tokens

def leerArchivo(file: str) -> Union[List[str], str]:
    transitions = {}
    inital_simbol = ""
    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, file)

        with open(file_path, "r", encoding="utf-8") as f:
            expresiones = f.read().split("\n")
            for expr in expresiones:
                production = expr.split("->")
                if inital_simbol == "":
                    inital_simbol = production[0].strip()
                transitions[production[0].strip()] = [x.strip() for x in production[1].split("|")]

            for key, value in transitions.items():
                prod = []
                for p in value:
                    prod.append(processProd(p))
                transitions[key] = prod

        print("Producciones: ", transitions)

        return inital_simbol, transitions
    except FileNotFoundError:
        return "El archivo no fue encontrado"
    except IOError:
        return "Error al leer el archivo"
    


inital_simbol, grammar = leerArchivo("cfg.txt")

first = First(grammar)
follow = Follow(grammar, first.first , inital_simbol)

print("\nFisrt:")
for non_terminal in sorted(first.first.keys()):
    print(f"First({non_terminal}) = {{ {', '.join(sorted(first.first[non_terminal]))} }}")

print("\nFollow:")
for non_terminal in sorted(follow.follow_set.keys()):
    print(f"Follow({non_terminal}) = {{ {', '.join(sorted(follow.follow_set[non_terminal]))} }}")