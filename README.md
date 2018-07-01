# megacli2prom
Megacli to prom textfile exporter. I have created it since my old controller does not report drive details under StorCli.

Example usage:

# crontab -l
* * * * * mkdir -m755 /tmp/textcollector >/dev/null 2>&1 ; /usr/local/sbin/megacli.py > /tmp/textcollector/megacli.prom
