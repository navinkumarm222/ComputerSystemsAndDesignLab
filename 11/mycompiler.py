from tokenizer import Tokenizer,Token
from collections import defaultdict
import os,sys

debug=1

printAllTokens= 0#True

printSymbolTable=0

printLocation=0




class Compiler:

    
    def __init__(self,file_path):
        self.file_name=os.path.basename(os.path.normpath(file_path))
        self.file_path=file_path

        self.output_code=defaultdict(list)
        
        self.token_iter=0
        t=Tokenizer.tokenize(file_path)
        self.plain_tokens=t[0]
        self.xml_tokens=t[1]
        self.count_of_tokens=len(t[0])

        self.classSymbolTable=dict()             
        # Format:
        # data_name:{"data_name":___ ,"data_type":___ ,"data_kind":___ ,"data_idx":___ }

        self.class_var_count=dict.fromkeys(["static","field","total"],0)


        self.subroutine_names=[]
        self.subroutines_table=dict()               
        # Format:
        # subroutine_name:{variables : [........
        #                       {data_name : 
        #                                   {"name":___ ,"type":___ ,"kind":___ ,"idx":___ } 
        #                                                                                                        }
        #                                                                                                           ..........]   ,
        #                  subroutine_var_count : {local: ____ , argument:____ , total : ____}  ,
        #                   subroutine_ret_type : ____  ,
        #                   subroutine_kind : _____  (constructor,method or function)
        #                                                       }

        self.labelnum=0                 # For compileIfStatement() ......


    def debug_print(self,n=15):
        print("*"*60)
        print()
        print("token_iter   token[lexicon]    [data]")
        for i in range(max(0,self.token_iter-n),min(len(self.plain_tokens),self.token_iter+n)):
            
            if(i==self.token_iter):
                print("-"*45)
                print("--",i,self.plain_tokens[i].lexicon,self.plain_tokens[i].data,"--",sep="\t")
                print("-"*45)
                continue
            print(i,self.plain_tokens[i].lexicon,self.plain_tokens[i].data,sep="\t")

        print("*"*60)
        print()
    

    def debug_printClassSymbolTable(self):
        print("\n"+"_"*60+"\n")
        print("***** ",self.className," class Symbol Table *****")
        print("\n"+"_"*60+"\n")
        for i in self.classSymbolTable:
            print(f"{i} : ","\t",self.classSymbolTable[i])

    def debug_printSubroutineSymbolTable(self):
        count=0
        for name in self.subroutine_names:
            count+=1
            #print("\n"+"_"*60+"\n")
            print(f"\t({count}) ***** Subroutine  [",name,"]  class Symbol Table *****")
            #print("\n"+"_"*60+"\n")
            for i in self.subroutines_table[name]["variables"]:
                print("\t"*2,i)
            print()




    def compileClass(self):

        print("*"*60+"\n")
        print(f"Started compiling {self.file_name}")
        print()

        token_list=self.plain_tokens
        token_iter=self.token_iter

        curr_token=token_list[token_iter]
        if not curr_token.data =="class":
            return
        token_iter+=1

        curr_token=token_list[token_iter]
        if not curr_token.lexicon=="identifier":
            return
        self.className=curr_token.data
        token_iter+=1

        assert self.file_name.split(".")[0]==self.className            # Check whether class_name matches with the file_name
  
        curr_token=token_list[token_iter]
        if not (curr_token.lexicon=="symbol" and curr_token.data=="{"):
            return
        token_iter+=1


        self.token_iter=token_iter
        self.compileClassVarDec()
        self.compileSubroutineDec()
        token_iter=self.token_iter

        curr_token=token_list[token_iter]
        if not (curr_token.lexicon=="symbol" and curr_token.data=="}"):
            raise ValueError("symbol } is missing during compileClass() !")
        token_iter+=1
        self.token_iter=token_iter

        print("Completed Compileclass() !!!!!!!!!!!!!\n")

    def compileClassVarDec(self):
        if (printLocation):
            print("\nNow Inside CompileClassVarDec() !!!!!!!!!!!!!")

        while(True):
            curr_token=self.plain_tokens[self.token_iter]

            # kind
            if(curr_token.lexicon=="keyword" and (curr_token.data=="static" or curr_token.data=="field")):
                data_kind=curr_token.data

                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]
                
                # type
                assert (curr_token.lexicon=="identifier" or (curr_token.lexicon=="keyword" and curr_token.data in ["int","char","boolean"]))
                data_type = curr_token.data

                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]

                #  var_name
                assert (curr_token.lexicon=="identifier")
                data_name=curr_token.data


                # Filling the class_Symbol_Table
                self.classSymbolTable[data_name]={"data_name":data_name,"data_type":data_type,"data_kind":data_kind,"data_idx":self.class_var_count[data_kind]}
                self.class_var_count[data_kind]+=1
                self.class_var_count["total"]+=1


                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]


                # Check for comma(,) --- Additional variables
                while(curr_token.lexicon=="symbol" and curr_token.data==","):
                    self.token_iter+=1
                    curr_token=self.plain_tokens[self.token_iter]

                    assert curr_token.lexicon=="identifier"                    
                    data_name=curr_token.data
                    self.classSymbolTable[data_name]={"data_name":data_name,"data_type":data_type,"data_kind":data_kind,"data_idx":self.class_var_count[data_kind]}
                    self.class_var_count[data_kind]+=1
                    self.class_var_count["total"]+=1

                    self.token_iter+=1
                    curr_token=self.plain_tokens[self.token_iter]


                if(curr_token.lexicon=="symbol" and curr_token.data==";"):
                    self.token_iter+=1
                    continue

                raise ValueError("symbol ; is missing during compileClassVarDec() !!!")


            else:
                break 
        
        #if( printSymbolTable and self.classSymbolTable):
            #self.debug_printClassSymbolTable()
            #self.debug_printSubroutineSymbolTable()
        return 
            
    


    def compileSubroutineDec(self):
        if printLocation:
            print("\nInside CompileSubroutineDec() !!!!!!!!!!!!!")
        
        while(True):
            curr_token=self.plain_tokens[self.token_iter]

            # kind
            if(curr_token.lexicon=="keyword" and curr_token.data in ["constructor","method","function"]):
                subroutine_kind=curr_token.data

                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]

                # return_type
                assert (curr_token.lexicon=="identifier" or (curr_token.lexicon=="keyword" and curr_token.data in ["int","char","boolean","void"]))
                subroutine_return_type = curr_token.data

                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]

                #  subroutine_name
                assert (curr_token.lexicon=="identifier")
                subroutine_name=curr_token.data

                # Initialising the subroutine_Symbol_Table
                self.subroutines_table[subroutine_name]=\
                {"variables":[],
                 "subroutine_var_count":{"local":0,"argument":0,"total":0},
                 "subroutine_ret_type": subroutine_return_type,
                 "subroutine_kind":subroutine_kind}
                
                # Initialising the subroutine_names
                self.subroutine_names.append(subroutine_name)



                if subroutine_kind=="method":
                    self.subroutines_table[subroutine_name]["variables"].append( {"this":{"name":"this","type":subroutine_name,"kind" : "argument", "idx":0}})
                    self.subroutines_table[subroutine_name]["subroutine_var_count"]["argument"]+=1
                    self.subroutines_table[subroutine_name]["subroutine_var_count"]["total"]+=1

                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]

                assert curr_token.lexicon=="symbol" and curr_token.data=="("

                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]

                self.compileParameterList(subroutine_name)

                curr_token=self.plain_tokens[self.token_iter]
                assert curr_token.lexicon=="symbol" and curr_token.data==")"

                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]

                self.compileSubroutineBody(subroutine_name)

                curr_token=self.plain_tokens[self.token_iter]
                assert curr_token.data=="}"

                self.token_iter+=1


            else:
                return 
        

    def compileParameterList(self,subroutine_name):
        if printLocation:
            print("\nInside CompileParameterList() !!!!!!!!!!!!!")

        while(True):
            curr_token=self.plain_tokens[self.token_iter]
            if(curr_token.data==")"):
                return
            
            if(curr_token.lexicon=="keyword" and curr_token.data in ["int","char","boolean"]) or curr_token.lexicon=="identifier":
                curr_argument_type=curr_token.data
            
            self.token_iter+=1
            curr_token=self.plain_tokens[self.token_iter]

            if curr_token.lexicon!="identifier":
                print("curr_token :",curr_token.lexicon,curr_token.data)
                raise ValueError("Not an identifier (code 432) !!! ")    
            
            
            curr_argument_name=curr_token.data

            '''
            if debug:
                print()
                print(self.subroutines_table)
                print("subroutine_name :",subroutine_name)
                print("curr_argument_name :",curr_argument_name)
                print()
            '''
            
            self.subroutines_table[subroutine_name]["variables"].append({curr_argument_name:{"name":curr_argument_name,"type":curr_argument_type,"kind" : "argument", "idx":self.subroutines_table[subroutine_name]["subroutine_var_count"]["argument"]}})
            self.subroutines_table[subroutine_name]["subroutine_var_count"]["argument"]+=1
            self.subroutines_table[subroutine_name]["subroutine_var_count"]["total"]+=1

            self.token_iter+=1
            curr_token=self.plain_tokens[self.token_iter]

            if(curr_token.data==","):
                self.token_iter+=1
                continue
            
            


    def compileSubroutineBody(self,subroutine_name):
        if printLocation:
            print("\nInside CompileSubroutineBody() !!!!!!!!!!!!!")

        curr_token=self.plain_tokens[self.token_iter]
        assert (curr_token.lexicon=="symbol" and curr_token.data=="{")

        self.token_iter+=1
        curr_token=self.plain_tokens[self.token_iter]

        self.compileVarDec(subroutine_name)

        self.output_code[subroutine_name].append(f"function {self.className}.{subroutine_name} {self.subroutines_table[subroutine_name]["subroutine_var_count"]["local"]}")             

        subroutine_type=self.subroutines_table[subroutine_name]["subroutine_kind"]
        if(subroutine_type=="constructor"):
            #self.output_code[subroutine_name].append(f"function {self.className}.{subroutine_name} {self.class_var_count["field"]}")                                                        # New change -2         
            self.output_code[subroutine_name].extend([f"push constant {self.class_var_count['field']}","call Memory.alloc 1","pop pointer 0"])

        elif (subroutine_type=="method"):
            #self.output_code[subroutine_name].append(f"function {self.className}.{subroutine_name} {self.subroutines_table[subroutine_name]["subroutine_var_count"]["local"]}")             
            self.output_code[subroutine_name].extend(["push argument 0","pop pointer 0"])

        else:
            pass
            #self.output_code[subroutine_name].append(f"function {self.className}.{subroutine_name} {self.subroutines_table[subroutine_name]["subroutine_var_count"]["local"]}")             

        self.compileStatements(subroutine_name)

        curr_token=self.plain_tokens[self.token_iter]
        assert (curr_token.lexicon=="symbol" and curr_token.data=="}")

        return 




    def compileVarDec(self,subroutine_name):
        while(True):
            curr_token=self.plain_tokens[self.token_iter]
            if(curr_token.lexicon=="keyword" and curr_token.data=="var"):
                
                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]

                if(curr_token.lexicon=="keyword" and curr_token.data in ["int","char","boolean"]) or curr_token.lexicon=="identifier":
                    var_type=curr_token.data
                else:
                    raise ValueError("Error at compileVarDec() !!!")
                
                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]

                while(True):
                    if curr_token.lexicon=="identifier":
                        var_name=curr_token.data
                    else:
                        return

                    self.subroutines_table[subroutine_name]["variables"].append({var_name:{"name":var_name,"type":var_type,"kind" : "local", "idx":self.subroutines_table[subroutine_name]["subroutine_var_count"]["local"]}})
                    self.subroutines_table[subroutine_name]["subroutine_var_count"]["local"]+=1
                    self.subroutines_table[subroutine_name]["subroutine_var_count"]["total"]+=1

                    self.token_iter+=1
                    curr_token=self.plain_tokens[self.token_iter]

                    if(curr_token.lexicon=="symbol" and curr_token.data==";"):
                        self.token_iter+=1
                        curr_token=self.plain_tokens[self.token_iter]
                        break 
                    if(curr_token.lexicon=="symbol" and curr_token.data==","):
                        self.token_iter+=1
                        curr_token=self.plain_tokens[self.token_iter]
                        continue

            else:
                return

    def compileStatements(self,subroutine_name):

        while(True):
            curr_token = self.plain_tokens[self.token_iter]

            if(curr_token.lexicon=="keyword" and curr_token.data=="let"):
                self.token_iter+=1
                self.compileLetStatement(subroutine_name)
                
            elif(curr_token.lexicon=="keyword" and curr_token.data=="if"):
                self.token_iter+=1
                self.compileIfStatement(subroutine_name)
                
            elif(curr_token.lexicon=="keyword" and curr_token.data=="while"):
                self.token_iter+=1
                self.compileWhileStatement(subroutine_name)
                
            elif(curr_token.lexicon=="keyword" and curr_token.data=="do"):
                self.token_iter+=1
                self.compileDoStatement(subroutine_name)
                
            elif(curr_token.lexicon=="keyword" and curr_token.data=="return"):
                self.token_iter+=1
                self.compileReturnStatement(subroutine_name)
                
            else:
                return
        

