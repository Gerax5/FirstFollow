class First:
    SPECIAL_CHARACTERS = ['$', '(', ')', '[', ']', '{', '}', '|', '*', '+', '?', '.',"-","/"]

    def __init__(self, grammar: dict):
        self.grammar = grammar
        self.first = {}
        for key in grammar:
            self.calculate_first(key)

    def calculate_first(self, character: str):
        
        if character in self.first:
            return self.first[character]
        
        if character.islower() or character in self.SPECIAL_CHARACTERS:
            return character
        
        for prod in self.grammar[character]:
            
            self.first[character] = self.first.get(character, set())
            i = 0
            while i < len(prod):
                cur_char: str = prod[i]

                if cur_char in self.SPECIAL_CHARACTERS or cur_char.islower():
                    self.first[character].add(prod[i])
                    break

                self.first[character].update(self.calculate_first(cur_char))

                if "ε" not in self.first[character]:
                    break

                i += 1
        
        return self.first[character]
