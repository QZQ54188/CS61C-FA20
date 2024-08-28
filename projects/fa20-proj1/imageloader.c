/************************************************************************
**
** NAME:        imageloader.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**              Justin Yokota - Starter Code
**				YOUR NAME HERE
**
**
** DATE:        2020-08-15
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include "imageloader.h"

//Opens a .ppm P3 image file, and constructs an Image object. 
//You may find the function fscanf useful.
//Make sure that you close the file with fclose before returning.
Image *readData(char *filename) 
{
	//YOUR CODE HERE
	FILE *fp = fopen(filename, "r");
	if(fp == NULL){
		printf("The entered file name does not exist.\n");
		return NULL;
	}

	char format[3];
	fscanf(fp, "%2s", format);
	if(strcmp(format, "P3") != 0){
		printf("Invalidate file format.\n");
		fclose(fp);
		return NULL;
	}

	//Allocate image memory first and then read the file for exception safety
	Image *img = (Image *)malloc(sizeof(Image));
	if(img == NULL){
		printf("Memory allocation failed.\n");
		fclose(fp);
		return NULL;
	}

	int maxValue;
	fscanf(fp, "%u %u", &(img->cols), &(img->rows));
	fscanf(fp, "%d", &maxValue);

	img->image = (Color **)malloc(img->rows * sizeof(Color *));
	if(img->image == NULL){
		printf("Memory allocation failed.\n");
		fclose(fp);
		return NULL;
	}

	for(uint32_t i = 0; i < img->rows; i++){
		img->image[i] = (Color *)malloc(img->cols * sizeof(Color));

		if(img->image[i] == NULL){
			printf("Memory allocation failed.\n");
			for(uint32_t j = 0; j < i; j++){
				free(img->image[j]);
			}
			free(img->image);
			free(img);
			fclose(fp);
			return NULL;
		}

		for(uint32_t j = 0; j < img->cols; j++){
			int tempR, tempG, tempB;
			fscanf(fp, "%d %d %d", &tempR, &tempG, &tempB);
			img->image[i][j].R = (uint8_t)tempR;
			img->image[i][j].G = (uint8_t)tempG;
			img->image[i][j].B = (uint8_t)tempB;
		}

	}

	fclose(fp);
	return img;
}

//Given an image, prints to stdout (e.g. with printf) a .ppm P3 file with the image's data.
void writeData(Image *image)
{
	//YOUR CODE HERE
	if(image == NULL){
		printf("The input image cannot be NULL.\n");
		return;
	}

	printf("P3\n");
	printf("%u %u\n", image->cols, image->rows);
	printf("255\n");

	for(uint32_t i = 0; i < image->rows; i++){
		for(uint32_t j = 0; j < image->cols; j++){
			unsigned int R = image->image[i][j].R;
			unsigned int G = image->image[i][j].G;
			unsigned int B = image->image[i][j].B;
			printFormatted(R);
			printFormatted(G);
			printFormatted(B);
			printf("  ");
		}
		printf("\n");
	}
}

void printFormatted(unsigned int num) {
    if (num >= 100) {
        printf("%-3u ", num);
    } else {
        printf("%3u ", num);
    }
}

//Frees an image
void freeImage(Image *image)
{
	//YOUR CODE HERE
	if(image == NULL){
		return;
	}

	for(uint32_t i = 0; i < image->rows; i++){
		free(image->image[i]);
	}
	free(image->image);
	free(image);
}