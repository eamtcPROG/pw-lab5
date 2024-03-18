import socket
import ssl
import sys


def fetch_url(url):
    """Fetch a URL using a raw socket with SSL for HTTPS."""
    try:
        scheme, url = parse_scheme(url)
        host, path = parse_url(url)
        port = 443  # HTTPS default port
        context = ssl.create_default_context()

        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
                ssock.send(request.encode())

                response = ""
                while True:
                    data = ssock.recv(1024)
                    if not data:
                        break
                    response += data.decode()

                print(strip_headers(response))
    except Exception as e:
        print(f"Error: {e}")


def parse_scheme(url):
    """Parse the URL scheme (http or https)."""
    if url.startswith("https://"):
        return "https", url[8:]
    elif url.startswith("http://"):
        return "http", url[7:]
    else:
        print("Invalid URL scheme. Only http and https are supported.")
        sys.exit(1)


def parse_url(url):
    """Parse the URL into host and path."""
    host, path = url, "/"
    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    return host, path


def strip_headers(response):
    """Strip headers from an HTTP response."""
    return "\n".join(response.split("\r\n\r\n", 1)[1:])


def show_help():
    """Print the help information."""
    print("""Usage:
  go2web -u <URL>    # Make an HTTP or HTTPS request to the specified URL and print the response
  go2web -h          # Show this help""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]
    if command == '-u' and len(sys.argv) == 3:
        fetch_url(sys.argv[2])
    elif command == '-h':
        show_help()
    else:
        show_help()


if __name__ == "__main__":
    main()
