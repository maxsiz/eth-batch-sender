# -*- coding: utf-8 -*-
import logging
import os
import json
import sys
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
import time
import config


def handle_batch_transfer(_receivers_list):
    """
    Sign  and Send new transfer transaction in Ethereum blockchain
    
    """
    try:
        #######################################################
        #1. Prepare contrac method
        ########################################################
        tx_data = token.encodeABI(
            #fn_name="multiTransfer", 
            fn_name="promo",
            args=[
                [Web3.toChecksumAddress(a) for a in _receivers_list] #address array
                #[1*10**18 for a in range(len(_receivers_list))] #amount array
            ]
        )
        logging.debug('tx_data={}'.format(tx_data))
        ###################################################
        #2. eth tx
        tx_full_data={
            'to': config.ADDRESS_TOKEN, 
            'from': config.ADDRESS_OPERATOR, 
            'data': tx_data,
            'nonce':w3.eth.getTransactionCount(config.ADDRESS_OPERATOR), 
            'gas':8000000, 
            'gasPrice': _gasPrice
        }
        logging.debug('tx_full_data={}'.format(tx_full_data))

        _estGas = w3.eth.estimateGas(tx_full_data)
        logging.info(
            '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n'
            'Estimate gas = {}\n'
            'gasPrice = {} gwei\n'
            'Estimate tx cost = {} eth\n'.format(
                _estGas,
                w3.fromWei(_gasPrice, 'gwei'),
                w3.fromWei(_estGas*_gasPrice, 'ether')
            )
        )
        # choice = input('Do you realy want sign and send this tx ? (Yes/no): ')
        # if  choice != 'Yes':
        #     sys.exit('Buy!!!')
    
    except Exception as e:
        logging.warning('Error in w3.eth.estimateGas = {}'.format(e.args))
    else:
        #Sign tx
        signed_tx=w3.eth.account.signTransaction(
            tx_full_data, 
            private_key=config.ADDRESS_OPERATOR_PRIVKEY
        )
        logging.debug('signed_tx={}'.format(signed_tx))
        
        #Send Raw tx
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logging.info('Please see in etherscan tx_hash={}'.format(tx_hash.hex()))

    finally:
        pass

    
def main():
    """
    Main entry point
    """

    if  len(sys.argv)==2:
        file1 = sys.argv[1] #file with receivers list
    else:
        print (
            'wrong params number - {}'
            ' , usage: python3 {} receivers_address_file'.format(
                len(sys.argv), sys.argv[0]
            )
        )
        sys.exit('use file as script param')

    with open(file1) as r_file:
        lines = r_file.readlines()
        receivers_list=[s.rstrip('\n') for s in lines]
        logging.debug('Receivers are {}'.format(receivers_list))
        handle_batch_transfer(receivers_list) 



####################################################################
####################################################################

####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################

########################################
###  Module initialize section      ####
########################################
logging.basicConfig(format='%(asctime)s->%(levelname)s:[in %(filename)s:%(lineno)d]:%(message)s'
    , level=int(config.APPLOG_LEVEL)
)

#txSenderAddress = '0x86C3582b6505CcB8faDAcb211fC1E5a8fDD26E91' #ExoACCICO
#web3 provider initializing
if 'http:'.upper() in config.WEB3_PROVIDER.upper():
    w3 = Web3(HTTPProvider(config.WEB3_PROVIDER))
elif 'ws:'.upper()  in config.WEB3_PROVIDER.upper() or 'wss:'.upper() in config.WEB3_PROVIDER.upper():
    w3 = Web3(Web3.WebsocketProvider(config.WEB3_PROVIDER))    
else:
    w3 = Web3(IPCProvider(config.WEB3_PROVIDER))
logging.info('w3.eth.blockNumber=' + str(w3.eth.blockNumber))
#w3.eth.defaultAccount  = config.ADDRESS_OPERATOR


_gasPrice = w3.toWei(config.GAS_PRICE, 'gwei')

#Need some injection on Rinkeby and -dev networks
if  w3.net.version == '4':
    from web3.middleware import geth_poa_middleware
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)


token = w3.eth.contract(address=config.ADDRESS_TOKEN,
    abi=config.TOKEN_ABI
)

name     = token.functions.name().call()
symbol   = token.functions.symbol().call()
#decimals = token.functions.decimals().call()
totalSupply = token.functions.totalSupply().call
logging.info('Token contract at address {} initialized:{} ({}), decimals='.format(
    config.ADDRESS_TOKEN,
    name,
    symbol,
    #decimals
    )
)

###########################################
if __name__ == '__main__':
    main()