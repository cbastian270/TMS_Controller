import config_1 as config
import RPi.GPIO as GPIO
import time


ScanMode = 0                                    


# gain channel
ADS1256_GAIN_E = {'ADS1256_GAIN_1' : 0, # GAIN   1
                  'ADS1256_GAIN_2' : 1,	# GAIN   2
                  'ADS1256_GAIN_4' : 2,	# GAIN   4
                  'ADS1256_GAIN_8' : 3,	# GAIN   8
                  'ADS1256_GAIN_16' : 4,# GAIN  16
                  'ADS1256_GAIN_32' : 5,# GAIN  32
                  'ADS1256_GAIN_64' : 6,# GAIN  64
                 }

# data rate
ADS1256_DRATE_E = {'ADS1256_30000SPS' : 0xF0, # reset the default values
                   'ADS1256_15000SPS' : 0xE0,
                   'ADS1256_7500SPS' : 0xD0,
                   'ADS1256_3750SPS' : 0xC0,
                   'ADS1256_2000SPS' : 0xB0,
                   'ADS1256_1000SPS' : 0xA1,
                   'ADS1256_500SPS' : 0x92,
                   'ADS1256_100SPS' : 0x82,
                   'ADS1256_60SPS' : 0x72,
                   'ADS1256_50SPS' : 0x63,
                   'ADS1256_30SPS' : 0x53,
                   'ADS1256_25SPS' : 0x43,
                   'ADS1256_15SPS' : 0x33,
                   'ADS1256_10SPS' : 0x20,
                   'ADS1256_5SPS' : 0x13,
                   'ADS1256_2d5SPS' : 0x03
                  }

# registration definition
REG_E = {'REG_STATUS': 0,  # x1H
         'REG_MUX'   : 1,  # 01H
         'REG_ADCON' : 2,  # 20H
         'REG_DRATE' : 3,  # F0H
         'REG_IO'    : 4,  # E0H
         'REG_OFC0'  : 5,  # xxH
         'REG_OFC1'  : 6,  # xxH
         'REG_OFC2'  : 7,  # xxH
         'REG_FSC0'  : 8,  # xxH
         'REG_FSC1'  : 9,  # xxH
         'REG_FSC2'  : 10, # xxH
        }

# command definition
CMD = {'CMD_WAKEUP' : 0x00,     # Completes SYNC and Exits Standby Mode 0000  0000 (00h)
       'CMD_RDATA' : 0x01,      # Read Data 0000  0001 (01h)
       'CMD_RDATAC' : 0x03,     # Read Data Continuously 0000   0011 (03h)
       'CMD_SDATAC' : 0x0F,     # Stop Read Data Continuously 0000   1111 (0Fh)
       'CMD_RREG' : 0x10,       # Read from REG rrr 0001 rrrr (1xh)
       'CMD_WREG' : 0x50,       # Write to REG rrr 0101 rrrr (5xh)
       'CMD_SELFCAL' : 0xF0,    # Offset and Gain Self-Calibration 1111    0000 (F0h)
       'CMD_SELFOCAL' : 0xF1,   # Offset Self-Calibration 1111    0001 (F1h)
       'CMD_SELFGCAL' : 0xF2,   # Gain Self-Calibration 1111    0010 (F2h)
       'CMD_SYSOCAL' : 0xF3,    # System Offset Calibration 1111   0011 (F3h)
       'CMD_SYSGCAL' : 0xF4,    # System Gain Calibration 1111    0100 (F4h)
       'CMD_SYNC' : 0xFC,       # Synchronize the A/D Conversion 1111   1100 (FCh)
       'CMD_STANDBY' : 0xFD,    # Begin Standby Mode 1111   1101 (FDh)
       'CMD_RESET' : 0xFE,      # Reset to Power-Up Values 1111   1110 (FEh)
      }
      


