
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
~K(A,A)


smaller test:
K(A,x) V K(B,A)
~K(A,A)
~K(B,A)
~K(A,B)
'''
from copy import deepcopy


class Term:
    def __init__(self, function, element1, element2, isNegated):
        self.function = function
        self.element1 = element1
        self.element2 = element2
        self.isNegated = isNegated

    def __eq__(self, __o: object) -> bool:
        return self.function == __o.function and self.element1 == __o.element1 and self.element2 == __o.element2 and self.isNegated == __o.isNegated

    def __lt__(self, __o: object) -> bool:
        if self.isNegated != __o.isNegated:
            return self.isNegated
        elif self.function != __o.function:
            return self.function < __o.function
        elif self.element1 != __o.element1:
            return self.element1 < __o.element1
        else:
            return self.element2 < __o.element2

    def __neg__(self) -> 'Term':
        return Term(self.function, self.element1, self.element2, not self.isNegated)

    def __getitem__(self, index: int) -> object:
        return (self.element1, self.element2)[index]

    def __str__(self) -> str:
        if self.isNegated:
            return '~{}({},{})'.format(self.function, self.element1, self.element2)
        return '{}({},{})'.format(self.function, self.element1, self.element2)

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __setitem__(self, index: int, value: object) -> None:
        if index == 0:
            self.element1 = value
        elif index == 1:
            self.element2 = value
        else:
            raise IndexError('Term Index out of range')

    def isUpper(self) -> bool:
        """check if the term elements is all upper

        Returns:
            bool: true if all upper
        """
        return self.element1.isupper() and self.element2.isupper()


class Sentence():
    def __init__(self, terms, label, source: tuple) -> None:
        """relation between terms is OR

        Args:
            terms (list[Term]): a list of terms
        """
        self.terms = terms
        self.label = label
        self.source = source

    def __getitem__(self, key):
        return self.terms[key]

    def __str__(self) -> str:
        if len(self.terms) == 0:
            return "None"
        return ' V '.join(map(str, self.terms))

    def __repr__(self) -> str:
        return '{}<-{},{}'.format(self.label, self.source, self.terms)

    def __hash__(self) -> int:
        return hash(str((self.terms)))

    def __iter__(self):
        return iter(self.terms)

    def append(self, term):
        self.terms.append(term)


class KB:
    def __init__(self, sentences) -> None:
        """relation between sentences is AND

        Args:
            sentences (list[Sentence]): a list of sentences
        """
        self.constantSet = set()
        self.sentenceSet = set()
        for sentence in sentences:
            self.sentenceSet.add(str(sentence.terms.sort()))
        self.sentences = sentences

    def __getitem__(self, key):
        return self.sentences[key]

    def __str__(self) -> str:
        return '\n'.join(map(str, self.sentences))

    def __len__(self):
        return len(self.sentences)

    def append(self, sentence):
        print('create', sentence.label, str(sentence.terms))
        self.sentenceSet.add(str(sentence.terms))
        self.sentences.append(sentence)

    def unify(self, sentence):
        """unify a sentence by replace variables with constants, and add to KB

        Args:
            sentence (Sentence): the sentence to be unified
        """
        varFlag = []   # False: not a variable, True: a variable
        for term in sentence:
            # mark the variable
            if term[0].islower():
                varFlag.append(True)
            else:
                varFlag.append(False)

            if term[1].islower():
                varFlag.append(True)
            else:
                varFlag.append(False)

        # replace the variable with the constant
        count = 0
        for constant in self.constantSet:
            count += 1

            newSentence = deepcopy(sentence)
            newSentence.label = 'U'+sentence.label[1:]+'-'+str(count)
            newSentence.source = ('Unify', sentence)

            for i in range(len(varFlag)):
                if varFlag[i]:
                    newSentence[i//2][i % 2] = constant

            self.append(newSentence)

    def resolution(self):
        """resolution, call unify for each sentence which has variables

        Returns:
            bool,object: True if the KB can be resolved, False if not.Object is the resolution result, None if the KB is not resolved.
        """
        count = 0

        # traverse all sentences
        i = 0
        while True:
            if i >= len(self):
                break
            hasVariable = False
            for term in self[i]:
                if not term.isUpper():
                    hasVariable = True

            if hasVariable:
                self.unify(self[i])
                i += 1
                continue

            j = i+1
            while True:
                if j >= len(self):
                    break

                count += 1
                if count >= 5000:
                    return False, None

                # try to resolve s1 and s2
                print('resolve', self[i].label, str(
                    self[i]), self[j].label, str(self[j]), 'len', len(self))
                terms = []

                hasVariable = False
                # remove duplicates
                for t1 in self[i].terms:
                    if t1 not in terms:
                        terms.append(t1)
                    if not t1.isUpper():
                        hasVariable = True
                        break
                for t2 in self[j].terms:
                    if t2 not in terms:
                        terms.append(t2)
                    if not t2.isUpper():
                        hasVariable = True
                        break

                if hasVariable:
                    j += 1
                    continue

                delFlag = False   # indicates whether a term deleted
                for t1 in self[i].terms:
                    for t2 in self[j].terms:
                        if t1 == -t2:
                            # delete t1 and t2
                            terms.remove(t1)
                            terms.remove(t2)
                            delFlag = True

                terms.sort()

                if len(terms) == 0:
                    s = Sentence(terms, '!', (self[i], self[j]))

                    # create a new sentence
                    self.append(s)
                    return True, s
                else:
                    if len(terms) >= 5:
                        # too large, thought useless
                        print('too large', terms)
                    else:
                        s = Sentence(terms, 'S'+str(len(self)+1),
                                     (self[i], self[j]))

                        # check if the terms are all in the KB, and if no new terms are created
                        if str(s.terms) not in self.sentenceSet and delFlag:

                            # create a new sentence
                            self.append(s)

                j += 1
            i += 1
        return False, None
