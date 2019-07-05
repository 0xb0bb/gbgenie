#!/usr/bin/env python
import nose
from nose.tools import assert_equal

import gbgenie

def test_decode_long():
    assert_equal(gbgenie.decode('001-5CA-E62'), {'addr': 0x515c, 'original': 0x02, 'value': 0x00})

def test_decode_short():
    assert_equal(gbgenie.decode('001-5CA'), {'addr': 0x515c, 'value': 0x00})

def test_encode_short():
    assert_equal(gbgenie.encode(0x7654, 0x01), '016-548')

def test_encode_long():
    assert_equal(gbgenie.encode(0x7654, 0x02, 0xff), '026-548-195')

if __name__ == '__main__':   
    nose.run()
