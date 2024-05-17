import pyvisa
from time import sleep
import os

filepath = "./data.csv"
rm = pyvisa.ResourceManager()
print(rm.list_resources())

# Defining the voltage limits of the BOP
v = -20
v_max = 20
v_step = 0.5

# Opening the Nanovoltmeter, defining a timeout limit and doing some sanity checks
Nanovolt_keithley = rm.open_resource('GPIB0::7::INSTR')
Nanovolt_keithley.timeout = 10000
n_string = Nanovolt_keithley.query('*IDN?')
n_licenseInfo = Nanovolt_keithley.query('*OPT?')

# Opening the BOP, defining a timeout limit and doing some sanity checks
BOP = rm.open_resource('GPIB0::6::INSTR')
BOP.write_termination = '\n'
BOP.read_termination = '\n'
BOP.query_delay = 3
BOP.timeout = 10000
b_string = BOP.query('*IDN?')
b_licenseInfo = BOP.query('*OPT?')
print(b_string)

# Nanovoltmeter configuration
Nanovolt_keithley.write('*RST')
Nanovolt_keithley.write(':SENS:FUNC: VOLT')
Nanovolt_keithley.write(':SENS:CHAN1')
Nanovolt_keithley.write(':SENS: VOLT:CHAN1: RANG:AUTO ON; *OPC')

# BOP configuration
BOP.write('*RST')
BOP.write('FUNC:MODE VOLT')
BOP.write(':VOLT 0; :CURR 20')
BOP.write('OUTP ON')

while v <= v_max:
    BOP.write(':VOLT ' + str(v))
    BOP.write('MEAS:VOLT:DC?')
    sleep(2)
    Volt_applied = float(BOP.read('MEAS:VOLT:DC?', 127))
    Volt_measured = float(Nanovolt_keithley.query(':READ?'))

    # Print the measured values
    print("{} {}".format(Volt_applied, Volt_measured))
    # Write the measured values on a file
    with open(filepath, 'a') as file:
        if os.stat(filepath).st_size == 0:
            file.write("Applied volt [V], Measured volt [V]\n")
        file.write("{:16.4f}, {:18.8f}\n".format(Volt_applied, Volt_measured))
    file.close()
    v += v_step

Nanovolt_keithley.close()
BOP.close()
rm.close()
