class flowerLang:
  cLineIdx:int=0 # current line index
  cResultL:list=[] # resulting python code lines
  loader:list=[]
  runner:list=[]
  fun:list=[]
  funIndent:int=0
  returnVar:str=""
  rConst:str=""
  rConst0:str=""
  isOpsControlled:int=0
  isHeader:bool=False
  isTail:bool=False
  def __init__(self):
    return None
  def initPilerInst(self):
    self.loader=[]
    self.runner=[]
    self.fun=[]
    self.funIndent=0
    #self.isHeader=False
    #self.isTail=False
    #self.isOpsControlled=0
    return 0
  def regInput(self,code:list=[]): # register the code to process
    self.code:list=code
    return 0
  def strInput(self,si:str=""): # convert the code
    self.code:list=si.splitlines()
    return 0
  def cln(self):
    return self.code[self.cLineIdx]
  def Token(self,obj:str="",delim:str=" "):
    esc:int=0
    idxThr:int=0
    output:list=[]
    #if obj=="": obj=self.head
    for idx in range(len(obj)):
      i=obj[idx]
      #print("char:",i)
      if i in ['"',"'"]:
        esc=1-esc
        #if esc==1: print("eval off")
        #if esc==0: print("eval on")
      if esc==0 and i==delim and not(obj[idx-1:idx+1] in [", ","  ","   "]):
        output.append(obj[idxThr:idx])
        idxThr=idx+1
        #print("saved")
    if idxThr<len(obj):
      output.append(obj[idxThr:idx+1])
    return output
  def HeadHunter(self):
    self.head:str=""
    self.headL:list=[]
    find:int=1
    while find:
      if (self.cln().lstrip()[0:1]=="(") and (")" in self.cln()):
        if self.cln().index(")")>0:
          for i in self.cln():
            if i==" ":
              self.funIndent+=1
            else:
              break
            #print("indent:",self.funIndent)
          self.head=self.cln().lstrip()
          self.headL=self.Token(self.head)
          self.returnVar=""
          #sanitize headL
          for i in range(len(self.headL)):
            self.headL[i]=self.headL[i].strip()
            #self.initPilerInst()
          find=0
          if (self.headL[-1]=="{") and (len(self.fun)>0):
            self.initPilerInst()
          self.isHeader=True
          self.isTail=False
          self.isOpsControlled=0
      else:
        if self.cln()[0:1]=="}":
          for i in self.loader:
            self.cResultL.append(i)
          #self.cResultL.append(self.rConst)
          for i in self.runner:
            self.cResultL.append(f"  {i}")
          self.cResultL.append(self.rConst0)
          self.initPilerInst()
          self.isHeader=False
          self.isTail=True
          self.isOpsControlled=0
        elif self.cln()[0:2+self.funIndent]==" "*(self.funIndent)+"<<":
          self.funIndent=0
          self.returnVar=self.Token(self.cln(),"<")[-1].strip()
          if self.returnVar!="":
            self.runner[-1]=f"{self.returnVar}={self.runner[-1]}"
          #for i in range(len(self.runner)):
          #  self.runner[i]=f" {self.runner[i]}"
          #for i in self.loader:
          #  self.cResultL.append(i)
          #self.cResultL.append(self.rConst)
          self.loader.append(self.rConst)
          self.isHeader=False
          self.isTail=True
          self.isOpsControlled=0
        else:
          vstr=self.cln()
          #print(self.isHeader,self.isTail)
          #print(vstr)
          if (self.isHeader==True) and (self.isTail==False):
          #print(self.cln())
            #self.loader[-1]=(" "*self.isOpsControlled)+self.loader[-1]
            self.loader.append((" "*self.isOpsControlled)+vstr)
            #self.loader.append(str(self.funIndent)+" "+str(self.isOpsControlled))
            #self.loader.append(f".{' '*self.isOpsControlled}.")
          #print(self.runner)
        #print("next line:",self.cLineIdx)
        self.cLineIdx+=1
    return 0
  def HeadPiler(self):
    #print(self.headL)
    #extract arguments
    head1:str=self.Token(self.headL[0],")")[0]
    head2:str=self.Token(self.headL[0],")")[1]
    #print(self.Token(self.headL[0],")"))
    head1=head1[1:]
    self.args=head1
    self.argv=self.Token(head1,",")
    self.argc=len(self.argv)
    self.funName=head2
    self.fun.append(head2)
    #sanitize argv
    for i in range(len(self.argv)):
      self.argv[i]=self.argv[i].strip()
    #print(self.fun,self.funName, self.args, self.argv, self.argc)
    return 0
  def BuildFun(self):
    self.funDec=" "*self.funIndent+f"def {self.funName}({self.args}):"
    self.funVar=f"{self.funName}({self.args})"
    if len(self.fun)>1:
      self.loader.append(self.funDec)
      self.runner.append(self.funVar)
    else:
      self.cResultL.append(self.funDec)
    #print(self.funDec)
    #print(self.loader)
  def r2v(self): # return to value
    #print(self.headL)
    if len(self.headL)>2:
      if self.headL[2]==">>":
          self.rConst=" "*self.funIndent+f"  return {self.headL[1]}({self.headL[3]})"
      if self.headL[1]==">>":
        self.rConst=" "*self.funIndent+f"  return {self.headL[2]}"
    if len(self.headL)>4:
      if self.headL[4]==">>":
          self.rConst=" "*self.funIndent+f"  return {self.headL[1]}({self.headL[5]})"
      if self.headL[3]==">>":
          self.rConst=" "*self.funIndent+f"  return {self.headL[4]}"
    if len(self.headL)<=2:
      self.rConst=""
      #print(self.rConst)
    if self.headL[-1]=="{":
      self.rConst0=f"{self.rConst}"
  def conFlow(self):
    if "<>" in self.headL:
      ops=self.headL.index("<>")
      self.isOpsControlled=4
      #print(self.headL)
      if ops in [1,2]:
        self.loader.append(" "*(self.funIndent)+f"  if {self.headL[ops+1]}:")
    if "><" in self.headL:
      ops=self.headL.index("><")
      self.isOpsControlled=4
      #print(self.headL)
      if ops in [1,2]:
        self.loader.append(" "*(self.funIndent)+f"  if not{self.headL[ops+1]}:")
    if "<<" in self.headL:
      ops=self.headL.index("<<")
      self.isOpsControlled=4
      #print(self.headL)
      if ops in [1,2]:
        self.loader.append(" "*(self.funIndent)+f"  while {self.headL[ops+1]}:")


# flower 0.7 transpiler
c=flowerLang()
code='''
# the simplest hello world in flower 0.7
()main {
  ()f
    print("Hello, world!")
  <<
}

# flow control examples
()flow >> 0 {
  (a=0)conditional <> (a==0) >> a
    print("Hello, world!",f"a = {a}")
  << example1

  (a=1)conditional_v >< (a==0) >> a
    print("Hello, world! a =",a)
  << example2

  (i=0)loop << (i<=5) >> i
    i+=1
    print(i)
  << example3

# variable flow example
()var {
  ()a str >> "Hello, world!"
  << a
  (a)f0 len >> a
  << l
  (l)f1 int >> l
  <<
}

()var2 {
  ()a >> a
    a="Hello, world!"
  << a

  (a)f0 >> l
    l=len(a)
  << l

  (l)f1 >> l
    l=int(l)
  <<

()end
'''
import sys
file=open(sys.argv[0],'r')
c.strInput(code)
#print(c.code)
for i in range(int(sys.argv[1])):
  c.HeadHunter()
  c.HeadPiler()
  c.BuildFun()
  c.conFlow()
  c.r2v()
  c.cLineIdx+=1
print('\n'.join(c.cResultL[:-1]))
print("main()")
