/**
 ******************************************************************************
 * @file    LTC4162.h
 * @author  Carlos Martinez Mora (carmamo.95@gmail.com)
 * @date	 Sep 25, 2023
 * @brief   short description of the file
 *			...
 *
 ******************************************************************************
 * @attention
 *
 *
 *
 ******************************************************************************
 */
#ifndef INC_LTC4162_H_
#define INC_LTC4162_H_

#include "stm32l4xx_hal.h"


typedef struct {

	/* I2C handle */
	I2C_HandleTypeDef	*i2cHandle;

} LTC4162_t;


void LTC4162_Init(I2C_HandleTypeDef *i2c);

HAL_StatusTypeDef LTC4162_SetReg(uint16_t reg, uint16_t data);

HAL_StatusTypeDef LTC4162_GetReg(uint16_t reg, uint16_t *rxdata);

HAL_StatusTypeDef LTC4162_GetTelemetry();



#endif /* INC_LTC4162_H_ */
