import config
import RPi.GPIO as GPIO
import time

ScanMode = 0

# Gain channel
ADS1256_GAIN_E = {'ADS1256_GAIN_1': 0,
                  'ADS1256_GAIN_2': 1,
                  'ADS1256_GAIN_4': 2,
                  'ADS1256_GAIN_8': 3,
                  'ADS1256_GAIN_16': 4,
                  'ADS1256_GAIN_32': 5,
                  'ADS1256_GAIN_64': 6}

# Data rate
ADS1256_DRATE_E = {'ADS1256_30000SPS': 0xF0,
                   'ADS1256_15000SPS': 0xE0,
                   'ADS1256_7500SPS': 0xD0,
                   'ADS1256_3750SPS': 0xC0,
                   'ADS1256_2000SPS': 0xB0,
                   'ADS1256_1000SPS': 0xA1,
                   'ADS1256_500SPS': 0x92,
                   'ADS1256_100SPS': 0x82,
                   'ADS1256_60SPS': 0x72,
                   'ADS1256_50SPS': 0x63,
                   'ADS1256_30SPS': 0x53,
                   'ADS1256_25SPS': 0x43,
                   'ADS1256_15SPS': 0x33,
                   'ADS1256_10SPS': 0x20,
                   'ADS1256_5SPS': 0x13,
                   'ADS1256_2d5SPS': 0x03}

# Register definition
REG_E = {'REG_STATUS': 0,
         'REG_MUX': 1,
         'REG_ADCON': 2,
         'REG_DRATE': 3,
         'REG_IO': 4,
         'REG_OFC0': 5,
         'REG_OFC1': 6,
         'REG_OFC2': 7,
         'REG_FSC0': 8,
         'REG_FSC1': 9,
         'REG_FSC2': 10}

# Command definition
CMD = {'CMD_WAKEUP': 0x00,
       'CMD_RDATA': 0x01,
       'CMD_RDATAC': 0x03,
       'CMD_SDATAC': 0x0F,
       'CMD_RREG': 0x10,
       'CMD_WREG': 0x50,
       'CMD_SELFCAL': 0xF0,
       'CMD_SELFOCAL': 0xF1,
       'CMD_SELFGCAL': 0xF2,
       'CMD_SYSOCAL': 0xF3,
       'CMD_SYSGCAL': 0xF4,
       'CMD_SYNC': 0xFC,
       'CMD_STANDBY': 0xFD,
       'CMD_RESET': 0xFE}


