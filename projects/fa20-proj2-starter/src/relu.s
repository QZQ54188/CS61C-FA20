.globl relu

.text
# ==============================================================================
# FUNCTION: Performs an inplace element-wise ReLU on an array of ints
# Arguments:
# 	a0 (int*) is the pointer to the array
#	a1 (int)  is the # of elements in the array
# Returns:
#	None
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 78.
# ==============================================================================
relu:

    blez a1, error_length
    li t0, 1

    # Prologue
    addi sp, sp, -4
    sw ra, 0(sp)

loop_start:
    li t0, 0       #t0 is the counter
    li t1, 4        #size of a word

loop_continue:
    beq t0, a1, loop_end
    mul t2, t0, t1
    add t3, a0, t2      #t3存储了目标字符的地址
    lw t4, 0(t3)
    addi t0, t0, 1
    blt t4, x0, change
    j loop_continue


loop_end:
    lw ra, 0(sp)
    addi sp, sp, 4
	ret

change:
    sw x0, 0(t3)
    j loop_continue

error_length:
    li a0, 78
    ecall
    