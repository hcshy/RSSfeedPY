import http.server
import ssl
import json
from urllib.parse import urlparse
from datetime import datetime, timezone
import configparser

class MyHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path).path
        if parsed_path == '/rss/':
            self._set_headers('application/rss+xml')
            rss_feed = create_rss_feed()
            self.wfile.write(rss_feed.encode('utf-8'))
        elif parsed_path == '/rssitem/':
            self._set_headers('application/json')
            json_response = json.dumps(rss_items[-1])  # Serve the latest RSS item
            self.wfile.write(json_response.encode('utf-8'))

    def do_POST(self):
        parsed_path = urlparse(self.path).path
        if (parsed_path == '/rssitem/'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            rss_item = json.loads(post_data.decode('utf-8'))

            new_item = {
                "PubDate": datetime.now(timezone.utc).strftime('%d %b %Y %H:%M:%S GMT'),
                "Title": rss_item['Title'],
                "Description": rss_item['Description'],
                "Link": rss_item['Link']
            }

            # Replace the existing RSS item with the new one
            rss_items[-1] = new_item
            rss_feed = create_rss_feed()

            self._set_headers('text/plain')
            self.wfile.write(b"RSS item updated successfully.")

def create_rss_feed():
    channel_info = """<rss version="2.0">
    <channel>
        <title><![CDATA[Sample RSS Feed]]></title>
        <link>https://www.example.com</link>
        <description><![CDATA[This is a sample RSS feed generated by Python.]]></description>
        <language>en-us</language>
        <pubDate>{}</pubDate>
    </channel>
</rss>""".format(datetime.now(timezone.utc).strftime('%d %b %Y %H:%M:%S GMT'))

    items = ""
    for item in rss_items:
        items += """<item>
        <title><![CDATA[{0}]]></title>
        <description><![CDATA[{1}]]></description>
        <link>{2}</link>
        <pubDate>{3}</pubDate>
    </item>""".format(item['Title'], item['Description'], item['Link'], item['PubDate'])
    
    return channel_info.replace('</channel>', items + '</channel>')

sample_json_item = {
    "PubDate": datetime.now(timezone.utc).strftime('%d %b %Y %H:%M:%S GMT'),
    "Title": "Sample Title",
    "Description": "Sample Description",
    "Link": "https://example.com"
}

rss_items = [sample_json_item]

def run(server_class=http.server.HTTPServer, handler_class=MyHandler):
    # Read configuration from settings.conf
    config = configparser.ConfigParser()
    config.read('settings.conf')

    host = config.get('DEFAULT', 'host', fallback='localhost')
    port = config.getint('DEFAULT', 'port', fallback=8080)
    certfile = config.get('DEFAULT', 'certfile', fallback='localhost.crt')
    keyfile = config.get('DEFAULT', 'keyfile', fallback='localhost.key')
    
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    
    # Using SSLContext for SSL configuration
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f'Serving HTTPS on {host} port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
