import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

# Set up logging to log the webhook data to a file
logging.basicConfig(filename='webhook_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse the incoming POST request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Log the raw JSON payload
        try:
            payload = post_data.decode('utf-8')
            json_data = json.loads(payload)
            logging.info(f"Received webhook: {json.dumps(json_data, indent=4)}")
        except json.JSONDecodeError:
            logging.error(f"Failed to decode JSON: {post_data}")

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'status': 'success', 'message': 'Webhook received'}
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=WebhookHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()