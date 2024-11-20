# simple_server.py

import http.server
import socketserver

# Define the handler to serve files
Handler = http.server.SimpleHTTPRequestHandler

# Define the port to listen on
PORT = 8000

# Create the server with the handler and the port
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
