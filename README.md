# linux-scannetports
Scan tcp/udp port

What to scan is defined through a config file
#### Example:
```
192.168.1.2 server1 tcp 80,443,111,2049
192.168.1.16 server2 tcp 22,25,53
192.168.1.16 server2 udp 123
192.168.1.11 server3 tcp 22,80,443,389,636,88,464,53
192.168.1.11 server3 udp 123
192.168.1.12 server4 tcp 22,80,443,389,636,88,464,53
192.168.1.12 server4 udp 123
```

#### Usage:
```
Usage: scannetport.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --file=FILENAME
                        filename to read [default: hosts]
  -c, --closed          Print only closed connections [default: False]
  -o, --open            Print only open connections [default: False]
  -u, --unresoved       Print only open connections [default: False]
```
