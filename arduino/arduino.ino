/*
 Circuit:

 DRDY: pin 6
 CSB: pin 7
 MOSI: pin 11
 MISO: pin 12
 SCK: pin 13

 created 31 July 2010
 modified 14 August 2010
 by Tom Igoe
 */

// the sensor communicates using SPI, so include the library:
#include <SPI.h>



// pins used for the connection with the sensor
// the other you need are controlled by the SPI library):
const int shdn = 2;             //shutdown active low
const int rel1 = 3;             //choose mode: 1: both VADJ0 and VADJ1 are connected to bank 45V
                                // 0: VADJ0 <-> P45V0 VAJD0, VADJ1 <-> P18V0_VADJ0
const int rel0 = 4;             // choose voltage source - 0: VADJ0 VADJ1, 1: picoameter
const int data_in = 5;          // ASIC data input
const int data_rdy = 6;         // ASIC output to indicate that next clk rising edge will probe last bit. After that another 
                                // rising edge is expected to save input buffer to internal register
const int spi_cs = 7;           // CS of SPI to ASIC (not used)
const int clk = 13;             // CLK - common for data_in and SPI. Here is used only as simple output to control data_in 

void setup() {
  Serial.begin(9600);

  // initialize the  data ready and chip select pins:
  pinMode(data_in, INPUT);
  pinMode(shdn, OUTPUT);
  pinMode(rel1, OUTPUT);
  pinMode(rel0, OUTPUT);
  pinMode(data_in, OUTPUT);
  pinMode(spi_cs, OUTPUT);
  pinMode(clk, OUTPUT);

  // TODO init ASIC register with zeros?

  // give the time to set up:
  delay(100);
  digitalWrite(data_in, LOW);
  digitalWrite(clk, LOW);
}

int get_data() {
    while (not Serial.available())
    {
        /* code */
    }
    return (Serial.read());
}

void loop() {
    uint32_t asic_buffer = 0;
    int uart_buffer = 0;
    
    uart_buffer = get_data();
    
    if (uart_buffer == 0xAB){   // magic word
        uart_buffer = get_data();
        if (uart_buffer == 1)   // update ASIC register
        {
            for (size_t i = 0; i < 4; i++)
            {
                uart_buffer = get_data();
                asic_buffer = (asic_buffer << 8) | uart_buffer;
            }
            update_asic(asic_buffer);
        } 
        else if (uart_buffer == 2) // update ios
        {
            uart_buffer = get_data();
            digitalWrite( (uart_buffer & 0xF0) >> 4, uart_buffer & 0xF);
            Serial.println("OUTPUT: " + String((uart_buffer & 0xF0)>> 4) + " set to " + String(uart_buffer & 0xF));
        } 
        else
        {
            Serial.println("Error: command not recognized " + String(uart_buffer));
        }
    } else {
        Serial.println("Error: magic word not recognized " + String(uart_buffer));
    }
}

void update_asic(uint32_t asic_buffer) {
    for (size_t i = 0; i < 32; i++)
    {
        // DRIVE DATA BIT
        if ((asic_buffer & (1 << (31-i))) == 0)
        {
            digitalWrite(data_in, LOW);
        } else {
            digitalWrite(data_in, HIGH);
        }
        // RISING EDGE
        digitalWrite(clk, HIGH);
        delayMicroseconds(10);
        // FALLING EDGE
        digitalWrite(clk, LOW);
        if (i == 29){
            if (digitalRead(data_rdy) == LOW)
            {
                Serial.println("\tERROR: DATA READY not detected for data " + String(asic_buffer));
            }
            
        }
        
    }
}