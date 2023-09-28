#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        STATUS_200 = "HTTP/1.1 200 OK\r\n"
        STATUS_301 = "HTTP/1.1 301 Move Permanently\r\n"
        STATUS_404 = "HTTP/1.1 404 Not Found\r\n"
        STATUS_405 = "HTTP/1.1 405 Method Not Allowed\r\n"

        requestDetails = self.data.decode('utf-8').split()
        requestType = requestDetails[0]
        requestPath = requestDetails[1]

        #print(requestPath)

        # if method is not GET
        if (requestType != "GET"):
            self.request.sendall(bytearray(STATUS_405, 'utf-8'))
            return
        
        # else it is a GET method
        else:
            # check if path ends with "/"
            if (requestPath[-1] != "/") and ("." not in requestPath.split("/")):
                newRequestPath = requestPath + "/"
                self.request.sendall(bytearray(f"{STATUS_301}Location:{newRequestPath}\r\n", "utf-8"))
                return
            
            # check if the directory is empty
            dotCount = 0
            for file in requestPath.split("/"):                
                if "." in file:
                    dotCount += 1
            if dotCount < 1:
                #print("executed")
                requestPath += "index.html"
            # add only files in www can be access
            requestPath = "./www" + requestPath
            if requestPath[-1] == "/":
                requestPath = requestPath[:-1]
            #print(requestPath)
            # check if file exist
            if os.path.exists(requestPath):
                contentType = ""
                # check for css or html
                if (requestPath.endswith(".html")):
                    contentType = "Content-type: text/html\r\n\r\n"
                elif (requestPath.endswith(".css")):
                    contentType = "Content-type: text/css\r\n\r\n"
                else:
                    contentType = "application/octet-stream\r\n\r\n"
                
                # read file
                f = open(requestPath, "r")
                content = f.read()
                f.close()

                # send status code and content
                self.request.sendall(bytearray(STATUS_200+contentType+content, "utf-8"))
                return
            # if not it is error 
            else:
                self.request.sendall(bytearray(STATUS_404,"utf-8"))
                return
        #print(requestDetails)
        #self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