class ADS1256:
        
        
    def __init__(self):        
        self.rst_pin = config.RST_PIN
        self.cs_pin = config.CS_PIN
        self.drdy_pin = config.DRDY_PIN   
                
         
    # Hardware reset
    def ADS1256_reset(self):
        config.digital_write(self.rst_pin, GPIO.HIGH)
        #config.delay_ms(200)
        config.digital_write(self.rst_pin, GPIO.LOW)
        #config.delay_ms(200)
        config.digital_write(self.rst_pin, GPIO.HIGH)
    
    def ADS1256_WriteCmd(self, reg):
        config.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        config.spi_writebyte([reg])
        config.digital_write(self.cs_pin, GPIO.HIGH)#cs 1
    
    def ADS1256_WriteReg(self, reg, data):
        config.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        config.spi_writebyte([CMD['CMD_WREG'] | reg, 0x00, data])
        config.digital_write(self.cs_pin, GPIO.HIGH)#cs 1
        
    def ADS1256_Read_data(self, reg):
        config.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        config.spi_writebyte([CMD['CMD_RREG'] | reg, 0x00])
        data = config.spi_readbytes(1)
        config.digital_write(self.cs_pin, GPIO.HIGH)#cs 1

        return data
        
    def ADS1256_WaitDRDY(self):
        for i in range(0,10000,1):
            if(config.digital_read(self.drdy_pin) == 0):
                
                break
        if(i >= 10000):
            print ("Time Out ...\r\n")
        
        
    def ADS1256_ReadChipID(self):
        self.ADS1256_WaitDRDY()
        id = self.ADS1256_Read_data(REG_E['REG_STATUS'])
        id = id[0] >> 4
        print ('ID:',id)  
        if id !=3:
            print("ADS connection error")
            raise Exception("ADS connection error")
        return id
        
    #The configuration parameters of ADC, gain and data rate
    def ADS1256_ConfigADC(self, gain, drate):
        self.ADS1256_WaitDRDY()
        buf = [0,0,0,0,0,0]
        buf[0] = (0<<3) | (1<<2) | (0<<1)
        buf[1] = 0x08
        buf[2] = (0<<5) | (0<<3) | (gain<<0)
        buf[3] = drate
        
        config.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        config.spi_writebyte([CMD['CMD_WREG'] | 0, 0x03])
        config.spi_writebyte(buf)
        
        config.digital_write(self.cs_pin, GPIO.HIGH)#cs 1
        #config.delay_ms(1) 



    def ADS1256_SetChannal(self, Channal):
        if Channal > 5:
            return 0
        self.ADS1256_WriteReg(REG_E['REG_MUX'], (Channal<<4) | (1<<3))

    def ADS1256_SetDiffChannal(self, Channal):
        if Channal == 0:
            self.ADS1256_WriteReg(REG_E['REG_MUX'], (0 << 4) | 1) 	#DiffChannal  AIN0-AIN1
        elif Channal == 1:
            self.ADS1256_WriteReg(REG_E['REG_MUX'], (2 << 4) | 3) 	#DiffChannal   AIN2-AIN3
        elif Channal == 2:
            self.ADS1256_WriteReg(REG_E['REG_MUX'], (4 << 4) | 5) 	#DiffChannal    AIN4-AIN5
        elif Channal == 3:
            self.ADS1256_WriteReg(REG_E['REG_MUX'], (6 << 4) | 7) 	#DiffChannal   AIN6-AIN7

    def ADS1256_SetMode(self, Mode):
        ScanMode = Mode

    def ADS1256_init(self):
        if (config.module_init() != 0):
            return -1
        self.ADS1256_reset()
        id = self.ADS1256_ReadChipID()
        if id == 3 :
            print("ID Read success  ")
        else:
            print("ID Read failed   ")
            return -1
        self.ADS1256_ConfigADC(ADS1256_GAIN_E['ADS1256_GAIN_1'], ADS1256_DRATE_E['ADS1256_30000SPS'])
        return 0
        
    def ADS1256_Read_ADC_Data(self):
        self.ADS1256_WaitDRDY()
        config.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        config.spi_writebyte([CMD['CMD_RDATA']])
        # config.delay_ms(10)

        buf = config.spi_readbytes(3)
        config.digital_write(self.cs_pin, GPIO.HIGH)#cs 1
        read = (buf[0]<<16) & 0xff0000
        read |= (buf[1]<<8) & 0xff00
        read |= (buf[2]) & 0xff
        if (read & 0x800000):
            read &= 0xF000000
        return read
 
    def ADS1256_GetAmountChannalValues(self, Channel, amount=1000):
        data_list = []
        data_string = ""
        
        counter = 0
        conversion_factor = 1675701.13                  # what is this conversion factor?
        intercept = 14386.52                            # is this a linear conversion?
        #print ("Start of GetChanVal")
        if(ScanMode == 0):# 0  Single-ended input  8 channel1 Differential input  4 channel 
            #print ("W")
            if(Channel>=7):                             # has 8 input channels, high limit
                return 0
            self.ADS1256_SetChannal(Channel)
            self.ADS1256_WriteCmd(CMD['CMD_SYNC'])      # synch connections
            #config.delay_ms(1)
            self.ADS1256_WriteCmd(CMD['CMD_WAKEUP'])    # wake up command 
            config.delay_ms(1)                          # delay for 1ms 
            #for _ in range(looop):
                #data_list.append(self.ADS1256_Read_ADC_Data())
            counter = 0
            while counter < amount:
                timestamp = time.time()
                value = ((self.ADS1256_Read_ADC_Data() - intercept) / conversion_factor)-2.5        # this is the diffrence from the line below normalize?
                counter += 1
                data_string += f"{Channel}, {timestamp}, {value}\n"
                counter += 1
        print (f"done with {Channel} with {counter} values")
        #print (data_string)
        return data_string #data_list
        
    def ADS1256_GetChannalValue(self, Channel, duration = 1):
        data_list = []
        data_string = ""
        start_time = time.time()
        counter = 0
        conversion_factor = 1675701.13                  # what is this conversion factor?
        intercept = 14386.52                            # is this a linear conversion?
        #print ("Start of GetChanVal")
        if(ScanMode == 0):# 0  Single-ended input  8 channel1 Differential input  4 channel 
            #print ("W")
            if(Channel>=7):                             # has 8 input channels, high limit
                return 0
            self.ADS1256_SetChannal(Channel)
            self.ADS1256_WriteCmd(CMD['CMD_SYNC'])      # synch connections
            #config.delay_ms(1)
            self.ADS1256_WriteCmd(CMD['CMD_WAKEUP'])    # wake up command 
            config.delay_ms(1)                          # delay for 1ms 
            #for _ in range(looop):
                #data_list.append(self.ADS1256_Read_ADC_Data())
            while time.time() - start_time < duration:
                timestamp = time.time()
                value = ((self.ADS1256_Read_ADC_Data() - intercept) / conversion_factor)-2.5        # this is the diffrence from the line below normalize?
                counter += 1
                data_string += f"{Channel}, {timestamp}, {value}\n"
      
        else:
            #print ("T")
            if(Channel>=4):
                return 0
            self.ADS1256_SetDiffChannal(Channel)
            self.ADS1256_WriteCmd(CMD['CMD_SYNC'])
            #config.delay_ms(10) 
            self.ADS1256_WriteCmd(CMD['CMD_WAKEUP'])
            config.delay_ms(1) 
            #for _ in range(looop):
                #data_list.append(self.ADS1256_Read_ADC_Data())
            while time.time() - start_time < duration:
                timestamp = time.time()
                value = (self.ADS1256_Read_ADC_Data() - intercept) / conversion_factor
                counter += 1
                data_string += f"{Channel}, {timestamp}, {value}\n"
        #print ("end of GetChannalValue")
        print (f"done with {Channel} with {counter} values")
        #print (data_string)
        return data_string #data_list
        
    def getchannal(self, channel):
        return self.ADS_GetChannalValue(channel)
        
    def ADS1256_GetAll(self):
        ADC_Value = ""
        #print ("start time: " + str(time.time()))
        #ADC_Value = [0,0,0,0,0,0,0,0]
        for i in range(1,7,1):
            #ADC_Value += self.ADS1256_GetChannalValue(i)
            ADC_Value += self.ADS1256_GetAmountChannalValues(i)
        #print ("end time: " + str(time.time()))
        return ADC_Value
        
    def getOne(self, channel):
        val = (self.ADS1256_GetChannalValue(channel))
       # return str(val * weird_val) + "," + str(time.time())+ "\n"
        return str(val) + "," + str(time.time())+ "\n"
        
    def getUpTo(self, channel_range):
        #print ("in getUpTo")
        if channel_range == 1:
            vals = [0]
            tims = [0]
        elif channel_range == 2:
            vals = [0,0]
            tims = [0,0]
        elif channel_range == 3:
            vals = [0,0,0]
            tims = [0,0,0]
        elif channel_range == 4:
            vals = [0,0,0,0]
            tims = [0,0,0,0]
        elif channel_range == 5:
            vals = [0,0,0,0,0]
            tims = [0,0,0,0,0]
        elif channel_range == 6:
            vals = [0,0,0,0,0,0]
            tims = [0,0,0,0,0,0]


            
        print (vals)
        print (tims)
        if channel_range == 1:
            vals[0] = self.getchannal(1) * 5.0/0x7fffff
            tims[0] = time.time()
            #print ("in if 1")
        else:
            for j in range(0, channel_range, 1):
                vals[j] = self.getchannal(j) * 5.0/0x7fffff
                tims[j] = time.time()
                #print ("in else")
        if channel_range == 1:
            retstring = str(vals[0]) + "," + str(tims[0]) + "\n"
        else:
            retstring = str(vals[1]) + "," + str(tims[1]) + "\n"
        print (len(vals))
        return retstring, vals#, tims
        
# test code to troubleshoot the configuration
    
#ADC = ADS1256()                 # setup instance 
#ADC.ADS1256_init()              # intiailize
#strt_time = time.time()         # set start time
#cur_time = strt_time            # set current time

#test = ADC.getOne(5)            # grab data from one
#print(test)                     # print data 

#test = ADC.ADS1256_GetAll()     # get all data 
#print(test)

# end of test code to trouble shoot the configuration


### END OF FILE ###

