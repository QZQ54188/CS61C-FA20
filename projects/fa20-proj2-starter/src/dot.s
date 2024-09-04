.globl dot

.text
# =======================================================
# FUNCTION: Dot product of 2 int vectors
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int)  is the stride of v0
#   a4 (int)  is the stride of v1
# Returns:
#   a0 (int)  is the dot product of v0 and v1
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 75.
# - If the stride of either vector is less than 1,
#   this function terminates the program with error code 76.
# =======================================================
dot:

	#check error
	blez a2, error_length
	blez a3, error_strride
	blez a4, error_strride

    # Prologue
	addi sp sp -12
	sw ra 0(sp)
	sw s0 4(sp)
	sw s1 8(sp)

	mv s0, a0 	# s0 is the pointer of v0
	mv s1, a1 	# s1 is the pointer 0f v1
	mv t0, a2 	# t0 is length
	mv t3, a3	#stride of v0
	mv t4, a4	#stride of v1

	li t1, 0 	# t1 is the count
	li t2, 0 	#the result

	#clac actual offset
	slli t3, t3, 2
	slli t4, t4, 2

loop_start:

    beq t1, t0, loop_end
	lw t5, 0(s0)
	lw t6, 0(s1)
	
	mul t5, t5, t6
	add t2, t2, t5 # the result of the mul v0[]*v1[]

	add s0, s0, t3
    add s1, s1, t4
	addi t1, t1, 1

	j loop_start

loop_end:

	mv a0, t2

    # Epilogue
	lw s1, 8(sp)
    lw s0, 4(sp)
	lw ra, 0(sp)
	addi sp, sp, 12
    ret

error_length:
	li a1, 75
	call exit2

error_strride:
	li a1, 76
	call exit2