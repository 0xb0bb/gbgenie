# gbgenie

A small utility to encode and decode Game Genie codes for the Nintendo GameBoy.

## Usage

### Command Line

```bash
$ ./gbgenie.py 
usage:    ./gbgenie.py <code>
          ./gbgenie.py <addr> <value> [original]

examples:

    decode: ./gbgenie.py 001-5CA-E62
            ./gbgenie.py 001-5CA

    encode: ./gbgenie.py 0x7654 0x01
            ./gbgenie.py 0x7654 0x02 0xff
            ./gbgenie.py 1234 ab cd

$ ./gbgenie.py 004-BCE-E66
0x14bc: 0x03 => 0x00

$ ./gbgenie.py 0x14bc 0x00 0x03
code: 004-BCE-E66

```

### Python

```python
#!/usr/bin/python
import gbgenie

CODE = '004-BCE-E66'

# decode a gameboy game genie code
data = gbgenie.decode(CODE)
print 'DECODE:  %s' % CODE
print 'address: 0x%02x; original: 0x%02x; replacement: 0x%02x\n' % (data['addr'], data['original'], data['value'])

# encode back into a gameboy game genie code
code = gbgenie.encode(data['value'], data['addr'], data['original'])
print 'ENCODE:  (0x%02x, 0x%02x, 0x%02x)' % (data['addr'], data['original'], data['value'])
print 'ggcode:  %s' % code

```
