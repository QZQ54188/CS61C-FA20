#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "lfsr.h"

void lfsr_calculate(uint16_t *reg) {
    /* YOUR CODE HERE */
    uint16_t bit0 = *reg & 1;
    uint16_t bit1 = (*reg >> 2) & 1;
    uint16_t bit2 = (*reg >> 3) & 1;
    uint16_t bit3 = (*reg >> 5) & 1;

    uint16_t newBit = bit0 ^ bit1 ^ bit2 ^ bit3;

    *reg >>= 1;
    *reg |= (newBit << 15);
}

