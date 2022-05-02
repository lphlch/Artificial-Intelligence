from copy import deepcopy


class a:
    def __init__(self,x) -> None:
        self.x=x
        
    def test(self):
        for i in self.x:
            for j in self.x:
                print('test',i,j)
                if i!=j and i+j < 5 and i+j not in self.x:
                    self.append(i+j)
                
    def append(self,y):
        self.x.append(y)

    
a1=a([1,2,3])
a2=a([1,2,4])
# t=a1.x+a2.x
# # t=deepcopy(a1.x)+deepcopy(a2.x)
# t[3]=1999
# print(a1.x,a2.x,t)
a.test(a1)