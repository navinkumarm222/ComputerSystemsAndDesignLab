import sys 

class Parser:
    def __init__(self,inputfile):
        self.file=open(inputfile,"r")
        self.currLine=""
        self.currInstruction=""
        self.currCommandType=""
        
    def clean(self):
        pass
    def hasMoreLines(self):
        self.currLine=self.file.readline()
        if self.currLine:
            return True 
        return False
    
    def advance(self):
        if not(self.currLine.strip()):
            self.currInstruction=None 
            return
        self.currInstruction=self.currLine.strip()
        dash=self.currInstruction.find("//")
        if dash>0:
            self.currInstruction=self.currInstruction[:dash]
        elif dash==0:
            self.currInstruction=None
        else:
            self.currInstruction=self.currInstruction

    def commandType(self):
        arithmetic=["add",'sub',"neg",'eq','gt','lt','not','and','or']
        memory=["pop","push"]
        if self.currInstruction==None:
            self.currCommandType=None
            return
        for i in arithmetic:
            if i in ((self.currInstruction.split())[0]).lower():
                self.currCommandType="Arithmetic_Instructions"
                return
         
        for i in memory:
            if i in ((self.currInstruction.split())[0]).lower():
                self.currCommandType="Memory_Instructions"
                return  
    
    def arg1(self):
        if self.currCommandType==None:
            return None
        if self.currCommandType=="Arithmetic_Instructions":
            return self.currInstruction.split()[0]
        if self.currCommandType=="Memory_Instructions":
            return self.currInstruction.split()[1]
        return "Error at arg1()"
    
    def arg2(self):
        if self.currCommandType==None:
            return None
        if self.currCommandType=="Arithmetic_Instructions":
            return None 
        if self.currCommandType=="Memory_Instructions":
            return self.currInstruction.split()[-1]
        return "Error at arg2()"

    def fclose(self):
        self.file.close()



