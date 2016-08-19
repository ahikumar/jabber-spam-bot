# Jabber-spam

Spam bot module for mass mailing messages via xmpp.


### Launch:

For launch:  
```Bash
$ python spam-bot.py
```


### Setting:

Bot takes the recipient and sender respectively of the file  `recipients` and `senders`. Bot configuration is in the file `config.py`.  

Log conducted in `stdout`, but you can remove it:  
```Python
# config.py

...
debug = False
```