#.data指令用于定义数据段，存放静态数据，.data指令之后的数据将存储在数据段中
#
.data
.word 2, 4, 6, 8
n: .word 9

#.text 指令用于定义代码段。代码段是存放指令的区域，
#程序运行时，处理器会从这个区域读取并执行指令。
.text


main:
    add t0, x0, x0
    addi t1, x0, 1
    #加载n的地址到t3寄存器中
    la t3, n
    lw t3, 0(t3)
fib:
    beq t3, x0, finish
    add t2, t1, t0
    mv t0, t1
    mv t1, t2
    addi t3, t3, -1
    #无条件跳转指令
    j fib
finish:
    #a0是用来指定系统调用编号的寄存器，a0中的不同数字可以产生不同的函数调用
    addi a0, x0, 1
    addi a1, t0, 0
    ecall # print integer ecall
    addi a0, x0, 10
    ecall # terminate ecall