class CodeWriter():
    def __init__(self,inputfile):
        outfile=".".join(inputfile.split(".")[0:-1])+".asm"
        self.inputfile=inputfile
        self.outputfile=open(outfile,"w+")
        self.relational_count=0

    
    def writeArithmetic(self,instruction):
        if instruction.lower()=='add':
            out='''
                @SP
                A=M-1
                D=M
                A=A-1
                M=D+M
                @SP
                M=M-1
                '''
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
        elif instruction.lower()=="sub":
            out='''
                @SP
                A=M-1
                D=M
                A=A-1
                M=M-D
                @SP
                M=M-1
                '''
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
        elif instruction.lower()=="neg":
            out='''
                @SP
                A=M-1
                M=-M
                '''
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)


        elif instruction.lower()=="not":
            out='''
                @SP
                A=M-1
                M=!M
                '''
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
        elif instruction.lower()=="and":
            out='''
                @SP
                A=M-1
                D=M
                A=A-1
                M=D&M
                @SP
                M=M-1
                '''
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
        elif instruction.lower()=="or":
            out='''
                @SP
                A=M-1
                D=M
                A=A-1
                M=D|M
                @SP
                M=M-1
                '''
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
        


        elif instruction.lower()=="eq":
            self.relational_count+=1
            out=f"""
                @SP
                AM=M-1
                D=M
                A=A-1
                D=M-D
                @LABELA{self.relational_count}
                D;JEQ
                @SP
                A=M-1
                M=0
                @LABELB{self.relational_count}
                0;JMP
                (LABELA{self.relational_count})
                @SP
                A=M-1
                M=-1
                (LABELB{self.relational_count})
                
                """
         
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
        elif instruction.lower()=="gt":
            self.relational_count+=1
            out=f"""
                @SP
                AM=M-1
                D=M
                A=A-1
                D=M-D
                @LABELA{self.relational_count}
                D;JGT
                @SP
                A=M-1
                M=0
                @LABELB{self.relational_count}
                0;JMP
                (LABELA{self.relational_count})
                @SP
                A=M-1
                M=-1
                (LABELB{self.relational_count})
                
                """
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
        elif instruction.lower()=="lt":
            self.relational_count+=1
            out=f"""
                @SP
                AM=M-1
                D=M
                A=A-1
                D=M-D
                @LABELA{self.relational_count}
                D;JLT
                @SP
                A=M-1
                M=0
                @LABELB{self.relational_count}
                0;JMP
                (LABELA{self.relational_count})
                @SP
                A=M-1
                M=-1
                (LABELB{self.relational_count})
                
                """
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
    
    def writeMemory(self,instruction):
        #P=Parser(self.inputfile)
        arg1=instruction.split()[1].lower()
        arg2=instruction.split()[2]
        #print('arg1:',arg1)
        #print('arg2:',arg2)

        if "push" in instruction.lower():
            mydict={'argument':"ARG",'local':"LCL",'this':"THIS",'that':"THAT"}
            if arg1.lower() in mydict:
                out=f'''
                    @{mydict[arg1.lower()]}
                    D=M
                    @{arg2}
                    A=D+A
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    '''
                out = "\n".join(line.strip() for line in out.splitlines())
                self.outputfile.writelines(out)

            elif arg1.lower()=='temp':
                out=f'''
                    @5
                    D=A
                    @{arg2}
                    A=D+A
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    '''
                out = "\n".join(line.strip() for line in out.splitlines())
                self.outputfile.writelines(out)
            
            elif arg1.lower()=='pointer' and arg2=="0":
                out=f'''
                    @3
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    '''
                out = "\n".join(line.strip() for line in out.splitlines())
                self.outputfile.writelines(out)
            elif arg1.lower()=='pointer' and arg2=="1":
                out=f'''
                    @4
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    '''
                out = "\n".join(line.strip() for line in out.splitlines())
                self.outputfile.writelines(out)
            elif arg1.lower()=='constant':
                out=f'''
                    @{arg2}
                    D=A
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    '''
                out = "\n".join(line.strip() for line in out.splitlines())
                self.outputfile.writelines(out)
            elif arg1.lower()=='static':
                out=f'''
                    @{self.inputfile}.{arg2}
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    '''
                out = "\n".join(line.strip() for line in out.splitlines())
                self.outputfile.writelines(out)
        elif "pop" in instruction.lower():
            mydict={'argument':"ARG","local":"LCL","this":"THIS","that":"THAT"}
            if arg1 in mydict:
                out=f'''
                @{mydict[arg1]}
                D=M
                @{arg2}
                D=D+A
                @R13
                M=D
                @SP
                AM=M-1
                D=M
                @R13
                A=M
                M=D
                '''

            if arg1=="temp":
                out=f'''
                @5
                D=A
                @{arg2}
                D=D+A
                @R13
                M=D
                @SP
                AM=M-1
                D=M
                @R13
                A=M
                M=D
                '''

            elif arg1=="static":
                out=f'''
                @SP
                AM=M-1
                D=M
                @{self.inputfile}.{arg2}
                M=D
                '''
            elif arg1=="pointer" and arg2=="0":
                out=f'''
                @SP
                AM=M-1
                D=M
                @THIS
                M=D
                '''
            elif arg1=="pointer" and arg2=="1":
                out=f'''
                @SP
                AM=M-1
                D=M
                @THAT
                M=D
                '''

            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
    def fclose(self):
        self.outputfile.close()
            
debug=0
class solver:
    def __init__(self,inputfile):
        self.inputfile=inputfile
    def solve(self):
        P=Parser(self.inputfile)
        Writer=CodeWriter(self.inputfile)
        while P.hasMoreLines():
            
            P.advance()
            P.commandType()
            if debug:
                print("Reached inside the loop:",P.currCommandType)
                print("P.currLine",P.currLine.strip())
                print('P.currInstruction',P.currInstruction)

            if P.currCommandType=="Arithmetic_Instructions":
                Writer.writeArithmetic(P.currInstruction.strip())
                if debug:
                    print(P.currInstruction)
                    print("Arithmetic        !!!!!!!!!!!!!!!!!!!!!!!!!!")
            elif P.currCommandType=="Memory_Instructions":
                Writer.writeMemory(P.currInstruction)
            #else:
            #    print("--------------------------------")
            if debug:
                print(Writer.outputfile.readlines())
                #print("Reached outside the loop:")
        P.fclose()
        Writer.fclose()
        

if __name__=="__main__":
    assert sys.argv[1].endswith(".vm")
    s=solver(sys.argv[1])
    s.solve()
