#include <stdlib.h>     //exit()
#include <signal.h>     //signal()
#include <time.h>
#include "ADS1256.h"
#include "stdio.h"
#include <time.h>
#include <string.h>
#include <sys/timeb.h>

#define size 20000     // The amount of data to collect

void  Handler(int signal)
{
    //System Exit
    printf("\r\nEND                  \r\n");
    DEV_ModuleExit();

    exit(0);
}


UDOUBLE ADC_read()
{
    UDOUBLE read = 0;
    UBYTE buf[3] = {0,0,0};
    
    while(DEV_Digital_Read(DEV_DRDY_PIN) == 0);
    while(DEV_Digital_Read(DEV_DRDY_PIN) == 1);
    
    buf[0] = DEV_SPI_ReadByte();
    buf[1] = DEV_SPI_ReadByte();
    buf[2] = DEV_SPI_ReadByte();
    
    read = ((UDOUBLE)buf[0] << 16) & 0x00FF0000;
    read |= ((UDOUBLE)buf[1] << 8);  /* Pay attention to It is wrong   read |= (buf[1] << 8) */
    read |= buf[2];
    if (read & 0x800000)
        read &= 0xFF000000;

    return read;
} 


int main(void)
{
    UDOUBLE i;
    float a[size];
    FILE *fp;
    fp = fopen("output.txt", "w"); // open-file

    if (fp == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    fprintf(fp, "Data data collected by the ADC\n"); // Output to a file


    printf("demo\r\n");
    DEV_ModuleInit();
    
    // Exception handling:ctrl + c
    signal(SIGINT, Handler);

    if(ADS1256_init() == 1){
        printf("\r\nEND                  \r\n");
        DEV_ModuleExit();
        exit(0);
    }

    printf("Data acquisition configuration\r\n");

    ADS1256_SetChannal(0);
    ADS1256_WriteCmd(CMD_SYNC);
    ADS1256_WriteCmd(CMD_WAKEUP);
    ADS1256_WaitDRDY();
    DEV_Delay_ms(1);

    printf("Start collecting data\r\n");

    DEV_Digital_Write(DEV_CS_PIN, 0);
    DEV_SPI_WriteByte(CMD_RDATAC);
    DEV_Delay_ms(1);

    struct timespec start={0,0}, finish={0,0}; 
    clock_gettime(CLOCK_REALTIME,&start);

    for (i = 0; i < size ; i++)
    {
        a[i] = ADC_read()*5.0/0x7fffff;
        /* code */
    }
    
    clock_gettime(CLOCK_REALTIME,&finish);
    printf("The time to collect the data is : %ld S (Take the positive down)\r\n",finish.tv_sec-start.tv_sec);
    DEV_Digital_Write(DEV_CS_PIN, 1);

    printf("Data collection completed\r\n");

    printf("Output the collected data to a document\r\n");
    for (i = 0; i < size ; i++)
    {
        fprintf(fp, "%f\r\n", a[i]);
        /* code */
    }

    fclose(fp); // closed file
    return 0;
}
