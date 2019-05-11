from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import model_retrieve as mr

class GP(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        # getting result from file
        file = open("files/data.txt", "r") 
        output_data = file.read()
        file.close()

        print("SENT: " + output_data[:100])
        
        self.wfile.write(bytes(output_data, "utf-8"))
        

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        self.wfile.write(response.getvalue())
        input_data = response.getvalue().decode("utf-8")
        print("RECEIVED: " + input_data[:100])

        # Doing some logic with given data
        output_data = mr.returnAverageResult(input_data)
        
        # writing result to file       
        file = open("files/data.txt","w") 
        file.write(output_data) 
        file.close() 
        

def run(server_class=HTTPServer, handler_class=GP, port=9090):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Server running at localhost:9090...')
    httpd.serve_forever()

run()
