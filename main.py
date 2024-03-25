import socket
import ssl
import sys
from bs4 import BeautifulSoup

def fetch_url(url):
    """Fetch a URL using a raw socket with SSL for HTTPS and parse specific HTML elements in a human-readable way."""
    try:
        scheme, url = parse_scheme(url)
        host, path = parse_url(url)
        port = 443  # HTTPS default port
        context = ssl.create_default_context()

        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
                ssock.send(request.encode())

                byte_buffer = bytearray()
                while True:
                    data = ssock.recv(1024)
                    if not data:
                        break
                    byte_buffer += data

                response = byte_buffer.decode('utf-8', errors='replace')
                html_content = strip_headers(response)
                soup = BeautifulSoup(html_content, 'html.parser')

                # Process and print the content in a human-readable way
                for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'li']):
                    if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        print('\n' + element.text)
                        print('-' * len(element.text))  # Underline for headers
                    elif element.name == 'p':
                        print('\n' + element.text)
                    elif element.name == 'a':
                        print(f"\nURL: {element.get('href')}")
                    elif element.name in ['ul', 'li']:
                        # Indent list items for readability
                        if element.name == 'li':
                            print(f"  - {element.text}")
                        else:
                            print(element.text)  # For ul, just print the text if needed
                    # print()  # Extra newline for spacing

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
  python3 main.py -u <URL>    # Make an HTTP or HTTPS request to the specified URL and print the response
  python3 main.py -h          # Show this help""")


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
