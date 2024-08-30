.globl simple_fn naive_pow inc_arr

.data
failure_message: .asciiz "Test failed for some reason.\n"
success_message: .asciiz "Sanity checks passed! Make sure there are no CC violations.\n"
array:
    .word 1 2 3 4 5
exp_inc_array_result:
    .word 2 3 4 5 6

.text
main:
    li s0, 2623
    li s1, 2910
    li s11, 134
    jal simple_fn
    li t0, 1
    bne a0, t0, failure
    li a0, 2
    li a1, 7
    jal naive_pow
    li t0, 128
    bne a0, t0, failure
    la a0, array
    li a1, 5
    jal inc_arr
    jal check_arr
    li t0, 2623
    li t1, 2910
    li t2, 134
    bne s0, t0, failure
    bne s1, t1, failure
    bne s11, t2, failure
    li a0, 4
    la a1, success_message
    ecall
    li a0, 10
    ecall

simple_fn:
    li a0, 1
    ret

naive_pow:
    # BEGIN PROLOGUE
    addi sp, sp, -4
    sw s0, 0(sp)
    # END PROLOGUE
    li s0, 1
naive_pow_loop:
    beq a1, zero, naive_pow_end
    mul s0, s0, a0
    addi a1, a1, -1
    j naive_pow_loop
naive_pow_end:
    mv a0, s0
    # BEGIN EPILOGUE
    lw s0, 0(sp)
    addi sp, sp, 4
    # END EPILOGUE
    ret

inc_arr:
    # BEGIN PROLOGUE
    addi sp, sp, -12
    sw ra, 0(sp)
    sw s0, 4(sp)
    sw s1, 8(sp)
    # END PROLOGUE
    mv s0, a0
    li t0, 0           # Initialize index to 0
    li s1, 5           # Array size
inc_arr_loop:
    beq t0, s1, inc_arr_end
    slli t1, t0, 2     # Convert array index to byte offset
    add a0, s0, t1     # Add offset to start of array
    jal helper_fn      # Call helper_fn
    addi t0, t0, 1     # Increment index
    j inc_arr_loop

inc_arr_end:
    # BEGIN EPILOGUE
    lw ra, 0(sp)      # Restore return address from stack
    lw s0, 4(sp)      # Restore s0 from stack
    lw s1, 8(sp)      # Restore s1 from stack
    addi sp, sp, 12   # Deallocate stack space
    # END EPILOGUE
    ret

helper_fn:
    # BEGIN PROLOGUE
    addi sp, sp, -4
    sw s0, 0(sp)
    # END PROLOGUE
    lw t1, 0(a0)
    addi s0, t1, 1
    sw s0, 0(a0)
    # BEGIN EPILOGUE
    lw s0, 0(sp)
    addi sp, sp, 4
    # END EPILOGUE
    ret

# YOU CAN IGNORE EVERYTHING BELOW THIS COMMENT

# Checks the result of inc_arr, which should contain 2 3 4 5 6 after
# one call.
# You can safely ignore this function; it has no errors.
check_arr:
    la t0, exp_inc_array_result
    la t1, array
    addi t2, t1, 20 # Last element is 5*4 bytes off
check_arr_loop:
    beq t1, t2, check_arr_end
    lw t3, 0(t0)
    lw t4, 0(t1)
    bne t3, t4, failure
    addi t0, t0, 4
    addi t1, t1, 4
    j check_arr_loop
check_arr_end:
    ret
    

# This isn't really a function - it just prints a message, then
# terminates the program on failure. Think of it like an exception.
failure:
    li a0, 4 # String print ecall
    la a1, failure_message
    ecall
    li a0, 10 # Exit ecall
    ecall
    
