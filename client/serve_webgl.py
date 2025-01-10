import sys
from http.server import SimpleHTTPRequestHandler, HTTPServer

'''
Code from https://gist.github.com/vwrs/68d47c974c7b772f342ebfe9a1f88d70
'''

class GzipRequestHandler(SimpleHTTPRequestHandler):
    '''HTTPRequestHandler for gzip files'''

    def end_headers(self):
        '''Set Content-Encoding: gzip for gzipped files'''
        if self.path.endswith('.gz'):
            self.send_header('Content-Encoding', 'gzip')
        super().end_headers()

    def do_GET(self):
        '''Set Content-Encoding and Content-Type to gzipped files'''
        path = self.translate_path(self.path)
        if path.endswith('.js.gz'):
            with open(path, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/javascript')
                self.end_headers()
                self.wfile.write(content)
        elif path.endswith('.wasm.gz'):
            with open(path, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/wasm')
                self.end_headers()
                self.wfile.write(content)
        elif path.endswith('.gz'):
            with open(path, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-Type',self.guess_type(path))
                self.end_headers()
                self.wfile.write(content)
        else:
            super().do_GET()

def serve(port: int):
    '''Run a local HTTP server'''
    httpd = HTTPServer(('localhost', port), GzipRequestHandler)
    print(f"Serving at http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print(f'usage: {sys.argv[0]} [PORT]')
        port = int(sys.argv[1])
        serve(port)
    except Exception as e:
        print('Error:', e)