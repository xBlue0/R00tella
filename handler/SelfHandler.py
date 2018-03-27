#!/usr/bin/env python

import socket
from utils import ip_utils
from service.AppData import AppData
from handler.HandlerInterface import HandlerInterface


class SelfHandler(HandlerInterface):

	def serve(self, request: str, sd: socket.socket) -> None:
		""" Handle the peer request
		Parameters:
			request - the list containing the request parameters
		Returns:
			str - the response
		"""
		command = request[:4]

		if command == "AQUE":
			if len(request) != 212:
				return "Invalid response. Expected: AQUE<pkt_id><ip_peer><port_peer><fileMD5><filename>"

			pktid = request[4:20]
			ip_peer = request[20:75]
			ip4_peer, ip6_peer = ip_utils.get_ip_pair(ip_peer)
			port_peer = request[75:80]
			filemd5 = request[80:112]
			filename = request[112:212].decode('UTF-8').lower().lstrip().rstrip()

			if not AppData.exist_packet(pktid):
				AppData.add_packet(pktid, ip_peer, port_peer)

			if not AppData.exist_peer_files((ip4_peer, ip6_peer, port_peer, filemd5, filename)):
				AppData.add_peer_files((ip4_peer, ip6_peer, port_peer, filemd5, filename))

			print(f'Response from {ip4_peer}|{ip6_peer} port {port_peer} --> File: {filename} MD5: {filemd5}')


		elif command == "ANEA":
			if len(request) != 80:
				return "Invalid response. Expected: ANEA<pkt_id><ip_peer><port_peer>"

			pktid = request[4:20]
			ip_peer = request[20:75]
			ip4_peer, ip6_peer = ip_utils.get_ip_pair(ip_peer)
			port_peer = request[75:80]

			if not AppData.exist_packet(pktid):
				AppData.add_packet(pktid, ip_peer, port_peer)

			if not AppData.is_neighbour((ip4_peer,ip6_peer,port_peer)):
				AppData.add_neighbour((ip4_peer,ip6_peer,port_peer))

			print(f'New neighbour founded: {ip4_peer}|{ip6_peer} port {port_peer}')

		elif command == "ARET":
			pass

			#memorizza pacchetto

			#ricevi pacchetto via socket

			#leggi pacchetto

		sd.close()
