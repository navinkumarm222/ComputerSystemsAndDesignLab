import sys ,os 

# global variable to identify multi-line comments
multi_comment_present=0




# Class Definitions
class Token:
    def __init__(self,data,lex):
        self.data=data 
        self.lexicon=lex
    
    def printAttributes(self):
        print("Data :", self.data," , lexicon :",self.lexicon)
        return

    def getXML(self):
        return f"<{self.lexicon}> {self.data} </{self.lexicon}>"
    

# Data-processing functions......................

def clean(line):
    line=line.strip()
    global multi_comment_present

    #check if already existing multi-line is not processed completely
    if(multi_comment_present):
        if("*/" in line):
            end_idx=line.find("*/")
            line=line[end_idx+2:]
            multi_comment_present=0
        else:
            return ""

    #check new multi-line comment
    line1=""
    line2=""
    start_idx=line.find("/*")
    if start_idx!=-1:
        end_idx=line[start_idx+2:].find("*/")
        if end_idx==-1:
            multi_comment_present=1
        else:
            line2=line[start_idx+2:][end_idx+2:].strip()                # very important !!! Because end_idx is relative to 'line[start_idx+2:]' , and not 'line'
        line1=line[:start_idx].strip()
        line=line1+" "+line2


    #check inline comment
    idx=line.find("//")
    if idx!=-1:
        line=line[:idx].strip()

    return line


def process(line):
    list_of_tokens=[]
    cleaned_line=clean(line)

    symbol=['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
    keyword=['class','constructor','function','method','field','static','var','int','char',
             'boolean','void','true','false','null','this','let','do','if','else','while','return']

    elem=""
    isInteger=False
    isString=False
    for i in range(len(cleaned_line)):
        if(cleaned_line[i] in symbol or cleaned_line[i].isspace()):
            if elem:
                if isInteger:
                    list_of_tokens.append(Token(elem,"integerConstant"))
                    isInteger=False

                elif isString:
                    if cleaned_line[i].isspace():
                        elem+=cleaned_line[i]
                        continue
                    list_of_tokens.append(Token(elem,"stringConstant"))
                    isString=False

                elif elem in keyword:
                    list_of_tokens.append(Token(elem,"keyword"))
                
                else:
                    list_of_tokens.append(Token(elem,"identifier"))

                elem=""
            if(not cleaned_line[i].isspace()):
                if(cleaned_line[i]=="<"):
                    list_of_tokens.append(Token("&lt;","symbol"))
                elif cleaned_line[i]==">":
                    list_of_tokens.append(Token("&gt;","symbol"))
                elif cleaned_line[i]=="&":
                    list_of_tokens.append(Token("&amp;","symbol"))
                else:
                    list_of_tokens.append(Token(cleaned_line[i],"symbol"))

        else:
            if(cleaned_line[i].isdigit()):
                if(not elem):
                    isInteger=True
                elem+=cleaned_line[i]

            else:
                if(not elem) and cleaned_line[i]=='"':
                    isString=True
                    continue
                elif elem and cleaned_line[i]=='"' and isString:
                    isString=False
                    list_of_tokens.append(Token(elem,"stringConstant"))
                    elem=""
                    continue
                elem+=cleaned_line[i]

    # after loop ..... Check if elem contains any remaining unprocessed term

    if elem:
        if isInteger:
            list_of_tokens.append(Token(elem,"integerConstant"))
            isInteger=False

        elif isString:
            list_of_tokens.append(Token(elem,"stringConstant"))
            isString=False

        elif elem in keyword:
            list_of_tokens.append(Token(elem,"keyword"))
                
        else:
            list_of_tokens.append(Token(elem,"identifier"))
        elem=""

    return list(list_of_tokens)




# main() ............................
res_data=[]
input_given=sys.argv[1]


# ---------------------------------------------------------- To handle directory ---------------------------------------------------------------------------

if os.path.isdir(input_given):

    folder_name = os.path.basename(os.path.normpath(input_given))
    #outputfile = os.path.join(input_given, folder_name + ".xml")

    for file_name in os.listdir(input_given):
        if not file_name.endswith(".jack"):
            continue
        
        file_full_path=os.path.join(input_given,file_name)
        with open(file_full_path,"r") as f:
            lines=f.readlines()
            for curr_line in lines:
                curr_token_list=process(curr_line)
                for token in curr_token_list:
                    xml_line=token.getXML()
                    res_data.append(xml_line)
                    res_data.append("\n")

        outputfile_name=file_name.replace(".jack","_mine.xml")
        outputfile = os.path.join(input_given,outputfile_name)

        with open(outputfile,"w") as f:
            
            f.write("<tokens>\n")
            f.writelines(res_data)
            f.write("</tokens>\n")
        
        res_data=[]
    
    


# ---------------------------------------------------------- To handle file ---------------------------------------------------------------------------

elif os.path.isfile(input_given):
    if not input_given.endswith(".jack"):
        exit(1)             # Exit with an error

    parent_folder_name=os.path.dirname(input_given)
    file=os.path.basename(os.path.normpath(input_given)) 
    
    outputfile_name=file.replace(".jack","_mine.xml")

    outputfile = os.path.join(parent_folder_name,outputfile_name)

    
    with open(input_given,"r") as f:
        lines=f.readlines()
        for curr_line in lines:
            curr_token_list=process(curr_line)
            for token in curr_token_list:
                xml_line=token.getXML()
                res_data.append(xml_line)
                res_data.append("\n")
        
    outputfile = os.path.join(parent_folder_name,outputfile_name)

    with open(outputfile,"w") as f:
        
        f.write("<tokens>\n")
        f.writelines(res_data)
        f.write("</tokens>\n")
        
    res_data=[]
      