import batch_sender
import logging

tx  = batch_sender.w3.eth.getTransaction(0x4b73271fddec011e0d6129ed3f2872131dc0aa8db2de5ed2e91be7d81807620a)
logging.debug('----------------------Tx = {}'.format(tx))