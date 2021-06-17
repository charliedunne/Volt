##
# Example code for testing the function parse_naturgy_bill()

import json
from importlib.machinery import SourceFileLoader

tst = SourceFileLoader("parse_naturgy_bill", "../src/parse_naturgy_bill_f.py").load_module()

# Run SWUT
[outCode, data] = tst.parse_naturgy_bill('../input/FEXXXXXXXXXXXXXX.xls')

# Verify Results
if (outCode != 0):
    print('ERROR in the parsing (code ' + str(outCode) + ')')
    exit()


# Check some data
data = json.loads(data)

if (data['cups'] != 'ESXXXXXXXXXXXXXXXXXXXX'):
    print('Test Failed. Wrong CUPS')
    exit()


if (data['bill'] != 'FEXXXXXXXXXXXXXX'):
    print('Test Failed. Wrong bill number')
    exit()

if (data['data'][5]['consumption'] != 0.089):
    print('Test Failed. Wrong data')
    exit()

print('Test SUCCESS')



