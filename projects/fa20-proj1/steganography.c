/************************************************************************
**
** NAME:        steganography.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**				Justin Yokota - Starter Code
**				YOUR NAME HERE
**
** DATE:        2020-08-23
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "imageloader.h"

//Determines what color the cell at the given row/col should be. This should not affect Image, and should allocate space for a new Color.
Color *evaluateOnePixel(Image *image, int row, int col)
{
	//YOUR CODE HERE
	Color originColor = image->image[row][col];
	Color *newColor = (Color *)malloc(sizeof(Color));
	if(newColor == NULL){
		printf("Memory allocation failed.\n");
        return NULL;
	}

	if(originColor.B & 1){
		newColor->R = 255;
		newColor->G = 255;
		newColor->B = 255;
	}else{
		newColor->R = 0;
		newColor->G = 0;
		newColor->B = 0;
	}

	return newColor;
}

//Given an image, creates a new image extracting the LSB of the B channel.
Image *steganography(Image *image)
{
	//YOUR CODE HERE
	Image *img = (Image *)malloc(sizeof(Image));
	if (img == NULL) {
        printf("Memory allocation failed.\n");
        return NULL;
    }

	img->cols = image->cols;
	img->rows = image->rows;
	img->image = (Color **)malloc(image->rows * sizeof(Color *));

	if(img->image == NULL){
		printf("Memory allocation failed.\n");
		free(img);
        return NULL;
	}

	for(uint32_t i = 0; i < img->rows; i++){
		img->image[i] = (Color *)malloc(img->cols * sizeof(Color));
		if (img->image[i] == NULL) {
            printf("Memory allocation failed.\n");
            for (uint32_t j = 0; j < i; j++) {
                free(img->image[j]);
            }
            free(img->image);
            free(img);
            return NULL;
        }
	}

	for (uint32_t i = 0; i < image->rows; i++) {
        for (uint32_t j = 0; j < image->cols; j++) {
            Color originalColor = image->image[i][j];
            Color *newColor = &img->image[i][j];
            
            // 提取 B 通道的 LSB
            if (originalColor.B & 1) {
                // 如果 LSB 是 1，设置新像素为白色
                newColor->R = 255;
                newColor->G = 255;
                newColor->B = 255;
            } else {
                // 如果 LSB 是 0，设置新像素为黑色
                newColor->R = 0;
                newColor->G = 0;
                newColor->B = 0;
            }
        }
    }

    return img;
}

void errorExit(const char *message){
	fprintf(stderr, "%s\n", message);
	exit(-1);
}

void printPixel(uint8_t b) {
    if (b & 1) {
        printf(" ");
    } else {
        printf("#");
    }
}

/*
Loads a file of ppm P3 format from a file, and prints to stdout (e.g. with printf) a new image, 
where each pixel is black if the LSB of the B channel is 0, 
and white if the LSB of the B channel is 1.

argc stores the number of arguments.
argv stores a list of arguments. Here is the expected input:
argv[0] will store the name of the program (this happens automatically).
argv[1] should contain a filename, containing a file of ppm P3 format (not necessarily with .ppm file extension).
If the input is not correct, a malloc fails, or any other error occurs, you should exit with code -1.
Otherwise, you should return from main with code 0.
Make sure to free all memory before returning!
*/
int main(int argc, char **argv)
{
	//YOUR CODE HERE
	if(argc != 2){
		errorExit("Usage: <program> <filename>.");
	}

	FILE *file = fopen(argv[1], "r");
	if(file == NULL){
		errorExit("Error opening file.");
	}

	char format[3];
	int width, height, maxValue;
	if(fscanf(file, "%2s", format) != 1 || format[0] != 'P' || format[1] != '3'){
		errorExit("Unsupported file format or corrupted file");
	}
	if (fscanf(file, "%d %d %d", &width, &height, &maxValue) != 3) {
        errorExit("Error reading image dimensions or max color value");
    }
    if (maxValue != 255) {
        errorExit("Unsupported max color value");
    }

	for (int i = 0; i < width * height; i++) {
        int r, g, b;
        if (fscanf(file, "%d %d %d", &r, &g, &b) != 3) {
            errorExit("Error reading pixel data");
        }
        printPixel(b);
        
        if ((i + 1) % width == 0) {
            printf("\n");
        }
    }
}


