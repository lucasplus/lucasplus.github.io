from fabric.api import *
import fabric.contrib.project as project
import os
import shutil
import sys
import socketserver

from pelican.server import ComplexHTTPRequestHandler

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = '..'
DEPLOY_PATH = env.deploy_path

# Port for `serve`
PORT = 8000

def build():
    """Build local version of site"""
    local('pelican -o {} -s pelicanconf.py'.format(env.deploy_path))

def rebuild():
    """`clean` then `build`"""
    clean()
    build()

def regenerate():
    """Automatically regenerate site upon file modification"""
    local('pelican -o {} -r -s pelicanconf.py'.format(env.deploy_path))

def serve():
    """Serve site at http://localhost:8000/"""
    os.chdir(env.deploy_path)

    class AddressReuseTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()

def reserve():
    """`build`, then `serve`"""
    build()
    serve()

def preview():
    """Build production version of site"""
    local('pelican -o {} -s publishconf.py'.format(env.deploy_path))
