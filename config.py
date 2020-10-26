# -*- coding: utf-8 -*-
import os
import logging
import json


abi_file=open('token.abi')
abi_str = abi_file.read()
APPLOG_LEVEL=os.environ.get('APPLOG_LEVEL',logging.DEBUG)# logging.DEBUG-10 .....logging.CRITICAL-50
WEB3_PROVIDER = os.environ.get('WEB3_PROVIDER','http://127.0.0.1:8545')
ADDRESS_TOKEN = os.environ.get('ADDRESS_TOKEN','0x9CaE745007abC88e7af872f704795e3823fd7D91')
ADDRESS_OPERATOR = os.environ.get('ADDRESS_OPERATOR','0xE71978b1696a972b1a8f724A4eBDB906d9dA0885')
ADDRESS_OPERATOR_PRIVKEY = os.environ.get('ADDRESS_OPERATOR_PRIVKEY',0)
TOKEN_ABI = json.loads(abi_str)
GAS_PRICE=os.environ.get('GAS_PRICE', '100')

