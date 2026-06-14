
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
@THAT
M=D

@0
D=A
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

@1
D=A
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

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

@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
(FibonacciSeries.vm$LOOP)

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

@SP
AM=M-1
D=M
@FibonacciSeries.vm$COMPUTE_ELEMENT
D;JNE

@FibonacciSeries.vm$END
0;JMP
(FibonacciSeries.vm$COMPUTE_ELEMENT)

@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1

@THAT
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

@4
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
M=D+M
@SP
M=M-1

@SP
AM=M-1
D=M
@THAT
M=D

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

@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

@FibonacciSeries.vm$LOOP
0;JMP
(FibonacciSeries.vm$END)
