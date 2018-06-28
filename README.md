This is a proxy that lets you observe and modify packets as they come and go, with custom python code. There's no need to restart the proxy, just change the parser module (single function), it'll be reloaded automatically.

There's a lot of 'borrowed' code from LiveOverflow, go check him out.

![exmaple](https://cukii.me/stjo/other/mc_proxy_chat_1.png)

# Getting started
```
git clone [this repo]
cp minecraft_replace_chat.py proxy.py # example parser that replaces the chat messages with a repeating string
python proxy.py
# start minecraft server (don't forget to disable online mode!)
(while true; do printf "time set 0\nweather clear\n"; sleep 10; done) | java -Xmx1024M -Xms1024M -jar server.jar nogui
# start minecraft and configure it to connect to 127.0.0.0:4000, the proxy should send all packets to 127.0.0.0:25565
# open up parser.py in your favorite editor and start playing
```

# Basics
I have supplied a basic parser.py, look it up. It has a function called parse, with 3 arguments. The proxy expects to get the modified data returned.

In proxy.py you can change on which host you listen, which port and where to forward everything (again, host and port).

Enter 'quit' to easily kill everithing.

### Example parser that just prints the data coming from the server
```
def parse(src_data, port, origin):
    if origin == 'server':
        print(src_data.hex())
    return src_data
```

# Performace
Absolutely terrible! I call reload() on **every single packet**. To improve this maybe you can add checking if something changed or even a manual command in the bottom in proxy.py.
