import os
from http.server import BaseHTTPRequestHandler
from routes.main import routes
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        if request_extension is "" or request_extension is ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()
        elif request_extension is ".py":
            handler = BadRequestHandler()
        else:
            handler = StaticHandler()
            handler.find(self.path)
 
        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        content_type = handler.getContentType()
        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', content_type)
        else:
            content = "404 Not Found"

        self.end_headers()

        if content_type.startswith('image'):
            return content
        else:
            return bytes(content, 'UTF-8')


    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)