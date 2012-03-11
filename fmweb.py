#!/usr/bin/env python2

import web
import socket
import json

# Default configuration, modify them to map your FMD setting.
fmd_addr = 'localhost'
fmd_port = 10098

urls = (
	'/fmweb/static/(.*)', 'Static',
	'/fmweb/(.*)', 'WebUI',
	'(.*)', 'Error',
)
app = web.application(urls, globals())

class Error:
	def GET(self, path):
		return "Error: Unknown path {0}".format(path)

class Static:
    def GET(self, file):
        try:
            web.header('Cache-Control', 'max-age=2592000')
            f = open('static/'+file, 'r')
            return f.read()
        except:
            return '' # you can send an 404 error here if you want

class WebUI:
	def GET(self, cmd):
		if cmd == '':
			cmd = 'info'
		result = self.runcmd(cmd)
		render = web.template.render('.')
		return render.index(result)

	def runcmd(self, cmd):
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			conn.connect((socket.gethostbyname(fmd_addr), fmd_port))
		except:
			print 'Connect to FMD failed. Is FMD running?'
			return
		res = conn.recv(1024)	# receive welcome info

		conn.send(cmd)
		res = conn.recv(4096)
		conn.send('bye')
		conn.close()

		try:
			return json.loads(res)
		except:
			print res

if __name__ == "__main__":
	app.run()
