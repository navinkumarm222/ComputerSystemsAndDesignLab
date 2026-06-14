
@256
D=A
@SP
M=D

@Sys.init$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

@3
D=M
@SP
A=M
M=D
@SP
M=M+1

@4
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
D=M
@5
D=D-A
@ARG
M=D

@SP
D=M
@LCL
M=D

@Sys.init
0;JMP
(Sys.init$ret.1)

@256
D=A
@SP
M=D
(Sys.init)

@4
D=A
@SP
A=M
M=D
@SP
M=M+1

@Main.fibonacci$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

@3
D=M
@SP
A=M
M=D
@SP
M=M+1

@4
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
D=M
@6
D=D-A
@ARG
M=D

@SP
D=M
@LCL
M=D

@Main.fibonacci
0;JMP
(Main.fibonacci$ret.1)
(END)

@END
0;JMP
(Main.fibonacci)

@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@2
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
A=A-1
D=M-D
@LABELA1
D;JLT
@SP
A=M-1
M=0
@LABELB1
0;JMP
(LABELA1)
@SP
A=M-1
M=-1
(LABELB1)


@SP
AM=M-1
D=M
@Main.vm$N_LT_2
D;JNE

@Main.vm$N_GE_2
0;JMP
(Main.vm$N_LT_2)

@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

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
(Main.vm$N_GE_2)

@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@2
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1

@Main.fibonacci$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

@3
D=M
@SP
A=M
M=D
@SP
M=M+1

@4
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
D=M
@6
D=D-A
@ARG
M=D

@SP
D=M
@LCL
M=D

@Main.fibonacci
0;JMP
(Main.fibonacci$ret.2)

@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@1
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1

@Main.fibonacci$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

@3
D=M
@SP
A=M
M=D
@SP
M=M+1

@4
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
D=M
@6
D=D-A
@ARG
M=D

@SP
D=M
@LCL
M=D

@Main.fibonacci
0;JMP
(Main.fibonacci$ret.3)

@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1

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
