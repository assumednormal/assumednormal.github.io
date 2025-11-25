import http.server
import socketserver
import os
import sys
import argparse
import socket


def find_available_port(start_port, max_attempts=10):
    """Try to find an available port starting from start_port."""
    for i in range(max_attempts):
        port = start_port + i
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    return None


def main():
    parser = argparse.ArgumentParser(description="Start a local web server for the blog")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on (default: 8000)")
    parser.add_argument("--auto-port", action="store_true", help="Automatically try next port if specified port is in use")
    args = parser.parse_args()
    
    port = args.port
    
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Server running at http://localhost:{port}/")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            if args.auto_port:
                available_port = find_available_port(port)
                if available_port:
                    print(f"Port {port} is already in use. Trying port {available_port}...")
                    with socketserver.TCPServer(("", available_port), handler) as httpd:
                        print(f"Server running at http://localhost:{available_port}/")
                        print("Press Ctrl+C to stop the server")
                        httpd.serve_forever()
                else:
                    print(f"Error: Could not find an available port starting from {port}")
                    sys.exit(1)
            else:
                print(f"Error: Port {port} is already in use.")
                print(f"Try running: python main.py --port {port + 1}")
                print(f"Or use: python main.py --auto-port")
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
