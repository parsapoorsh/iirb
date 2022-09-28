# Iran's internet restriction bypass using shadowsocks

### You need two VPS with Ubuntu operating system.
One in Iran, for example, has the name VPS1 and the IP address 1.2.3.4
One outside of Iran, for example, has the name VPS2 and the IP address 5.6.7.8, or you can use other Shadowsocks servers that VPS1 has access to.

This method works like this, you connect to VPS1 from your device in Iran, VPS1 transfers data to VPS2 and VPS2 sends data to the destination and vice versa.

- Note 1: You need a root terminal, enter the root terminal with the `sudo bash` command.
- Note 2: It is better to use port `80` or `443` for Iranian server.

If you want to build VPS2 yourself, use the following commands:  
`pip install pproxy`  
`screen -S ss-server pproxy -l ss://chacha20-ietf-poly1305:PASSWORD@0.0.0.0:80`  
And exit the environment with `ctrl+a` and `d`
- Replace 80 with port of your choice
- Open the port in firewall with:  
`iptables -I INPUT -p tcp -m tcp --dport 80 -j ACCEPT`  
`iptables -I INPUT -p udp -m udp --dport 80 -j ACCEPT`  

Now on VPS1, use the following commands:  
`wget https://raw.githubusercontent.com/parsapoorsh/iirb/main/iirb.py`  
`screen -S ss-server python3 iirb.py PASSWORD 1.2.3.4 ss://chacha20-ietf-poly1305:PASSWORD@5.6.7.8:80`  
- Replace 5.6.7.8:80 with IP/domain and port of VPS2
- Replace 1.2.3.4 with IP/domain and port of VPS1

Congratulations! Now copy 'Batch export share URL' from VPS1 output and enter it in your device.

You need to install shadowsocks client on your device.  
For Windows: `outline` or `v2rayn`  
For Android: `outline` or `v2rayng`  
For ios: `outline`  
