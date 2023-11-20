# NOTE: the default pyvisa import works well for Python 3.6+
# if you are working with python version lower than 3.6, use 'import visa' instead of import pyvisa as visa

import pyvisa as visa
import time
import numpy as np
# start of Untitled

def frequencyValues(power0, power1, points):
    # Set up result array
    result = np.empty(0)

    # Add values for each decade and for the final value
    for i in range(power0, power1):
        result = np.append(result, np.linspace(10**i, 10**(i + 1), points)[:-1])
    result = np.append(result, 10**power1)

    # Return result
    return result

vals = frequencyValues(2, 10, 10)
print(vals)
rm = visa.ResourceManager()
scope = rm.open_resource('USB0::0x2A8D::0x0396::CN62097153::0::INSTR')
fg = rm.open_resource('USB0::0x2A8D::0x8D01::CN61420203::0::INSTR')
string = fg.query('*IDN?')

idn_scope = scope.query('*IDN?')
opt_scope = scope.query('*OPT?')
scope.write(':SYSTem:PRESet')
scope.write(':MEASure:FREQuency %s' % ('CHANnel1'))

for i in vals:
    print(i)
    fg.write(':SOURce:FREQuency %G' % (i))
    scope.write(':AUToscale %s' % ('CHANnel1'))
    input()

temp_values = scope.query_ascii_values(':MEASure:FREQuency? %s' % ('CHANnel1'))
source = temp_values[0]
print(temp_values)

scope.close()
fg.close()
rm.close()

# end of Untitled
