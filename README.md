### PyQt6 matplotlib streaming data visualization

Simple and generic TCP server + PyQt5 client for visualizing stream data.
Uses threading module because I find it to be less convoluted than asyncio. Uses socketserver and sockets.
Focus is simplicity and ease of application to a variety of use cases.

server.py -> basic socketserver.TCPServer that sends random integers over the connection.
client.py -> GUI dashboard and client, refresh rate of ~10Hz (adjustable) plotting integers with matplotlib.
flake.nix -> dependency management

Most likely extremely broken, only using this for exploration.