# --------------------------------------------------------------------------------------------------------------------------------------
    def compileLetStatement(self,subroutine_name):
        
        curr_token=self.plain_tokens[self.token_iter]
        if(curr_token.lexicon=="identifier"):
            var_name=curr_token.data
        else:
            raise ValueError("Not an identifier after 'let' stmt !!!")
        
        self.token_iter+=1
        curr_token=self.plain_tokens[self.token_iter]

        if curr_token.data=="[":
            self.token_iter+=1

            self.compileExpression(subroutine_name)

            curr_token=self.plain_tokens[self.token_iter]
            assert curr_token.data=="]" and curr_token.lexicon=="symbol"

            for i in range(len(self.subroutines_table[subroutine_name]["variables"])):
                if (var_name in self.subroutines_table[subroutine_name]["variables"][i]):
                    var_kind=self.subroutines_table[subroutine_name]["variables"][i][var_name]["kind"]
                    var_idx=self.subroutines_table[subroutine_name]["variables"][i][var_name]["idx"]
            self.output_code[subroutine_name].extend([f"push {var_kind} {var_idx}","add"])

            self.token_iter+=1
            curr_token=self.plain_tokens[self.token_iter]

            assert curr_token.data=="="
            self.token_iter+=1
            self.compileExpression(subroutine_name)
            self.output_code[subroutine_name].extend(["pop temp 0","pop pointer 1","push temp 0","pop that 0"])
            

            #self.token_iter+=1
            curr_token=self.plain_tokens[self.token_iter]

            if debug and curr_token.data!=";":
                print("About line 400:\ncurr_token : ",curr_token.lexicon,curr_token.data)
                self.debug_print()
            assert (curr_token.data==";" and curr_token.lexicon=="symbol")
        
            self.token_iter+=1
            return



        else:
            assert curr_token.data=="="
            self.token_iter+=1
            self.compileExpression(subroutine_name)

            i=0
            flag=0      # not found

            if var_name in self.classSymbolTable:
                flag=1
                var_kind=self.classSymbolTable[var_name]["data_kind"]
                var_idx=self.classSymbolTable[var_name]["data_idx"]
                if var_kind=="field":
                    var_kind="this"
        
            for i in range(len(self.subroutines_table[subroutine_name]["variables"])):
                if var_name in self.subroutines_table[subroutine_name]["variables"][i]:
                    flag=1      # found
                    var_kind=self.subroutines_table[subroutine_name]["variables"][i][var_name]["kind"]
                    var_idx=self.subroutines_table[subroutine_name]["variables"][i][var_name]["idx"]
                    break

            if not flag:
                self.debug_print()

                print(self.subroutines_table[subroutine_name]["variables"])
                raise ValueError(f"{var_name} is not found error !!! ")

            if debug and printSymbolTable and self.className=="PongGame" and self.subroutine_names[-1]=="new":
                self.debug_printClassSymbolTable()
                print(f"At {subroutine_name}, under compileLetSatement, 'pop {var_kind} {var_idx}' \n,where {var_kind} {var_idx} corresponds to {var_name}")
            
            self.output_code[subroutine_name].append(f"pop {var_kind} {var_idx}")

            curr_token=self.plain_tokens[self.token_iter]

            if debug and curr_token.data!=";":
                print("About line 434:\ncurr_token : ",curr_token.lexicon,curr_token.data)
                self.debug_print(10)
            assert (curr_token.data==";" and curr_token.lexicon=="symbol")
        
            self.token_iter+=1
            return


        
    def compileIfStatement(self,subroutine_name):
        Tlabelnum=self.labelnum
        self.labelnum+=2

        curr_token=self.plain_tokens[self.token_iter]
        assert curr_token.data=="("
        self.token_iter+=1

        self.compileExpression(subroutine_name)

        curr_token=self.plain_tokens[self.token_iter]
        assert curr_token.data==")"
        self.token_iter+=1
        curr_token=self.plain_tokens[self.token_iter]
        assert curr_token.data=="{"
        self.token_iter+=1

        self.output_code[subroutine_name].extend(["not",f"if-goto {self.className}.{Tlabelnum}"])
        self.compileStatements(subroutine_name)

        curr_token=self.plain_tokens[self.token_iter]
        assert curr_token.data=="}"
        self.token_iter+=1

        self.output_code[subroutine_name].extend([f"goto {self.className}.{Tlabelnum+1}",f"label {self.className}.{Tlabelnum}"])

        curr_token=self.plain_tokens[self.token_iter]
        if curr_token.lexicon=="keyword" and curr_token.data=="else":
            self.token_iter+=1
            curr_token=self.plain_tokens[self.token_iter]
            assert curr_token.data=="{"
            self.token_iter+=1

            self.compileStatements(subroutine_name)

            curr_token=self.plain_tokens[self.token_iter]
            assert curr_token.data=="}"
            self.token_iter+=1

        self.output_code[subroutine_name].extend([f"label {self.className}.{Tlabelnum+1}"])

        return 

    def compileWhileStatement(self,subroutine_name):
        Tlabelnum=self.labelnum
        self.labelnum+=2

        curr_token=self.plain_tokens[self.token_iter]
        assert curr_token.data=="("
        self.token_iter+=1

        self.output_code[subroutine_name].extend([f"label {self.className}.{Tlabelnum}"])

        self.compileExpression(subroutine_name)

        curr_token=self.plain_tokens[self.token_iter]

        if debug and curr_token.data!=")":
            print("About line 500:\ncurr_token : ",curr_token.lexicon,curr_token.data)
            self.debug_print(10)

        assert curr_token.data==")"
        self.token_iter+=1
        curr_token=self.plain_tokens[self.token_iter]
        assert curr_token.data=="{"
        self.token_iter+=1

        self.output_code[subroutine_name].extend(["not",f"if-goto {self.className}.{Tlabelnum+1}"])
        self.compileStatements(subroutine_name)

        curr_token=self.plain_tokens[self.token_iter]

        if(curr_token.data!="}" and debug):
            self.debug_print(20)
        assert curr_token.data=="}"
        self.token_iter+=1

        self.output_code[subroutine_name].extend([f"goto {self.className}.{Tlabelnum}",f"label {self.className}.{Tlabelnum+1}"])

        return
    

    def compileDoStatement(self,subroutine_name):
        curr_token=self.plain_tokens[self.token_iter]

        assert curr_token.lexicon=="identifier"
        id1=curr_token.data

        self.token_iter+=1
        curr_token=self.plain_tokens[self.token_iter]

        if(curr_token.lexicon=="symbol" and curr_token.data=="."):
            
            self.token_iter+=1
            curr_token=self.plain_tokens[self.token_iter]

            assert curr_token.lexicon=="identifier"
            id2=curr_token.data


            flag=0              # It means that id1 is not in the class_symbol_table and not in the subroutinne_symbol_table

            for i in range(len(self.subroutines_table[subroutine_name]["variables"])):                 # can be replaced with self.subroutines_table[subroutine_name]["subroutine_var_count"]["total"]
                if(id1 in self.subroutines_table[subroutine_name]["variables"][i]):
                    id1_kind=self.subroutines_table[subroutine_name]["variables"][i][id1]["kind"]
                    id1_idx=self.subroutines_table[subroutine_name]["variables"][i][id1]["idx"]
                    id1_type=self.subroutines_table[subroutine_name]["variables"][i][id1]["type"]
                    self.output_code[subroutine_name].extend([f"push {id1_kind} {id1_idx}"])
                    flag=1
                    break

            if(id1 in self.classSymbolTable):
                id1_kind=self.classSymbolTable[id1]["data_kind"]
                id1_idx=self.classSymbolTable[id1]["data_idx"]
                id1_type=self.classSymbolTable[id1]["data_type"]


                if id1_kind=="field":
                    id1_kind="this"

                self.output_code[subroutine_name].extend([f"push {id1_kind} {id1_idx}"])
                flag=1

            self.token_iter+=1
            curr_token=self.plain_tokens[self.token_iter]

            assert curr_token.data=="("
            self.token_iter+=1
            np=self.compileExpressionList(subroutine_name)

            curr_token=self.plain_tokens[self.token_iter]
            assert curr_token.data==")"
            self.token_iter+=1

            curr_token=self.plain_tokens[self.token_iter]
            assert curr_token.data==";"
            self.token_iter+=1


            if flag:
                self.output_code[subroutine_name].extend([f"call {id1_type}.{id2} {np+1}","pop temp 0"])
            else:
                self.output_code[subroutine_name].extend([f"call {id1}.{id2} {np}","pop temp 0"])


        else:
            self.output_code[subroutine_name].extend(["push pointer 0"])
            #self.token_iter+=1                                                                             # New change
            curr_token=self.plain_tokens[self.token_iter]

            if(curr_token.data!="(" and debug):
                self.debug_print()
            assert curr_token.data=="("
            self.token_iter+=1
            np=self.compileExpressionList(subroutine_name)
            curr_token=self.plain_tokens[self.token_iter]
            assert curr_token.data==")"

            self.token_iter+=1

            curr_token=self.plain_tokens[self.token_iter]
            assert curr_token.data==";"
            self.token_iter+=1

            self.output_code[subroutine_name].extend([f"call {self.className}.{id1} {np+1}","pop temp 0"])
        
        return            


    def compileReturnStatement(self,subroutine_name):
        curr_token=self.plain_tokens[self.token_iter]
        if curr_token.lexicon=="symbol" and curr_token.data==";":
            self.output_code[subroutine_name].extend(["push constant 0","return"])
            self.token_iter+=1
            return
        self.compileExpression(subroutine_name)
        self.output_code[subroutine_name].extend(["return"])

        curr_token=self.plain_tokens[self.token_iter]
        assert curr_token.lexicon=="symbol" and curr_token.data==";"
        self.token_iter+=1
        return

    def compileExpression(self,subroutine_name):
        self.compileTerm(subroutine_name)
        curr_token=self.plain_tokens[self.token_iter]

        if False and debug:
            flag=0
            print(".........................................")
            print(curr_token.lexicon,curr_token.data)
            print(".........................................")


        op_dict={"+":"add","-":"sub","/":"call Math.divide 2","|":"or","&amp;":"and","&lt;":"lt","&gt;":"gt","=":"eq","*":"call Math.multiply 2"}

        while curr_token.lexicon=="symbol" and curr_token.data in ["+","-","/","|","&amp;","&lt;","&gt;","=","*"] and not curr_token.data==";":
            curr_symbol=curr_token.data         # Very Very Important !!!       Because the operator should be added after pushing the two operands!!!

            self.token_iter+=1
            self.compileTerm(subroutine_name)
            self.output_code[subroutine_name].append(op_dict[curr_symbol])
            curr_token=self.plain_tokens[self.token_iter]
            if False and debug:
                flag=1
            continue
        

        if False and debug:
            if flag==1:
                return
            print(".........................................")
            print(curr_token.lexicon,curr_token.data)
            print(".........................................")
        return


    def compileExpressionList(self,subroutine_name):
        np=0

        curr_token=self.plain_tokens[self.token_iter]
        if(curr_token.data==")"):
            return np 
        
        while True:
            self.compileExpression(subroutine_name)
            np+=1

            curr_token=self.plain_tokens[self.token_iter]
            if(curr_token.data==")"):
                return np
            elif curr_token.data==",":
                self.token_iter+=1
                continue

            else:
                self.debug_print(10)
                raise ValueError("Error at curr_token value ( Under compileExpressionList() !!! )")       
            

    def compileTerm(self,subroutine_name):
        curr_token=self.plain_tokens[self.token_iter]

        if False and debug:
            print("At compileTerm() :",curr_token.lexicon,curr_token.data)

        if(curr_token.lexicon=="symbol" and curr_token.data in ["-","~"]):
            op="not"
            if(curr_token.data=="-"):
                op="neg"
            self.token_iter+=1
            self.compileTerm(subroutine_name)

            self.output_code[subroutine_name].append(op)
            return 

        elif curr_token.data=="(":
            self.token_iter+=1
            self.compileExpression(subroutine_name)

            curr_token=self.plain_tokens[self.token_iter]
            assert curr_token.data==")"

            self.token_iter+=1                                                                               # Doubt whether to increment the token_iter ???
            return
        
        elif curr_token.lexicon=="integerConstant":
            self.output_code[subroutine_name].append(f"push constant {curr_token.data}")
            self.token_iter+=1
            return

        elif curr_token.lexicon=="stringConstant":
            mystr=curr_token.data
            lenStr=len(mystr)
            self.output_code[subroutine_name].extend([f"push constant {lenStr}","call String.new 1"])

            for i in range(lenStr):
                self.output_code[subroutine_name].extend([f"push constant {ord(mystr[i])}","call String.appendChar 2"])

            self.token_iter+=1
            return

        elif curr_token.lexicon=="keyword":
            if curr_token.data=="this":
                self.output_code[subroutine_name].append("push pointer 0")
                self.token_iter+=1
                return
            
            assert curr_token.data in ["true","false","null"]
            self.output_code[subroutine_name].append("push constant 0")
            if curr_token.data=="true":
                self.output_code[subroutine_name].append("not")


            if False and debug:
                print("....................Before.........................")
                print(curr_token.lexicon,curr_token.data)
                print(".........................................")

            self.token_iter+=1

            if False and debug:
                curr_token=self.plain_tokens[self.token_iter]
                print(".....................After..................")
                print(curr_token.lexicon,curr_token.data)
                print(".........................................")
            return 

        elif curr_token.lexicon=="identifier":
            varname=curr_token.data
            self.token_iter+=1
            curr_token=self.plain_tokens[self.token_iter]

            flag=0
            if curr_token.data not in ["[","(","."]:
                for i in range(len(self.subroutines_table[subroutine_name]["variables"])):
                    if(varname in self.subroutines_table[subroutine_name]["variables"][i]):
                        var_kind=self.subroutines_table[subroutine_name]["variables"][i][varname]["kind"]
                        var_type=self.subroutines_table[subroutine_name]["variables"][i][varname]["type"]
                        var_idx=self.subroutines_table[subroutine_name]["variables"][i][varname]["idx"]
                        self.output_code[subroutine_name].extend([f"push {var_kind} {var_idx}"])
                        flag=1
                        break

                if varname in self.classSymbolTable and not flag:
                    var_kind=self.classSymbolTable[varname]["data_kind"]
                    var_idx=self.classSymbolTable[varname]["data_idx"]
                    var_type=self.classSymbolTable[varname]["data_type"]

                    if var_kind=="field":
                        var_kind="this"


                    self.output_code[subroutine_name].extend([f"push {var_kind} {var_idx}"])
                    flag=1

                if not flag:
                    raise ValueError("(1st) Flag remains zero..... Meaning that not in any symbol Table")
                
            elif curr_token.data=="[":
                self.token_iter+=1
                
                self.compileExpression(subroutine_name)
                curr_token=self.plain_tokens[self.token_iter]
                assert curr_token.data=="]"

                for i in range(len(self.subroutines_table[subroutine_name]["variables"])):
                    if(varname in self.subroutines_table[subroutine_name]["variables"][i]):
                        var_kind=self.subroutines_table[subroutine_name]["variables"][i][varname]["kind"]
                        var_type=self.subroutines_table[subroutine_name]["variables"][i][varname]["type"]
                        var_idx=self.subroutines_table[subroutine_name]["variables"][i][varname]["idx"]
                        self.output_code[subroutine_name].extend([f"push {var_kind} {var_idx}"])
                        flag=1
                        break

                if varname in self.classSymbolTable and not flag:
                    var_kind=self.classSymbolTable[varname]["data_kind"]
                    var_idx=self.classSymbolTable[varname]["data_idx"]
                    var_type=self.classSymbolTable[varname]["data_type"]

                    if var_kind=="field":
                        var_kind="this"

                    self.output_code[subroutine_name].extend([f"push {var_kind} {var_idx}"])
                    flag=1

                if not flag:
                    raise ValueError("(2nd) Flag remains zero..... Meaning that not in any symbol Table")
                
                self.output_code[subroutine_name].extend(["add","pop pointer 1","push that 0"])

                self.token_iter+=1
                return
            
            elif curr_token.data=="(":
                self.output_code[subroutine_name].extend([f"push pointer 0"])
                self.token_iter+=1

                np=self.compileExpressionList(subroutine_name)

                curr_token=self.plain_tokens[self.token_iter]
                assert curr_token.data==")"

                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]
                assert curr_token.data==";"

                self.token_iter+=1

                self.output_code[subroutine_name].extend([f"call {self.className}.{varname} {np+1}"])
                return
            
            else:
                id1=varname
                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]

                assert curr_token.lexicon=="identifier"
                id2=curr_token.data


                flag=0              # It means that id1 is not in the class_symbol_table and not in the subroutinne_symbol_table

                for i in range(len(self.subroutines_table[subroutine_name]["variables"])):                 # can be replaced with self.subroutines_table[subroutine_name]["subroutine_var_count"]["total"]
                    if(id1 in self.subroutines_table[subroutine_name]["variables"][i]):
                        id1_kind=self.subroutines_table[subroutine_name]["variables"][i][id1]["kind"]
                        id1_idx=self.subroutines_table[subroutine_name]["variables"][i][id1]["idx"]
                        id1_type=self.subroutines_table[subroutine_name]["variables"][i][id1]["type"]
                        self.output_code[subroutine_name].extend([f"push {id1_kind} {id1_idx}"])
                        flag=1
                        break

                if(id1 in self.classSymbolTable):
                    id1_kind=self.classSymbolTable[id1]["data_kind"]
                    id1_idx=self.classSymbolTable[id1]["data_idx"]
                    id1_type=self.classSymbolTable[id1]["data_type"]

                    if id1_kind=="field":
                        id1_kind="this"


                    self.output_code[subroutine_name].extend([f"push {id1_kind} {id1_idx}"])
                    flag=1

                self.token_iter+=1
                curr_token=self.plain_tokens[self.token_iter]

                assert curr_token.data=="("
                self.token_iter+=1
                np=self.compileExpressionList(subroutine_name)

                curr_token=self.plain_tokens[self.token_iter]
                assert curr_token.data==")"
                self.token_iter+=1

                curr_token=self.plain_tokens[self.token_iter]
                #assert curr_token.data==";"
                #self.token_iter+=1                                                                    # Use only verification of ";" once


                if flag:
                    self.output_code[subroutine_name].extend([f"call {id1_type}.{id2} {np+1}"])
                else:
                    self.output_code[subroutine_name].extend([f"call {id1}.{id2} {np}"])
                
                
                return
            




