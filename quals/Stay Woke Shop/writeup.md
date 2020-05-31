---
html:
  embed_local_images: true
  embed_svg: true
  offline: true
export_on_save:
  html: true
print_background: true
---
@import "../style.less"

# StayWoke Shop - localo


**Category:** Web
**Difficulty:** Easy        
**Author:** pspaul

## Description
>Are you missing some essential items that were sold out in your local supermarket? You can easily stock up on these in my shop:
>
>http://staywoke.hax1.allesctf.net/
## Summery
The author provided a link to an online shop. You can buy everything you need toilet paper, tinfoil and much more. You can put up to `10` products into your shopping cart. You can use a currency called `w0kecoin` to pay, you just need the right bank account number. In addition to that you can lower the price a bit by using a coupon.

## Solution
The website uses an internal api to process the order. We can change the `POST` request parameter `paymentEndpoint` to do a `SSRF`.
@import "ssrf.png"
I fuzzed the parameter a bit.
@import "fuzz.py"
We often get the message: `Error from Payment API: "Cannot GET /[...]/wallets/0/balance\n\nTry GETting /help for possible endpoints."` So there seems to be an endpoint where we can list all endpoints of the api. But two of my tests were a bit more interesting:
```e
Test: 35
Error from Payment API: "Cannot GET /\n\nTry GETting /help for possible endpoints."
[...]
Test: 63
Error from Payment API: "Cannot GET /\n\nTry GETting /help for possible endpoints."
```
The characters I tested were `#` and `?`. We can use those to trim our request and therefore a request with `http://payment-api:9090/help?` will list us the endpoints.  
```json
Error from Payment API: {
  "endpoints": [
    {
      "method": "GET",
      "path": "/wallets/:id/balance",
      "description": "check wallet balance"
    },
    {
      "method": "GET",
      "path": "/wallets",
      "description": "list all wallets"
    },
    {
      "method": "GET",
      "path": "/help",
      "description": "this help message"
    }
  ]
}
```
We can use the same method to list all wallets with `http://payment-api:9090/wallets?`
```json
Error from Payment API: [{"account":"1337-420-69-93dcbbcd","balance":133500}]
```
We can now use this account to buy stuff.
If we select an item to buy, the url is `http://staywoke.hax1.allesctf.net/products/[id]`. For toilet paper it is `http://staywoke.hax1.allesctf.net/products/2`, if we change the id to `1` we can put the flag into our shopping cart.
@import "flag.png"
But we still can't afford the flag, since it costs 2€ too much.
The news banner on the top contains a coupon to get `20% off`.
```json
[
  "neue Chemtrails gesichtet",
  "COVID-19 ist erfunden von denen da oben",
  "20% Rabatt mit dem Code I<3CORONA",
  "BND betreibt neuen Honeypot \"CSCG\" um 0days abzugreifen",
  "SARS-CoV-2 war ein Insiderjob"
]
```
But unfortunately we can't use this code on the flag. But we get a new item in our shopping cart if we redeem it.
@import "cart.png"
If we now remove an item, the value of the coupon item stays the same.
@import "money.png"
We should now get money if we check out, but this does not work.
Instead we have to put 10 normal items into the shopping cart, redeem the coupon remove the items and add the flag. The price is now at 1335€ and we can afford it. 
@import "1335.png"

## Mitigation
- never trust client information
- don't expose secret endpoints
- use more tinfoil

## Flag
CSCG{c00l_k1ds_st4y_@_/home/}