class ADS1256:
    
    def __init__(self):
        self.rst_pin0 = config.RST_PIN0
        self.cs_pin0 = config.CS_PIN0
        self.drdy_pin0 = config.DRDY_PIN0
        self.rst_pin1 = config.RST_PIN1
        self.cs_pin1 = config.CS_PIN1
        self.drdy_pin1 = config.DRDY_PIN1

    def ADS1256_reset0(self):
        config.digital_write(self.rst_pin0, GPIO.HIGH)
        config.delay_ms(20)
        config.digital_write(self.rst_pin0, GPIO.LOW)
        config.delay_ms(20)
        config.digital_write(self.rst_pin0, GPIO.HIGH)
    
    def ADS1256_reset1(self):
        config.digital_write(self.rst_pin1, GPIO.HIGH)
        config.delay_ms(20)
        config.digital_write(self.rst_pin1, GPIO.LOW)
        config.delay_ms(20)
        config.digital_write(self.rst_pin1, GPIO.HIGH)

    def ADS1256_WriteCmd0(self, reg):
        config.digital_write(self.cs_pin0, GPIO.LOW)#cs  0
        self.write_cmd0(self.cs_pin0, reg)
        config.digital_write(self.cs_pin0, GPIO.HIGH)#cs 1
        
    def ADS1256_WriteCmd1(self, reg):
        config.digital_write(self.cs_pin0, GPIO.LOW)#cs  0
        self.write_cmd1(self.cs_pin1, reg)
        config.digital_write(self.cs_pin1, GPIO.HIGH)#cs 1

    def write_cmd0(self, cs_pin, reg):
        print('Here E7A')
        config.digital_write(self.cs_pin0, GPIO.LOW)
        config.spi_writebyte0([reg])
        config.digital_write(self.cs_pin0, GPIO.HIGH)
        
    def write_cmd1(self, cs_pin, reg):
        config.digital_write(self.cs_pin1, GPIO.LOW)
        config.spi_writebyte1([reg])
        config.digital_write(self.cs_pin1, GPIO.HIGH)

    def ADS1256_WriteReg0(self, reg, data):
        config.digital_write(self.cs_pin0, GPIO.LOW)#cs  0
        self.write_reg0(self.cs_pin0, reg, data)
        config.digital_write(self.cs_pin0, GPIO.HIGH)#cs 1
        
    def ADS1256_WriteReg1(self, reg, data):
        config.digital_write(self.cs_pin1, GPIO.LOW)#cs  0
        self.write_reg1(self.cs_pin1, reg, data)
        config.digital_write(self.cs_pin1, GPIO.HIGH)#cs 1

    def write_reg0(self, cs_pin, reg, data):
        config.digital_write(cs_pin0, GPIO.LOW)
        config.spi_writebyte0([CMD['CMD_WREG'] | reg, 0x00, data])
        config.digital_write(cs_pin0, GPIO.HIGH)
        
    def write_reg1(self, cs_pin, reg, data):
        config.digital_write(cs_pin1, GPIO.LOW)
        config.spi_writebyte1([CMD['CMD_WREG'] | reg, 0x00, data])
        config.digital_write(cs_pin1, GPIO.HIGH)

    def ADS1256_Read_data0(self, reg):
        config.digital_write(self.cs_pin0, GPIO.LOW)#cs  0
        print('Here C2A')
        config.spi_writebyte0([CMD['CMD_RREG'] | reg, 0x00])
        data = config.spi_readbytes0(1)
        config.digital_write(self.cs_pin0, GPIO.HIGH)#cs 1
        
        return data
        
    def ADS1256_Read_data1(self, reg):
        config.digital_write(self.cs_pin1, GPIO.LOW)#cs  0
        config.spi_writebyte1([CMD['CMD_RREG'] | reg, 0x00])
        data = config.spi_readbytes1(1)
        config.digital_write(self.cs_pin1, GPIO.HIGH)#cs 1
        
        return data       

    def read_data0(self, reg):
        config.digital_write(self.cs_pin0, GPIO.LOW)
        print('Here C2A1')
        config.spi_writebyte0([CMD['CMD_RREG'] | reg, 0x00])
        print('Here C2A2')
        data = config.spi_readbytes0(1)
        print('Here C2A3')
        config.digital_write(self.cs_pin0, GPIO.HIGH)
        print('Here C2A4', data)
        return data
        
    def read_data1(self, reg):
        print('Here C2A1')
        config.digital_write(self.cs_pin1, GPIO.LOW)
        print('Here C2A2')
        config.spi_writebyte1([CMD['CMD_RREG'] | reg, 0x00])
        print('Here C2A3')
        data = config.spi_readbytes1(1)
        print('Here C2A4', data)
        config.digital_write(self.cs_pin1, GPIO.HIGH)
        return data

    def ADS1256_WaitDRDY0(self):
        for i in range(0, 10000, 1):
            if config.digital_read(self.drdy_pin0) == 0:
                break
        if i >= 10000:
            print("Time Out ...\r\n")
            
    def ADS1256_WaitDRDY1(self):
        for i in range(0, 10000, 1):
            if config.digital_read(self.drdy_pin1) == 0:
                break
        if i >= 10000:
            print("Time Out ...\r\n")

    def ADS1256_ReadChipID0(self):
        print('Here C1')
        self.ADS1256_WaitDRDY0()
        print('Here C2')
        id = self.ADS1256_Read_data0(REG_E['REG_STATUS'])
        print('Here C3, ID', id)
        id = id[0] >> 4
        print('Here C4, ID', id)
        return id

    def ADS1256_ReadChipID1(self):
        print('Here C1')
        self.ADS1256_WaitDRDY1()
        print('Here C2')
        id = self.ADS1256_Read_data1(REG_E['REG_STATUS'])
        print('Here C3, ID', id)
        id = id[0] >> 4
        print('Here C4, ID', id)
        return id

    def ADS1256_ConfigADC0(self, gain, drate):
        print('Here E1')
        self.ADS1256_WaitDRDY0()
        print('Here E2')
        buf = [0, 0, 0, 0, 0, 0, 0, 0]
        print('Here E3')
        buf[0] = (0 << 3) | (1 << 2) | (0 << 1)
        print('Here E4')
        buf[1] = 0x08
        print('Here E5')
        buf[2] = (0 << 5) | (0 << 3) | (gain << 0)
        print('Here E6')
        buf[3] = drate
        print('Here E7')
        self.write_cmd0(self.cs_pin0, CMD['CMD_WREG'] | 0)
        print('Here E8')
        config.spi_writebyte0([0x03])
        print('Here E9')
        config.spi_writebyte0(buf)
        print('Here E10')
        
    def ADS1256_ConfigADC1(self, gain, drate):
        self.ADS1256_WaitDRDY1()
        buf = [0, 0, 0, 0, 0, 0, 0, 0]
        buf[0] = (0 << 3) | (1 << 2) | (0 << 1)
        buf[1] = 0x08
        buf[2] = (0 << 5) | (0 << 3) | (gain << 0)
        buf[3] = drate

        self.write_cmd1(self.cs_pin1, CMD['CMD_WREG'] | 0)
        config.spi_writebyte1([0x03])
        config.spi_writebyte1(buf)   
        
    def ADS1256_SetChannal0(self, Channel):
        if Channel > 7:
            return 0
        self.ADS1256_WriteReg0(REG_E['REG_MUX'], (Channel << 4) | (1 << 3))
        
    def ADS1256_SetChannal1(self, Channel):
        if Channel > 7:
            return 0
        self.ADS1256_WriteReg1(REG_E['REG_MUX'], (Channel << 4) | (1 << 3))

    def ADS1256_SetDiffChannal0(self, Channel):
        if Channel == 0:
            self.ADS1256_WriteReg0(REG_E['REG_MUX'], (0 << 4) | 1)  # DiffChannal  AIN0-AIN1
        elif Channel == 1:
            self.ADS1256_WriteReg0(REG_E['REG_MUX'], (2 << 4) | 3)  # DiffChannal   AIN2-AIN3
        elif Channel == 2:
            self.ADS1256_WriteReg0(REG_E['REG_MUX'], (4 << 4) | 5)  # DiffChannal    AIN4-AIN5
        elif Channel == 3:
            self.ADS1256_WriteReg0(REG_E['REG_MUX'], (6 << 4) | 7)  # DiffChannal   AIN6-AIN7

    def ADS1256_SetDiffChannal(self, Channel):
        if Channel == 0:
            self.ADS1256_WriteReg1(REG_E['REG_MUX'], (0 << 4) | 1)  # DiffChannal  AIN0-AIN1
        elif Channel == 1:
            self.ADS1256_WriteReg1(REG_E['REG_MUX'], (2 << 4) | 3)  # DiffChannal   AIN2-AIN3
        elif Channel == 2:
            self.ADS1256_WriteReg1(REG_E['REG_MUX'], (4 << 4) | 5)  # DiffChannal    AIN4-AIN5
        elif Channel == 3:
            self.ADS1256_WriteReg1(REG_E['REG_MUX'], (6 << 4) | 7)  # DiffChannal   AIN6-AIN7

    def ADS1256_SetMode(self, Mode):
        global ScanMode
        ScanMode = Mode

    def ADS1256_init0(self):
        print('Here A')
        if config.module_init() != 0:
            return -1
        print('Here B')
        self.ADS1256_reset0()
        print('Here C')
        id = self.ADS1256_ReadChipID0()
        print('Here D')
        if id == 3:
            print("ID Read success  ")
        else:
            print("ID Read failed   ")
            return -1
        print('Here E')
        self.ADS1256_ConfigADC0(ADS1256_GAIN_E['ADS1256_GAIN_1'], ADS1256_DRATE_E['ADS1256_30000SPS'])
        print('Here F')
        return 0

    def ADS1256_init1(self):  
        print('Here A')
        if config.module_init() != 0:
            return -1
        print('Here B')
        self.ADS1256_reset1()      
        print('Here C')
        id = self.ADS1256_ReadChipID1()
        print('Here D')
        if id == 6:
            print("ID Read success  ")
        else:
            print("ID Read failed   ")
            return -1
        print('Here E')
        self.ADS1256_ConfigADC1(ADS1256_GAIN_E['ADS1256_GAIN_1'], ADS1256_DRATE_E['ADS1256_30000SPS'])
        print('Here F')
        return 0

    def ADS1256_Read_ADC_Data0(self):
        self.ADS1256_WaitDRDY0()
        return self.read_adc_data0(self.cs_pin0)

    def ADS1256_Read_ADC_Data1(self):
        self.ADS1256_WaitDRDY1()
        return self.read_adc_data1(self.cs_pin1)

    def read_adc_data0(self, cs_pin):
        config.digital_write(cs_pin0, GPIO.LOW)
        config.spi_writebyte0([CMD['CMD_RDATA']])
        buf = config.spi_readbytes0(3)
        config.digital_write(cs_pin0, GPIO.HIGH)
        read = (buf[0] << 16) & 0xff0000
        read |= (buf[1] << 8) & 0xff00
        read |= (buf[2]) & 0xff
        if read & 0x800000:
            read &= 0xF000000
        return read
        
    def read_adc_data1(self, cs_pin):
        config.digital_write(cs_pin1, GPIO.LOW)
        config.spi_writebyte1([CMD['CMD_RDATA']])
        buf = config.spi_readbytes1(3)
        config.digital_write(cs_pin1, GPIO.HIGH)
        read = (buf[0] << 16) & 0xff0000
        read |= (buf[1] << 8) & 0xff00
        read |= (buf[2]) & 0xff
        if read & 0x800000:
            read &= 0xF000000
        return read


    def ADS1256_GetChannalValue(self, Channel, window, duration=1.0):
        data_list = []
        data_string = ""
        counter0 = 0
        counter1 = 0
        conversion_factor = 1675701.13
        intercept = 14386.52

        if ScanMode == 0:
            if Channel >= 8:
                return 0
            self.ADS1256_SetChannal0(Channel)
            self.ADS1256_WriteCmd0(CMD['CMD_SYNC'])
            self.ADS1256_WriteCmd0(CMD['CMD_WAKEUP'])
            
            self.ADS1256_SetChannal1(Channel)
            self.ADS1256_WriteCmd1(CMD['CMD_SYNC'])
            self.ADS1256_WriteCmd1(CMD['CMD_WAKEUP'])            
            
            start_time = time.time()
            while time.time() - start_time < duration:
                timestamp0 = time.time()
                value0 = (self.ADS1256_Read_ADC_Data0() - intercept) / conversion_factor
                counter0 += 1
                timestamp1 = time.time()
                value1 = (self.ADS1256_Read_ADC_Data1() - intercept) / conversion_factor
                counter1 += 1
                data_string += f"{window}, {Channel}, {timestamp0}, {value0}, {timestamp1}, {value1}\n"
        else:
            if Channel >= 4:
                return 0
            self.ADS1256_SetDiffChannal0(Channel)
            self.ADS1256_WriteCmd0(CMD['CMD_SYNC'])
            self.ADS1256_WriteCmd0(CMD['CMD_WAKEUP'])
            
            self.ADS1256_SetDiffChannal1(Channel)
            self.ADS1256_WriteCmd1(CMD['CMD_SYNC'])
            self.ADS1256_WriteCmd1(CMD['CMD_WAKEUP'])
            
            start_time = time.time()
            while time.time() - start_time < duration:
                timestamp0 = time.time()
                value0 = (self.ADS1256_Read_ADC_Data0() - intercept) / conversion_factor
                counter0 += 1
                timestamp1 = time.time()
                value1 = (self.ADS1256_Read_ADC_Data1() - intercept) / conversion_factor
                counter1 += 1
                data_string += f"{window}, {Channel}, {timestamp0}, {value0}, {timestamp1}, {value1}\n"

        print(f"done with {Channel} with {counter0} values for ADC1 and {counter1} values for ADC2")
        return data_string


    def ADS1256_GetAll(self, window):
        ADC_Value = ""
        print("start time: " + str(time.time()))
        for i in range(0, 8, 1):
            ADC_Value += self.ADS1256_GetChannalValue(i,window)
        print("end time: " + str(time.time()))
        #print(ADC_Value)
        return ADC_Value

    def getOne(self, channel):
        val = self.ADS1256_GetChannalValue(channel)
        return str(val * weird_val) + "," + str(time.time()) + "\n"

    def getUpTo(self, channel_range):
        vals = []
        tims = []
        if channel_range == 1:
            vals = [0]
            tims = [0]
        else:
            for _ in range(channel_range):
                vals.append(0)
                tims.append(0)
        if channel_range == 1:
            vals[0] = self.getchannal(1) * 5.0 / 0x7fffff
            tims[0] = time.time()
        else:
            for j in range(channel_range):
                vals[j] = self.getchannal(j) * 5.0 / 0x7fffff
                tims[j] = time.time()
        return vals, tims

