v = int(10)
print('VOLT ' + str(v))

# Set the buffer size
buffer_size = 20
# Configures the buffer size and enables the buffer mode on the nanovoltmeter.
Nanovolt_keithley.write(':TRAC:POIN ' + str(buffer_size) + '; :TRAC:FEED SENS')
# Enables the Mean calculation mode.
Nanovolt_keithley.write(':CALC2:FORM MEAN; :CALC2:STAT ON')

# Put the next 20 measurements in the buffer.
Nanovolt_keithley.write(':TRAC:FEED:CONT NEXT')
# Calculates the mean voltage across the collected data.
Volt_measured = float(Nanovolt_keithley.query(':CALC2:IMM?'))
# Clear the all buffer stored values
Nanovolt_keithley.write(':TRAC:CLE')

