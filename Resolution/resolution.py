
'''
K(a,b) = a kill b
H(a,b) = a hate b
R(a,b) = a is richer than b

K(A,A) V K(B,A) V K(C,A)
H(A,A) V H(B,A) V H(C,A)
~H(A,x) V ~H(C,x)
H(A,A)
H(A,C)
R(x,A) V H(B,x)
~H(A,x) V H(B,x)
~H(A,A) V ~H(A,B) V ~H(A,C)
~H(B,A) V ~H(B,B) V ~H(B,C)
~H(C,A) V ~H(C,B) V ~H(C,C)
~K(x,A) V ~R(x,A)



smaller test:
K(A,A) V K(B,A) V K(C,A)
~K(A,A)
~K(B,A)
~K(C,A)
'''
class Term:
    def __init__(self, function, element1, element2, isNegated):
        self.function = function
        self.element1 = element1
        self.element2 = element2
        self.isNegated = isNegated
        
    def __eq__(self, __o: object) -> bool:
        return self.function == __o.function and self.element1 == __o.element1 and self.element2 == __o.element2 and self.isNegated == __o.isNegated
        
    def __lt__(self, __o: object) -> bool:
        if self.isNegated != __o.isNegated :
            return self.isNegated
        elif self.function != __o.function :
            return self.function < __o.function
        elif self.element1 != __o.element1 :
            return self.element1 < __o.element1
        else:
            return self.element2 < __o.element2
        
    def __neg__(self) -> 'Term':
        return Term(self.function, self.element1, self.element2, not self.isNegated)
    
    def __str__(self) -> str:
        if self.isNegated:
            return '~{}({},{})'.format(self.function, self.element1, self.element2)
        return '{}({},{})'.format(self.function, self.element1, self.element2)
    
    def __repr__(self) -> str:
        return str(self)
    
    def __hash__(self) -> int:
        return hash(str(self))
    
class Sentence():
    def __init__(self, terms, label, source:tuple) -> None:
        """relation between terms is OR

        Args:
            terms (list[Term]): a list of terms
        """        
        self.terms = terms  # 
        self.label = label
        self.source=source
        
    def __getitem__(self, key):
        return self.terms[key]
    
    def __str__(self) -> str:
        if len(self.terms)==0:
            return "None"
        return ' V '.join(map(str, self.terms))
    
    def __repr__(self) -> str:
        return '{}<-{},{}'.format(self.label,self.source,self.terms)
    
    def __hash__(self) -> int:
        return hash(str((self.terms)))
    
    def append(self,term):
        self.terms.append(term)


class KB:
    # sourceSet=set()
    sentenceSet=set()
    def __init__(self,sentences) -> None:
        """relation between sentences is AND

        Args:
            sentences (list[Sentence]): a list of sentences
        """        
        for sentence in sentences:
            self.sentenceSet.add(str(sentence.terms.sort()))
        self.sentences = sentences
        
    def __getitem__(self, key):
        return self.sentences[key]
    
    def __str__(self) -> str:
        return '\n'.join(map(str, self.sentences))
    
    def __len__(self):
        return len(self.sentences)
    
    def append(self,sentence):
        self.sentences.append(sentence)
        
    def resolution(self):
        
        # traverse all sentences
        i=0
        while True:
            if i >= len(self):
                break
            j=i+1
            while True:
                if j>=len(self):
                    break
                # if self[i].label != self[j].label and (self[i].label,self[j].label) not in self.sourceSet and (self[j].label,self[i].label) not in self.sourceSet:
                # try to resolve s1 and s2
                print('resolve',self[i].label,self[j].label,'len',len(self),'i',i,'j',j)
                terms=[]
                # remove duplicates
                for t1 in self[i].terms:
                    if t1 not in terms:
                        terms.append(t1)
                for t2 in self[j].terms:
                    if t2 not in terms:
                        terms.append(t2)
                        
                for t1 in self[i].terms:
                    for t2 in self[j].terms:
                        if t1==-t2:
                            # delete t1 and t2
                            terms.remove(t1)
                            terms.remove(t2)
                            
                terms.sort()
                
                if len(terms)==0:
                    s=Sentence(terms,'!',(self[i].label,self[j].label))
                    # create a new sentence
                    # self.sourceSet.add(s.source)
                    self.sentenceSet.add(str(s.terms))
                    self.append(s)
                    return True
                else:
                    s=Sentence(terms,'S'+str(len(self)+1),(self[i].label,self[j].label))
                    # check if the terms are all in the KB
                    if str(s.terms) not in self.sentenceSet:
                        # create a new sentence
                        # self.sourceSet.add(s.source)
                        self.sentenceSet.add(str(s.terms))
                        self.append(s)
                j+=1
            i+=1
        return False