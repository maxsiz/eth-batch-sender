# eth-batch-sender
A utility for preparing, signing and sending to the Ethereum network a
 transaction for sending tokens in a bundle. The recipient addresses must 
 be specified in the `receivers.csv` file, each on a separate line. 


### Local use with Docker

All parameters are passed to the container through environment variables,
which can be set in the file `.env.local` 

`env.local` example
```txt
APP_LOGLEVEL=40
WEB3_INFURA_PROJECT_ID=79f3c18a7d394279b3bc877fa2610caf
WEB3_PROVIDER=wss://rinkeby.infura.io/ws/v3/79f3c18a7d394279b3bc877fa2610caf
ADDRESS_TOKEN=0x9CaE745007abC88e7af872f704795e3823fd7D91
ADDRESS_OPERATOR=0xafB42ffDC859f82eDb3E93680F95212200f0CCA1
ADDRESS_OPERATOR_PRIVKEY=384d9719f2cdfa068a58811541aa1a6059306a4ae61a0a360ee6443d3f610977
GAS_PRICE=100
```

`token.abi` should contain json from the ABI of the contract.


```bash
cd eth-batch-sender

#1. Build image with dependencies
docker build -f ./docker/DockerfileLocal -t eth_batch_sender:local .

#2. !!!!!!!!!! put and check receivers strings into receivers.csv
cat receivers.csv

#3. Just run and check output
docker-compose -p batch -f docker-compose-local.yaml up

#4. For long receivers list please use this
# receiver record format: `address;float_amount`
# float amount may be: 2,1E+016 or 2.1E+016 or 5000000000000000
docker-compose -p batch -f docker-compose-local2.yaml up
```
### Examples of tx sent
[DEMO PROMO vTOKEN with promo(address[] _rec)](https://rinkeby.etherscan.io/token/0x131220c96a08020cc9e58954ddc26c89b6dc2b13)  
[1000+ address tx](https://rinkeby.etherscan.io/tx/0x5a6fb25ece2c726508bcf2228adb0be7b658ea2b02902fb29b3717d2d967a8e2)  
[PROMO token code](./yAtoken.sol)

-------------------------------------------------------------

[Token ERC20+ multiTransfer([],[])](https://rinkeby.etherscan.io/address/0x9cae745007abc88e7af872f704795e3823fd7d91#code)  

Transactions:  
https://rinkeby.etherscan.io/tx/0x994ced7df05924bc991a8b2810f85358035f652aeda11d09a0add1065a58a74b  
https://rinkeby.etherscan.io/tx/0x53ef83aaa38541c233b4d1970693a6c9b9e0f5fcf61e18722dcd45d63287364f  

### Adaptation
Lines 21-27 of the `batch_sender.py` file can be changed if the method has a different name and parameters.


### Tokens
QDEFi
https://bscscan.com/token/0x8F00A6D49165C4679Fb851846BcF18Bb37546084

QDAOI
https://bscscan.com/token/0x2bf5b0df27f31388d5b825b39bd752bed6c7f7e9