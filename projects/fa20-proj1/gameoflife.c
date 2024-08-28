/************************************************************************
**
** NAME:        gameoflife.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Justin Yokota - Starter Code
**				YOUR NAME HERE
**
**
** DATE:        2020-08-23
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "imageloader.h"

//Determines what color the cell at the given row/col should be. This function allocates space for a new Color.
//Note that you will need to read the eight neighbors of the cell in question. The grid "wraps", so we treat the top row as adjacent to the bottom row
//and the left column as adjacent to the right column.
Color *evaluateOneCell(Image *image, int row, int col, uint32_t rule)
{
	//YOUR CODE HERE
	int rows = image->rows;
	int cols = image->cols;

	int dirX[] = {-1, -1, -1, 0, 0, 1, 1, 1};
	int dirY[] = {-1, 0, 1, -1, 1, -1, 0, 1};

	int neighbors = 0;
	for(int i = 0; i < 8; i++){
		int neighborX = (row + dirX[i] + rows) % rows;
		int neighborY = (col + dirY[i] + cols) % cols;

		Color *neighborColor = &(image->image[neighborX][neighborY]);
		if(neighborColor->R || neighborColor->G || neighborColor->B){
			neighbors++;
		}
	}

	Color *curColor = &(image->image[row][col]);
	int isLive = curColor->B || curColor->G || curColor->R;

	Color *newColor = (Color *)malloc(sizeof(Color));
	if(newColor == NULL){
		return NULL;
	}

	if(isLive &&(neighbors < 2 || neighbors > 3)){
		newColor->R = 0;
		newColor->G = 0;
		newColor->B = 0;
	}else if(!isLive && neighbors == 3){
		newColor->R = 255;
		newColor->G = 255;
		newColor->B = 255;
	}else{
		newColor->R = curColor->R;
		newColor->G = curColor->G;
		newColor->B = curColor->B;
	}

	return newColor;
}

//The main body of Life; given an image and a rule, computes one iteration of the Game of Life.
//You should be able to copy most of this from steganography.c
Image *life(Image *image, uint32_t rule)
{
	//YOUR CODE HERE
	Image *img = (Image *)malloc(sizeof(Image));
	if(img == NULL){
		return NULL;
	}

	img->rows = image->rows;
	img->cols = image->cols;

	img->image = (Color **)malloc(img->rows * sizeof(Color *));
	if(img->image == NULL){
		free(img);
		return NULL;
	}

	for(uint32_t i = 0; i < img->rows; i++){
		img->image[i] = (Color *)malloc(img->cols * sizeof(Color));
		if (img->image[i] == NULL) {
            // Free previously allocated rows in case of failure
            for (uint32_t j = 0; j < i; j++) {
                free(img->image[j]);
            }
            free(img->image);
            free(img);
            return NULL; // Handle allocation failure
        }
	}

	for(uint32_t row = 0; row < image->rows; row++){
		for(uint32_t col = 0; col < image->cols; col++){
			Color *newColor = evaluateOneCell(image, row, col, rule);
			if (newColor == NULL) {
                // Free the new image in case of failure
                for (uint32_t i = 0; i < img->rows; i++) {
                    free(img->image[i]);
                }
                free(img->image);
                free(img);
                return NULL; // Handle allocation failure
            }

			img->image[row][col] = *newColor;
			free(newColor);
		}
	}

	return img;
}

/*
Loads a .ppm from a file, computes the next iteration of the game of life, then prints to stdout the new image.

argc stores the number of arguments.
argv stores a list of arguments. Here is the expected input:
argv[0] will store the name of the program (this happens automatically).
argv[1] should contain a filename, containing a .ppm.
argv[2] should contain a hexadecimal number (such as 0x1808). Note that this will be a string.
You may find the function strtol useful for this conversion.
If the input is not correct, a malloc fails, or any other error occurs, you should exit with code -1.
Otherwise, you should return from main with code 0.
Make sure to free all memory before returning!

You may find it useful to copy the code from steganography.c, to start.
*/
int main(int argc, char **argv)
{
	//YOUR CODE HERE
	if (argc != 3) {
        fprintf(stderr, "Usage: %s <filename.ppm> <rule in hexadecimal>\n", argv[0]);
        return -1;
    }

	Image *image = readData(argv[1]);
	if (image == NULL) {
        fprintf(stderr, "Error: Could not read image from file %s\n", argv[1]);
        return -1;
    }

	char *endptr;
    uint32_t rule = (uint32_t)strtol(argv[2], &endptr, 16);
    if (*endptr != '\0') {
        fprintf(stderr, "Error: Invalid hexadecimal number %s\n", argv[2]);
        freeImage(image);
        return -1;
    }

	Image *newImage = life(image, rule);
    if (newImage == NULL) {
        fprintf(stderr, "Error: Could not compute the next generation of the game of life\n");
        freeImage(image);
        return -1;
    }

	writeImage(newImage);
	freeImage(image);
	freeImage(newImage);

	return 0;
}
