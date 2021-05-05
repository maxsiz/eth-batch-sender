# -*- coding: utf-8 -*-
import logging
import os
import json
import sys
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
import datetime, random
import config


def handle_batch_transfer(_receivers_list, _file, _amounts=[]):
    """
    Sign  and Send new transfer transaction in Ethereum blockchain
    
    """
    try:
        if  len(_receivers_list) > 254:
            logging.warning('!!!!!!!!Param list is longer 254, {}. You can comment it if contract can accept it.'.format(len(_receivers_list)))
            return;
        #######################################################
        #1. Prepare contrac method
        ########################################################
        tx_data = token.encodeABI(
            fn_name="transferMany", #qdao
            #fn_name="promo",
            #fn_name="multiTransfer", #qdefi
            args=[
                [Web3.toChecksumAddress(a) for a in _receivers_list], #address array
                #[1*10**18 for a in range(len(_receivers_list))] #amount array for qdao
                _amounts #amount array for qdao
                #1*10**16 #constant amount for qdefi
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
            #'nonce':2, 
            'gas':7000000, 
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
        logging.info('File {}  etherscan tx_hash= {}'.format(_file ,tx_hash.hex()))
        return tx_hash.hex() 
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

    #
    send_log = SendLog(file1)


    with open(file1) as r_file:
        lines = r_file.readlines()
        receivers_list=[s.rstrip('\n') for s in lines if len(s)>1]
        logging.debug('len(lines)={}'.format(len(lines)))
        #try search amounts
        #[int(float(x.split(';')[1].replace(',','.'))) for x in lines2]
        if ';' in receivers_list[0]:
            amounts = [int(float(x.split(';')[1].replace(',','.'))) for x in receivers_list]
            receivers_list = [x.split(';')[0] for x in receivers_list]
            #logging.debug('Amounts are {}'.format(amounts))
        #logging.debug('Receivers are {}'.format(receivers_list))

        for i in range(len(lines)//BATCH_SIZE +1):
            from_index = int(send_log.get_last_sended_index()) + 1

            if  len(lines) - from_index >= BATCH_SIZE:
                #rest more or equal than batch lenght
                to_index = from_index + BATCH_SIZE-1
            elif len(lines) < (from_index ):
                #all is done
                logging.info('All is done. {} records sended'.format(len(lines)))
                return
            else:
                to_index = len(lines)  #for last record include

            logging.info('Sending from_index(string)={} to_index(string)={}..'.format(from_index, to_index))           
            tx_hash = handle_batch_transfer(
                receivers_list[from_index-1:to_index-1], 
                file1, 
                amounts[from_index-1:to_index-1]
            )
            logging.info('send array [{}:{}], from {}, to {},  len={}'.format(
                from_index - 1,
                to_index,
                receivers_list[from_index - 1],
                receivers_list[from_index - 1:to_index][-1],
                len(receivers_list[from_index - 1:to_index])
            ))
            #tx_hash = str(random.random()*100000) #Dummy
            if  tx_hash is not None:

                send_log.add_record_log(to_index, tx_hash, 0)

                #receipt = {'status':1} #Dummy
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash) 
                logging.debug('tx receipt:{}'.format(receipt))
                send_log.update_tx_state(to_index, tx_hash, receipt['status'])  
                if receipt['status'] != 1:
                    logging.warning('Please CHECK LOG - {}'.format(send_log.log_file_name))
                    break

class SendLog:
    def __init__(self,file_for_send):
        self.send_file_name = file_for_send
        self.log_file_name = self.send_file_name + '.log'
        if  not os.path.exists(self.log_file_name):
            with open(self.log_file_name, 'w'):pass
    
    def get_last_sended_index(self):
        if  os.stat(self.log_file_name).st_size > 3:
            with open(self.log_file_name, 'r') as log_file:
                log_lines = log_file.readlines()
                if  len(log_lines) > 0 :
                    if  log_lines[-1].split(';')[2] == '1': #ok status
                        self.last_receiver_index = log_lines[-1].split(';')[0]
                    else:
                        logging.warning('Please check you log {}'.format(log_file))
                        raise
                else:
                    self.last_receiver_index = 0        
        else:
            self.last_receiver_index = 0

        return self.last_receiver_index

    # def get_total_for_send(self):
    #     return self.total_strings    

    def add_record_log(self, _receivers_index, _tx_hash, _tx_state):
        log_str = '{};{};{};{}\n'.format(
            _receivers_index, 
            _tx_hash, 
            _tx_state,
            datetime.datetime.now().time()
        )
        logging.debug('add logg rec')
        with open(self.log_file_name, 'a') as log_file:
            log_file.write(log_str)
            #log_file.close()
        with open(self.log_file_name) as log_file:
            logging.debug('addrecord: Read from file len: {}'.format(len(log_file.read())))    

    def update_tx_state(self, _receivers_index, _tx_hash, _tx_state):
        with open(self.log_file_name, 'r') as log_file:
            log_lines = log_file.readlines()
            #logging.debug('update tx, reading from log:{}'.format(log_lines))
            #log_lines = [s.rstrip('\n') for s in lines]
        tx_hashes= [x.split(';')[1] for x in log_lines]
        #logging.debug('Update state. Searche for {} in {}'.format(_tx_hash, tx_hashes))    
        index = tx_hashes.index(_tx_hash)
        log_lines[index] = '{};{};{};{}\n'.format(
            _receivers_index, 
            _tx_hash, 
            _tx_state,
            datetime.datetime.now().time()
        )
        #logging.debug('Lets save new lines: {}'.format(log_lines))
        with open(self.log_file_name, 'w') as log_file:
            log_file.writelines(log_lines)
        self.total_strings = len(log_lines)
        
        
        

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
if 'http:'.upper() in config.WEB3_PROVIDER.upper() or 'https:'.upper() in config.WEB3_PROVIDER.upper():
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
decimals = token.functions.decimals().call()
totalSupply = token.functions.totalSupply().call()
logging.info('Token contract at address {} initialized:{} ({}), decimals={}, totalSupply={}'.format(
    config.ADDRESS_TOKEN,
    name,
    symbol,
    decimals,
    totalSupply
    )
)

BATCH_SIZE=200

###########################################
if __name__ == '__main__':
    main()