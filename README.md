# PiBot

Quick & dirty raspberry pi interface via websockets.

Controls:

* [ITEAD Sim800 GSM shield](https://www.itead.cc/wiki/RPI_SIM800_GSM/GPRS_ADD-ON_V2.0)
* (todo: Divoom Timebox, sys, imap, ...)

Use the socket client: **./client_www/ws.html** or connect a websocket and launch raw AT commands via:
```
phone,<COMMAND>
```
(Without the preceding "AT", e.g.: "phone,+CSQ")


Python 3.5 - needed modules:

- PyBluez

- tornado

- pyserial

- pyserial-asyncio