#!/usr/bin/python3
# REPO -> https://github.com/parsapoorsh/iirb
from argparse import ArgumentParser

parser = ArgumentParser(
    description="Iran's internet restriction bypass using shadowsocks")
parser.add_argument("spassword",
                    type=str,
                    help="Shadowsocks password for this server")
parser.add_argument("hostname",
                    type=str,
                    help="Domain/IP address of this server")
parser.add_argument(
    "rsserver",
    type=str,
    help="Shadowsocks server outside Iran WITHOUT base64 encode")
parser.add_argument(
    "sport",
    type=int,
    default=80,
    nargs="?",
    help="This server port for shadowsocks proxy. default is 80",
)
args = parser.parse_args()

import os, sys, asyncio
from base64 import urlsafe_b64encode

if os.geteuid() != 0:
    print(
        "You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.",
        file=sys.stderr,
    )
    exit(2)
try:
    import pproxy
except ModuleNotFoundError:
    os.system("pip install pproxy")
finally:
    import pproxy

for ptype in ("tcp", "udp"):
    if (os.system(
            f"iptables -I INPUT -p {ptype} -m {ptype} --dport {args.sport} -j ACCEPT"
    ) != 0):
        print(
            f"There is a problem opening the firewall, please open port {args.sport}/{ptype} manually",
            file=sys.stderr,
        )

servers = [
    pproxy.Server(
        f"ss://chacha20-ietf-poly1305:{args.spassword}@0.0.0.0:{args.sport}")
]

remote = pproxy.Connection(args.rsserver)
hargs = dict(rserver=[remote], verbose=print)
loop = asyncio.get_event_loop()
loop.set_exception_handler(lambda *args, **kwargs: None)
handlers = []
for server in servers:
    handlers.extend((
        loop.run_until_complete(server.start_server(hargs)),
        loop.run_until_complete(server.udp_start_server(hargs)),
    ))

try:
    print(
        f"Share URL: ss://chacha20-ietf-poly1305:{args.spassword}@{args.hostname}:{args.sport}"
    )
    print(
        "Batch export share URL: ss://",
        urlsafe_b64encode(
            f"chacha20-ietf-poly1305:{args.spassword}@{args.hostname}:{args.sport}"
            .encode()).decode(),
        sep="",
    )
    loop.run_forever()
except KeyboardInterrupt:
    exit(0)
