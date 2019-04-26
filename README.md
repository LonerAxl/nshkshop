# nshkshop
simple spiders for store.nintendo.com.hk and store.nintendo.co.jp

I wrote these spider on Mac, so not guarantee working on other OS

about venv
use pip to install scrapy and selenium

pip install scrapy

pip install selenium

-----------------------------------

scrapy crawl nshkspider

use this to run nshkspider, which gives all the items in store.nintendo.com.hk

-----------------------------------

scrapy crawl nsjpsalespider

use this to run nsjpsalespider, which gives all on sale items in store.nintendo.co.jp

-----------------------------------

for this spider, chromedriver is necessary

https://sites.google.com/a/chromium.org/chromedriver/downloads

unzip and put the executable in a dedicated folder and add this folder to the environment variable PATH

or just put it in a folder which is in PATH

and this one is still slightly buggy

will fix later

and will rewrite README.md later (after I learn how to format this :)

