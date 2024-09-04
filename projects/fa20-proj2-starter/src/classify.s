.globl classify

.text
classify:
    # =====================================
    # COMMAND LINE ARGUMENTS
    # =====================================
    # Args:
    #   a0 (int)    argc
    #   a1 (char**) argv
    #   a2 (int)    print_classification, if this is zero, 
    #               you should print the classification. Otherwise,
    #               this function should not print ANYTHING.
    # Returns:
    #   a0 (int)    Classification
    # Exceptions:
    # - If there are an incorrect number of command line args,
    #   this function terminates the program with exit code 89.
    # - If malloc fails, this function terminats the program with exit code 88.
    #
    # Usage:
    #   main.s <M0_PATH> <M1_PATH> <INPUT_PATH> <OUTPUT_PATH>

    li t0, 5
    bne a0, t0, error_args

    addi sp, sp, -32
    sw s0, 0(sp)                            # malloc space
    sw s1, 4(sp)                            # argv
    sw s2, 8(sp)                            # print_classification
    sw s3, 12(sp)                           # m0
    sw s4, 16(sp)                           # m1
    sw s5, 20(sp)                           # input
    sw s6, 24(sp)                           # argmax
    sw ra, 28(sp)
    mv s1, a1                               # ** argv
    mv s2, a2

    li a0, 36       #9 * sizeof(int)
    jal malloc
    beqz a0, error_malloc
    mv s0, a0       #s0 save the ptr address


	# =====================================
    # LOAD MATRICES
    # =====================================

    #load m0
    lw a0, 4(s1)    #argv[1] == <M0_PATH>
    addi a1, s0, 0
    addi a2, s0, 4
    jal read_matrix
    mv s3, a0

    #load m1
    lw a0, 8(s1)    #argv[2] == <M1_PATH>
    addi a1, s0, 8
    addi a2, s0, 12
    jal read_matrix
    mv s4, a0

    #load input 
    lw a0, 12(s1)
    addi a1, s0, 16
    addi a2, s0, 20
    jal read_matrix
    mv s5, a0



    # =====================================
    # RUN LAYERS
    # =====================================
    # 1. LINEAR LAYER:    m0 * input
    # 2. NONLINEAR LAYER: ReLU(m0 * input)
    # 3. LINEAR LAYER:    m1 * ReLU(m0 * input)

    # 1. LINEAR LAYER:    m0 * input
    lw a0, 0(s0)        #m0's row
    lw t0, 20(s0)       #input's col
    mul a0, a0, t0
    slli a0, a0, 2
    jal malloc
    beqz a0, error_malloc
    sw a0, 24(s0)       # save pointer to h to 24(s0)

   # matmul(a0, input)
    mv a0, s3           # m0
    lw a1, 0(s0)        # m0_row
    lw a2, 4(s0)        # m0_col
    mv a3, s5           # input
    lw a4, 16(s0)       # input_row
    lw a5, 20(s0)       # input_col   
    lw a6, 24(s0)       # pointer to h
    jal matmul 



    #2. NONLINEAR LAYER: ReLU(m0 * input)
    lw a0, 24(s0)
    lw t0, 0(s0)
    lw t1, 20(s0)
    mul a1, t0, t1      # The number of integers in the array       
    jal relu


    # 3. LINEAR LAYER:    m1 * ReLU(m0 * input)
    # malloc space
    lw a0, 8(s0)                            # m1_row
    lw t0, 20(s0)                           # h_col (same as input_col)
    mul a0, a0, t0                          # row * col
    slli a0, a0, 2                          # * 4 bytes
    jal malloc
    beqz a0, error_malloc
    sw a0, 28(s0)                           # save pointer to o to 28(s0)

    # matmul(a1, h)
    mv a0, s4                               # m1
    lw a1, 8(s0)                            # m1_row
    lw a2, 12(s0)
    lw a3, 24(s0)                           # h
    lw a4, 0(s0)                            # m0_row
    lw a5, 20(s0)                           # input_col
    lw a6, 28(s0)                           # o
    jal matmul


    # =====================================
    # WRITE OUTPUT
    # =====================================
    # Write output matrix

    lw a0, 16(s1)                           # OUTPUT_PATH
    lw a1, 28(s0)                           # o
    lw a2, 8(s0)                            # m1_row
    lw a3, 20(s0)                           # input_col
    jal write_matrix



    # =====================================
    # CALCULATE CLASSIFICATION/LABEL
    # =====================================
    # Call argmax

    lw a0, 28(s0)                           # o
    lw t0, 8(s0)                            # m1_row
    lw t1, 20(s0)                           # input_col
    mul a1, t0, t1                          # size
    jal argmax
    mv s6, a0 


    # Print classification
    
    bne s2, x0, end
    mv a1, s6
    jal print_int


    # Print newline afterwards for clarity

    li a1, '\n'
    jal print_char


end:
    # free space
    lw a0, 24(s0)                           # h
    jal free
    lw a0, 28(s0)                           # o
    jal free
    mv a0, s0
    jal free
    mv a0, s3
    jal free
    mv a0, s4
    jal free
    mv a0, s5
    jal free

    mv a0, s6
    
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)                           # m0
    lw s4, 16(sp)                           # m1
    lw s5, 20(sp)
    lw s6, 24(sp)
    lw ra, 28(sp)
    addi sp, sp, 32
    ret

error_args:
    li a1, 89
    call exit2

error_malloc:
    li a1, 88
    call exit2