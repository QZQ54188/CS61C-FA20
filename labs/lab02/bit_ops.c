#include <stdio.h>
#include "bit_ops.h"

// Return the nth bit of x.
// Assume 0 <= n <= 31
unsigned get_bit(unsigned x,
                 unsigned n) {
    // YOUR CODE HERE
    // Returning -1 is a placeholder (it makes
    // no sense, because get_bit only returns 
    // 0 or 1)
    if(n > 31){
        return -1;
    }
    return (x >> n) & 1;
}


// Set the nth bit of the value of x to v.
// Assume 0 <= n <= 31, and v is 0 or 1
void set_bit(unsigned * x,
             unsigned n,
             unsigned v) {
    // YOUR CODE HERE
    unsigned curBit = get_bit(*x, n);
    if(curBit != v){
        if(v == 1){
            *x |= (1U << n);
        }else{
            *x &= ~(1U << n);
        }
    }

}


// Flip the nth bit of the value of x.
// Assume 0 <= n <= 31
void flip_bit(unsigned * x,
              unsigned n) {
    // YOUR CODE HERE
    unsigned curBit = get_bit(*x, n);
    set_bit(x, n, !curBit);
}

