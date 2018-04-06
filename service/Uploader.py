#!/usr/bin/env python

import socket
import os
import stat


class Uploader:

	def __init__(self, sd: socket.socket, fd: int):
		self.sd = sd
		self.fd = fd

	def start(self):

		try:
			filesize = os.fstat(self.fd)[stat.ST_SIZE]
		except OSError as e:
			print(f'Something went wrong: {e}')
			raise e
		# Calcolo i chunk
		nchunk = filesize / 4096
		# Verifico se il file si divide esattamente nei chunk
		if (filesize % 4096) != 0:
			nchunk = nchunk + 1

		nchunk = int(nchunk)

		# Invio identificativo al peer
		response = "ARET" + str(nchunk).zfill(6)
		self.sd.send(response.encode())

		for i in range(nchunk):
			data = os.read(self.fd, 4096)
			#print(f'Letti {len(data)} bytes da file: {data}')
			readed_size = str(len(data)).zfill(5)
			print(f'invio {readed_size} bytes')
			self.sd.send(readed_size.encode())
			self.sd.send(data)
		os.close(self.fd)
