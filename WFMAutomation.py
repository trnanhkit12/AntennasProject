# NOTE: the default pyvisa import works well for Python 3.6+
# if you are working with python version lower than 3.6, use 'import visa' instead of import pyvisa as visa

import pyvisa as visa
import time
import numpy as np
# start of Untitled

scope_address = 'USB0::0x2A8D::0x0396::CN62097187::0::INSTR'
fg_address = 'USB0::0x2A8D::0x8D01::CN61420105::0::INSTR'

# Takes two ints power0 and power1
# Returns an array of frequencies that sweep from 10^power0 to 10^power1 with a 
# given number of points in between 
def frequencyValues(power0, power1, points):
    # Set up result array
    result = np.empty(0)

    # Add values for each decade and for the final value
    for i in range(power0, power1):
        result = np.append(result, np.linspace(10**i, 10**(i + 1), points)[:-1])
    result = np.append(result, 10**power1)

    # Return result
    return result

vals = frequencyValues(2, 7, 5)
print(vals)
rm = visa.ResourceManager()
scope = rm.open_resource(scope_address)
fg = rm.open_resource(fg_address)
OUTPUT_CHANNEL ='CHANnel1' # REMINDING WHICH SCOPE'S CHANNEL WE'RE MEASURING THE OUTPUT FROM
string = fg.query('*IDN?') # What is this?

idn_scope = scope.query('*IDN?')
opt_scope = scope.query('*OPT?')
fg.write('*RST')           # Resets the function generator to the default setting

# Initializing scope's view
scope.write(':SYSTem:PRESet')
scope.write(':MEASure:FREQuency %s' % ('CHANnel1'))
scope.write(':MEASure:VPP %s' % ('CHANnel1'))
scope.write(':MEASure:PHASe %s,%s' % ('CHANnel2', 'CHANnel1'))  # phase difference between channel 1 (out) to channel 2 (in)

fg.write(':OUTPut:LOAD %s' % ('INFinity'))  # Sets the function generator to high impedance mode
freq_out = np.empty(0)
v_out = np.empty(0)
phase_diff = np.empty(0)
print(freq_out)
print(freq_out)
for i in vals:
    print(i)
    fg.write(':SOURce1:APPLy:SINusoid %G HZ,%G V' % (i, 1.0))   # A testing function generator output simulating the 
                                                                # output waveforms (remove when performing test)
    fg.query_ascii_values('*OPC?')
    fg.write(':SOURce2:APPLy:SINusoid %G HZ,%G V' % (i, 1.0))
    fg.query_ascii_values('*OPC?')
    scope.write(':AUToscale')
    scope.query_ascii_values('*OPC?')
    # getting values from channel out
    freq_out = np.append(freq_out, scope.query_ascii_values(':MEASure:FREQuency? %s' % ('CHANnel1'))[0])
    v_out = np.append(v_out, scope.query_ascii_values(':MEASure:VPP? %s' % ('CHANnel1'))[0])
    phase_diff = np.append(phase_diff, scope.query_ascii_values(':MEASure:PHASe? %s,%s' % ('CHANnel2', 'CHANnel1'))[0])

print(freq_out)
print(v_out)
print(phase_diff)

scope.close()
fg.close()
rm.close()

# end of Untitled
