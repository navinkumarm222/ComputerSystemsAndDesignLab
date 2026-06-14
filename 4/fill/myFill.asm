// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

(START)
@i
M=0 // Till 8191

@KBD
D=M
@WHITELOOP
D;JEQ


(BLACKLOOP)
@i
D=M
@16384
A=A+D
M=-1

@i
M=M+1
D=M
@8192
D=D-A
@BLACKLOOP
D;JLT
@END
0;JMP


(WHITELOOP)
@i
D=M
@16384
A=A+D
M=0

@i
M=M+1
D=M
@8192
D=D-A
@WHITELOOP
D;JLT

(END)
@START
0;JMP


	


