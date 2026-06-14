import sys 
import os

counter_dict={}

class Parser:
    def __init__(self,inputfile):
        self.file=open(inputfile,"r")
        self.currLine=""
        self.currInstruction=""
        self.currCommandType=""
        self.token1=""
        self.token2=""
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
        func_commands=["function","call","return"]
        branching=["label","goto","if-goto"]
        if self.currInstruction==None:
            self.currCommandType=None
            return
        instruction=((self.currInstruction.split())[0]).lower()
        for i in arithmetic:
            if i in (instruction):
                self.currCommandType="Arithmetic_Instructions"
                return
         
        for i in memory:
            if i in (instruction):
                self.currCommandType="Memory_Instructions"
                return  
            
        for i in func_commands:
            if i in (instruction):
                self.currCommandType="Function_Instructions"
                return
            
        for i in branching:
            if i in (instruction):
                self.currCommandType="Branching_Instructions"
                return
    
    def arg1(self):
        if self.currCommandType==None:
            return None
        if self.currCommandType=="Arithmetic_Instructions":
            return self.currInstruction.split()[0]
        if self.currCommandType=="Memory_Instructions":
            return self.currInstruction.split()[1]
        if self.currCommandType=="Branching_Instructions":
            return self.currInstruction.split()[1]
        if self.currCommandType=="Function_Instructions":
            if((self.currInstruction.split()[0]).lower()=="return"):
                return None
            return self.currInstruction.split()[1]
        return "Error at arg1()"
    
    def arg2(self):
        if self.currCommandType==None:
            return None
        if self.currCommandType=="Arithmetic_Instructions":
            return None 
        if self.currCommandType=="Memory_Instructions":
            return self.currInstruction.split()[-1]
        if self.currCommandType=="Branching_Instructions":
            return None 
        if self.currCommandType=="Function_Instructions":
            if((self.currInstruction.split()[0]).lower()=="return"):
                return None
            return self.currInstruction.split()[2]
        return "Error at arg2()"

    def fclose(self):
        self.file.close()



