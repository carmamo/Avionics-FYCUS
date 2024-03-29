/**
 ******************************************************************************
 * @file    EPS_FYCUS.h
 * @author  Carlos Martinez Mora (carmamo.95@gmail.com)
 * @date	 Sep 21, 2023
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
#ifndef INC_EPS_FYCUS_H_
#define INC_EPS_FYCUS_H_

#ifdef __cplusplus
extern "C" {
#endif

#include "stm32l4xx_hal.h"
#include <stdbool.h>

/*
 * DEFINES
 */


/*
 * VARIABLES
 */


/*
 * TYPEDEF STRUCTS
 */


typedef struct
{
	uint16_t v_in;
	uint16_t v_out;
	uint16_t v_bat;
	uint16_t i_bat;
	uint16_t i_in;
	uint16_t uC_temp;
	uint16_t die_temp;
	uint16_t thermistor_voltage;
	uint16_t bsr;
	uint16_t charger_state;
} EPS_Telemetry;

/*
 * FUNCTION PROTOTYPES
 */

void send_telemetry();

void get_temperature();

void get_array_voltage();


/*
 * INITIALIZE
 */


/*
 * LOW-LEVEL OLED FUNCTIONS
 */


/*
 * MATH FUNCTIONS
 */

uint32_t map(uint32_t au32_IN, uint32_t au32_INmin, uint32_t au32_INmax, uint32_t au32_OUTmin, uint32_t au32_OUTmax);


/*
 * LOW-LEVEL FUNCTIONS
 */

void send_uart(char *string);



#ifdef __cplusplus
}
#endif


#endif /* INC_EPS_FYCUS_H_ */
