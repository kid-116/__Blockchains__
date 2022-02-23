// SPDX-License-Identifier: UNLICENSED
// Mecoin ICO

pragma solidity ^0.8;

contract mecoin_ico {
    // mecoin pool
    uint public coin_pool = 1000000;
    // conversion rate
    uint public usd_to_mecoin = 1000;
    // coins in market
    uint public coins_in_market = 0;
    // mapping investor's address to equity
    mapping(address => uint) equity_mecoins;

    modifier can_buy_mecoin(uint usd_invested) {
        require(usd_invested * usd_to_mecoin + coins_in_market <= coin_pool);
        _;
    }
    modifier can_sell_mecoin(address investor, uint mecoin_sold) {
        require(equity_mecoins[investor] >= mecoin_sold);
        _;
    }

    function equity_in_mecoins(address investor) public view returns (uint) {
        return equity_mecoins[investor];
    }
    function equity_in_usd(address investor) public view returns (uint) {
        return equity_in_mecoins(investor) * usd_to_mecoin;
    }

    function buy_mecoins(address investor, uint usd_invested) public 
    can_buy_mecoin(usd_invested) {
        uint mecoins_bought = usd_invested * usd_to_mecoin;
        equity_mecoins[investor] += mecoins_bought;
        coins_in_market += mecoins_bought;
    }

    function sell_mecoins(address investor, uint mecoin_sold) public 
    can_sell_mecoin(investor, mecoin_sold) {
        equity_mecoins[investor] -= mecoin_sold;
        coins_in_market -= mecoin_sold;
    }
}