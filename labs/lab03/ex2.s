.globl main

.data
source:
    .word   3
    .word   1
    .word   4
    .word   1
    .word   5
    .word   9
    .word   0
dest:
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0
    .word   0

.text
fun:
    #t0-t6是临时寄存器，用于在计算中存储中间结果
    addi t0, a0, 1
    sub t1, x0, a0
    #a0是用来返回函数结果的寄存器
    mul a0, t0, t1
    #跳转到ra寄存器中储存的地址，用于函数返回
    jr ra

main:
    # BEGIN PROLOGUE
    addi sp, sp, -20
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw ra, 16(sp)
    # END PROLOGUE
    addi t0, x0, 0
    addi s0, x0, 0
    #s0-s11是保存寄存器，用于存储在函数中需要保留一段时间的变量或数据。
    la s1, source       #The registers acting as pointers to the source.
    la s2, dest         #The registers acting as pointers to the dest arrays.
#The assembly code for the loop found in the C code.
loop:
    slli s3, t0, 2      # s3 = t0 << 2 (t0 * 4) 用于计算数组偏移量
    add t1, s1, s3      # t1 = s1 + s3 计算当前数组元素的地址
    lw t2, 0(t1)        # t2 = *t1 从数组中加载当前元素到t2
    beq t2, x0, exit    # if (t2 == 0) 跳转到exit，结束循环
    add a0, x0, t2      # a0 = t2 将当前元素的值传递给a0，准备作为函数参数
    addi sp, sp, -8     # sp -= 8 准备堆栈，保存当前状态
    sw t0, 0(sp)        # 将t0保存到堆栈
    sw t2, 4(sp)        # 将t2保存到堆栈
    jal fun             # 调用函数 fun (函数调用后返回a0中的结果)
    lw t0, 0(sp)        # 恢复t0的值
    lw t2, 4(sp)        # 恢复t2的值
    addi sp, sp, 8      # sp += 8 恢复堆栈指针
    add t2, x0, a0      # t2 = a0 保存函数的返回值
    add t3, s2, s3      # t3 = s2 + s3 计算保存结果的地址
    sw t2, 0(t3)        # 将结果保存回数组
    add s0, s0, t2      # s0 += t2 更新总和，The register representing the variable sum.
    addi t0, t0, 1      # t0 += 1 增加数组索引，The register representing the variable k.
    jal x0, loop
exit:
    add a0, x0, s0      # 将 s0 的值复制到 a0 中，通常 a0 用于返回值
    # BEGIN EPILOGUE
    lw s0, 0(sp)        #将保存寄存器中的值恢复为0
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw ra, 16(sp)
    addi sp, sp, 20
    # END EPILOGUE
    jr ra
