

class Term:
    def __init__(self, function, element1, element2, isNegated):
        self.function = function
        self.element1 = element1
        self.element2 = element2
        self.isNegated = isNegated
        
    def __str__(self) -> str:
        if self.isNegated:
            return '!{}({}, {})'.format(self.function, self.element1, self.element2)
        return '{}({}, {})'.format(self.function, self.element1, self.element2)

class Sentence():
    def __init__(self, terms) -> None:
        """relation between terms is OR

        Args:
            terms (list[Term]): a list of terms
        """        
        self.terms = terms  # 
        
    def __getitem__(self, key):
        return self.terms[key]
    
    def __str__(self) -> str:
        return ' OR '.join(map(str, self.terms))
    
    def append(self,term):
        self.terms.append(term)


class KB:
    def __init__(self,sentences) -> None:
        """relation between sentences is AND

        Args:
            sentences (list[Sentence]): a list of sentences
        """        
        
        self.sentences = sentences
        
    def __getitem__(self, key):
        return self.sentences[key]
    
    def __str__(self) -> str:
        return '\n'.join(map(str, self.sentences))
    
    def append(self,sentence):
        self.sentences.append(sentence)
        
    