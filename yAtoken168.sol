// PROMO TOKEN

pragma solidity ^0.6.12;

contract Promo {
    uint256 public immutable totalSupply;
    string  public  name;
    string  public  symbol;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    constructor  
        () 
        public
        {
            totalSupply = 80000000000000;
            name   = "www.168pools.com - visit now for DeFi ROi and POOLs stats";
            symbol = "www.168pools.com - visit now for DeFi ROi and POOLs stats";
            emit Transfer(address(0), address(this), 80000000000000);
        }
    
 
    function approve(address spender, uint256 amount) external returns (bool) {
         emit Approval(msg.sender, spender, 100);
         return true;
    }
     
     
    function transfer(address recipient, uint256 amount) external  returns (bool) {
         emit Transfer(msg.sender, recipient, 2500);
         return true;
    }
    
    function promo(address[] memory _recipient) external  returns (bool) {
        for (uint i=0; i< _recipient.length; i++){
             emit Transfer(msg.sender, _recipient[i], 856420144564);
        }
        return true;
    }
    
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool){
         emit Transfer(sender, recipient, 100);
         return true;
     }

    function allowance(address owner, address spender) external  view returns (uint256){
        return uint256(-1);
    }

    function balanceOf(address account) external  view returns (uint256){
        return uint256(856420144564);
    }
    
}