class CodeWriter():
    def __init__(self,inputfile,outputfile="",operation_type="a"):
        if outputfile:
            outfile=outputfile
        else:
            outfile=".".join(inputfile.split(".")[0:-1])+".asm"
        self.inputfile=os.path.basename(os.path.normpath(inputfile))

        self.outputfile=open(outfile,operation_type)
        self.relational_label_count=0
        global counter_dict
        self.counter_dict=counter_dict
        self.function_name=""

    
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
            self.relational_label_count+=1
            out=f"""
                @SP
                AM=M-1
                D=M
                A=A-1
                D=M-D
                @LABELA{self.relational_label_count}
                D;JEQ
                @SP
                A=M-1
                M=0
                @LABELB{self.relational_label_count}
                0;JMP
                (LABELA{self.relational_label_count})
                @SP
                A=M-1
                M=-1
                (LABELB{self.relational_label_count})
                
                """
         
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
        elif instruction.lower()=="gt":
            self.relational_label_count+=1
            out=f"""
                @SP
                AM=M-1
                D=M
                A=A-1
                D=M-D
                @LABELA{self.relational_label_count}
                D;JGT
                @SP
                A=M-1
                M=0
                @LABELB{self.relational_label_count}
                0;JMP
                (LABELA{self.relational_label_count})
                @SP
                A=M-1
                M=-1
                (LABELB{self.relational_label_count})
                
                """
            out = "\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
        elif instruction.lower()=="lt":
            self.relational_label_count+=1
            out=f"""
                @SP
                AM=M-1
                D=M
                A=A-1
                D=M-D
                @LABELA{self.relational_label_count}
                D;JLT
                @SP
                A=M-1
                M=0
                @LABELB{self.relational_label_count}
                0;JMP
                (LABELA{self.relational_label_count})
                @SP
                A=M-1
                M=-1
                (LABELB{self.relational_label_count})
                
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

    def writeFunction(self,instruction,currfile=None):
        if(currfile==None):
            currfile=self.inputfile
        instruction=[i.strip() for i in instruction.split()]
        if instruction[0].lower()=="return":
            out='''
            @LCL
            D=M
            @R13
            M=D

            @5
            D=A
            @R13
            A=M-D
            D=M
            @R14
            M=D

            @SP
            A=M-1
            D=M
            @ARG
            A=M
            M=D

            @ARG
            D=M
            @SP
            M=D+1

            @R13
            AM=M-1
            D=M
            @THAT
            M=D

            @R13
            AM=M-1
            D=M
            @THIS
            M=D

            @R13
            AM=M-1
            D=M
            @ARG
            M=D
            
            @R13
            AM=M-1
            D=M
            @LCL
            M=D

            @R14
            A=M
            0;JMP
            '''
            out="\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
            #self.writeBranching("goto R14")


        elif instruction[0].lower()=="function":
            
            arg1=instruction[1]
            self.function_name=arg1
            if len(instruction)<3:
                arg2=0
            else:
                arg2=instruction[2]
            out=f'({self.function_name})\n'              #{currfile}.
            self.outputfile.writelines(out)
            for _ in range(int(arg2)):
                self.writeMemory("push constant 0") 


        elif instruction[0].lower()=="call":
            arg1=instruction[1]
            self.function_name=arg1
            if len(instruction)<3:
                arg2=0
            else:
                arg2=instruction[2]
            if arg1 not in counter_dict:
                counter_dict[arg1]=1
            #(Change New): modified_instruct=f"push constant {self.inputfile}.{arg1}$ret.{counter_dict[arg1]}"
            modified_instruct=f"push constant {arg1}$ret.{counter_dict[arg1]}"          #{currfile}.
            self.writeMemory(modified_instruct)

            #modified_instruct="push local 0"
            out='''
            @LCL
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            '''
            out="\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
            #self.writeMemory(modified_instruct)
            

            #modified_instruct="push argument 0"
            out='''
            @ARG
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            '''
            out="\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)
            #self.writeMemory(modified_instruct)
            
            
            modified_instruct="push pointer 0"
            self.writeMemory(modified_instruct)
            modified_instruct="push pointer 1"
            self.writeMemory(modified_instruct)
            out=f'''
            @SP
            D=M
            @{int(arg2)+5}
            D=D-A
            @ARG
            M=D

            @SP
            D=M
            @LCL
            M=D
            '''

            out="\n".join(line.strip() for line in out.splitlines())
            self.outputfile.writelines(out)

            self.writeBranching(f"goto {arg1}")                             
            
            #(Change New): self.outputfile.writelines(f"({self.inputfile}.{arg1}$ret.{counter_dict[arg1]})\n")
            self.outputfile.writelines(f"({arg1}$ret.{counter_dict[arg1]})\n")           #{currfile}.
            
            counter_dict[arg1]+=1


         
    
    def writeBranching(self,instruction,currfile=None):
        instruction=[i.strip() for i in instruction.split()]
        mystring=instruction[1]
        if currfile==None:
            currfile=self.inputfile
            newstring=f"{mystring}"
        else:
            newstring=f"{currfile}${mystring}"
        
        if instruction[0].lower()=="label":
            out=f"({newstring})\n"
        elif instruction[0].lower()=="goto":
            #(Change New): Below:- from   @{self.inputfile}${mystring}   to   @{mystring}

            #{currfile}$
            out=f'''
            @{newstring}
            0;JMP
            '''
            out="\n".join(line.strip() for line in out.splitlines())
        else:
            out=f'''
            @SP
            AM=M-1
            D=M
            @{newstring}
            D;JNE
            '''
            out="\n".join(line.strip() for line in out.splitlines())

        self.outputfile.writelines(out)


    def fclose(self):
        self.outputfile.close()
            
debug=0
class solver:
    def __init__(self,inputfile,outputfile=""):
        self.inputfile=inputfile
        if outputfile:
            self.outputfile=outputfile
        else:
            self.outputfile=".".join(inputfile.split(".")[0:-1]+["asm"])
    def Bootstrap(self):
        Writer=CodeWriter(self.inputfile,self.outputfile,"w")
        
        out=f'''
        @256
        D=A
        @SP
        M=D
        '''
        #@Sys.vm.Sys.init
        #0;JMP
        
        out="\n".join(line.strip() for line in out.splitlines())
        Writer.outputfile.write(out)
        
        
        Writer.writeFunction("call Sys.init 0","Sys.vm")
        #(Change New): Writer.writeFunction("call Sys.init 0")

        #(Change 5): out=f'''({os.path.basename(os.path.normpath(self.inputfile))}$ret.1)\n'''
        Writer.outputfile.write(out)
        Writer.fclose()
    def solve(self,operation_type="a",currfile=None):
        P=Parser(self.inputfile)
        Writer=CodeWriter(self.inputfile,self.outputfile,operation_type)
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

            elif P.currCommandType=="Branching_Instructions":
                Writer.writeBranching(P.currInstruction,currfile)

            elif P.currCommandType=="Function_Instructions":
                Writer.writeFunction(P.currInstruction,currfile)

            
            #else:
            #    print("--------------------------------")
            if debug:
                print(Writer.outputfile.readlines())
                #print("Reached outside the loop:")
        P.fclose()
        Writer.fclose()





if __name__=="__main__":

    input_given=sys.argv[1]
    
    if os.path.isfile(input_given):
        assert input_given.endswith(".vm")
        counter_dict[sys.argv[1]]=1
        s=solver(sys.argv[1])
        s.solve(operation_type="w")
    
    elif os.path.isdir(input_given):
        start=0
        folder_name = os.path.basename(os.path.normpath(input_given))
        outputfile = os.path.join(input_given, folder_name + ".asm")

        s=solver(input_given,outputfile)
        s.Bootstrap()

        flag=0 # 0 denotes no sys.init 
        
        
        sys_file=os.path.join(input_given,"Sys.vm")
        #(Change 2): sys_file=os.path.join(folder_name,"Sys.vm")
        
        if os.path.exists(sys_file):
            #s=solver(file_fullpath,outputfile)
            s=solver(sys_file,outputfile)
            s.solve()
            flag=1
        


        counter_dict[sys.argv[1]]=1
        for file in os.listdir(input_given):
            if (not file.endswith(".vm")) or file.endswith("Sys.vm"):
                continue
            
            file_fullpath=os.path.join(input_given,file)
            #(Change 2): file_fullpath=os.path.join(folder_name,file)
            
            '''
            (Change 4): 
            '''
            if start==0:
                start+=1
                s=solver(file_fullpath,outputfile)
                if flag:
                    s.solve(currfile=file)
                else:
                    s.solve(operation_type="w",currfile=file)
                continue
            

            s=solver(file_fullpath,outputfile)
            s.solve(currfile=file)
                