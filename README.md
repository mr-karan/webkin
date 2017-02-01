# webkin
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/mr-karan/webkin/master/LICENSE)

>webkin lets you send webpages to your kindle device through terminal. 
Note : Python3+ only.

### Installation : 

> `pip install webkin`

[![asciicast](https://asciinema.org/a/101549.png)](https://asciinema.org/a/101549)

###Avilable commands : 

#### To parse URL and send it to your kindle email id.

`webkin --url `

#### To change the default directory.

`webkin --url=<url> --path=</path/to/your/place> `

> Example : 

`webkin -u=https://medium.com/@mrkaran/my-development-setup-7e767d33fc41 --verbose`

![img](http://i.imgur.com/aeIzhPQ.jpg)

### Pre Installation

`webkin` depends on calibre CLI tools and uses `ebook-convert` to convert `html` to `mobi` format. Please ensure that you have Calibre installed alongwith CLI tools and `ebook-convert` is present in your PATH. 
For OSX users, you don't need to do anything besides [installing Calibre](http://calibre-ebook.com/download_osx).
I have tested it on Ubuntu 16.04 fresh VM and after installing Calibre, it worked fine. If you install using [this](http://calibre-ebook.com/download_linux) method, you need to manually add `ebook-convert` to your path, while if you install it from PPA, it's automatically in your PATH.

```
sudo add-apt-repository ppa:n-muench/calibre2
sudo apt-get update
sudo apt-get install calibre
```
[Source](http://askubuntu.com/questions/338172/how-to-install-calibre-on-ubuntu-12-04)

### First Time Setup 
You need to export tokens to add your `Amazon Email Address` (should be present in your [Approved Personal Document Email List](https://www.amazon.com/gp/help/customer/display.html?nodeId=2019742) ), `Kindle Email Address`, `Mercury Web Parser API Key` ,`SMTP Hostname and SMTP Port`. The first time setup will guide you on how to do that.

 - To obtain your Mercury Web API key, signup [here](https://mercury.postlight.com/web-parser/)
 - If you're using GMail, you need to add `smtp.gmail.com` as your `SMTP_Host_NAME` while the default port is `587` so you can skip adding that. If you're using any other email provider, you can find a comprehensive list over [here](https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html) and add accordingly
 - If you're using GMail and have turned on 2FA (which you must absolutely), you rather need to add an Application Password instead of your email password. Set a new one over [here](https://security.google.com/settings/security/apppasswords)

## Credits

- [calibre](http://calibre-ebook.com/)
- [Mercury Web Parser](https://mercury.postlight.com/web-parser/)
- [@sathyabhat](https://github.com/SathyaBhat/spotify-dl/blob/master/spotify_dl/scaffold.py) for his clean implementation of fetching tokens in a CLI program, which I have shamlelessly adapted for webkin.

## Contributing

Feel free to report any issues and/or send PRs for additional features.

## Why ? 

Well, there are a couple of tools to already do this task, but I couldn't find any Open source tool which does it. Though Kindle uses a `MOBI` format which itself is closed source, I found the need of a CLI application to automate this boring task for me. If you're looking for a tool to do this but don't wanna use a terminal, you can also take a look at [this](https://chrome.google.com/webstore/detail/send-to-kindle-for-google/cgdjpilhipecahhcilnafpblkieebhea?hl=en) chrome extension. I like my stuff in the Terminal so I did it :)  

### License
> MIT © Karan Sharma 

> [LICENSE included here](LICENSE)
