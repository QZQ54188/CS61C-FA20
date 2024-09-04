.globl abs

.text
# =================================================================
# FUNCTION: Given an int return its absolute value.
# Arguments:
# 	a0 (int) is input integer
# Returns:
#	a0 (int) the absolute value of the input
# =================================================================
abs:
    # Check if the input is negative
    bgez a0, done          # If a0 >= 0, jump to done (a0 is already non-negative)
    neg  a0, a0            # Negate a0 to make it positive if it's negative

done:
    ret                    # Return from the function