# main() ....................................
res_data=[]
input_given=sys.argv[1]



# ---------------------------------------------------------- To handle directory ---------------------------------------------------------------------------

if os.path.isdir(input_given):
    folder_name = os.path.basename(os.path.normpath(input_given))

    for file_name in os.listdir(input_given):
        if not file_name.endswith(".jack"):
            continue

        file_full_path=os.path.join(input_given,file_name)


        c=Compiler(file_full_path)
        if printAllTokens:
            for i in (c.plain_tokens):
                print(i.data)        
        
        c.compileClass()

        if debug and printSymbolTable:            
            #print("c.classSymbolTable",c.classSymbolTable)
            c.debug_printClassSymbolTable()

            #print("c.subroutines_table",c.subroutines_table)
            c.debug_printSubroutineSymbolTable()

        with open(f"{file_name[:-5]}.vm","w") as f:
            for i in c.output_code:
                f.writelines("\n".join(c.output_code[i]))
                f.write("\n")

            


    

    


# ---------------------------------------------------------- To handle file ---------------------------------------------------------------------------

elif os.path.isfile(input_given):
    if not input_given.endswith(".jack"):
        exit(1)             # Exit with an error

    parent_folder_name=os.path.dirname(input_given)
    file=os.path.basename(os.path.normpath(input_given))
    file_name=file[:-5]


    c=Compiler(input_given)

    if printAllTokens:
        for i in (c.plain_tokens):
            print(i.data)


    c.compileClass()   


    #print(c.output_code)
    if debug and printSymbolTable:

        #print("c.classSymbolTable",c.classSymbolTable)
        c.debug_printClassSymbolTable()

        #print("c.subroutines_table",c.subroutines_table)
        c.debug_printSubroutineSymbolTable()


    with open(f"{file_name}.vm","w") as f:
        for i in c.subroutine_names:
            f.writelines("\n".join(c.output_code[i]))
            f.write("\n")