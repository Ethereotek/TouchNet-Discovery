import json
import socket
		
DiscMCastOut = op("DiscMCastOut")		# used for sending discovery announcement
DiscUCastOut = op("DiscUCastOut")		# used for sending to server once it has been found
PeersTable = op("Peers")
DiscoveryTimer = op("DiscoveryTimer")
Parent = op.TouchNetDiscovery
Mode = Parent.par.Mode
# Alias = tdu.Dependency(Parent.par.Alias.eval()).val
Alias = Parent.par.Alias
SearchForever = Parent.par.Searchforever

Hostname = socket.gethostname()
# multicast has to be sent on physical NIC
# for now, IPAddress = 127.0.0.1 so that server sends to localhost
#IPAddress = Parent.par.Localaddress.eval()
IPAddress = "127.0.0.1"

Name = project.name 
TouchNetPort = 22099
if Parent.par.Touchnet:
	pass


DiscMCastPort = 9099	# same for in/out, meaning sender will receive its own messages
DiscUCastPort = Parent.par.Discport.val#9199

def HandleUDPMessage(message):
		# try to decode the packet
		# if it raises an error, payload is malformed
	try:
		payload = json.loads(message)
	except:
		raise Exception("Error executing def HandlePacket() >> payload can not be decoded")
			# upon deployment, just pass
		return -1
	else:
		pType = str(payload["type"])
		method_map[pType](payload)
		# events.emit(str(pType), payload)
		return 0

def SendDiscovery():
	# hostname = socket.gethostname()
	# name = project.name
	payload_dict = {
		"type":1,
		"alias":Alias.eval(),
		"hostname":Hostname,
		"address":IPAddress,
		"name":Name,
		"discPort":DiscUCastPort,
		"tnPort":TouchNetPort
		}
	payload_string = json.dumps(payload_dict)

	DiscMCastOut.send(payload_string, terminator="")
	# print("Client has sent discovery packet")
	# return "Success >> Client has sent Discovery Packet"
	
def HandleDiscoveryAnnc(payload):
		# get the alias
	peerAlias = payload["alias"]

		# if alias is empty
	if not peerAlias:
		return 3
		# if alias is self, return
	if peerAlias == Alias.eval():
		return 2

		# test if alias has already been discovered
	aliasInPeers = PeersTable.findCell(peerAlias, cols=["Alias"])

		# if alias has been discovered, return
	if aliasInPeers:
		return 1
	
	# if not aliasInPeers:
	# 	return 3

		# unpack rest of payload
	peerHost = payload["hostname"]
	peerAddress = payload["address"]
	peerName = payload["name"]
	peerPort = payload["discPort"]
	peerTnPort = payload["tnPort"]

	# if peerAlias != Alias:

		# think if there's a way to unpack all the elements of the 
		# udp packet into a list that can be passed to appendRow()
		# or other necessary func

		#aliasInPeers = PeersTable.findCell(peerAlias, cols=["Alias"])
		# hostInPeers = PeersTable.findCell(peerHost, cols=["Host Name"])
		# addressInPeers = PeersTable.findCell(peerAddress, cols=["IP"])
		# nameInPeers = PeersTable.findCell(peerName, cols=["Project Name"])

	# For testing purposes, we can add same client multiple times
			# Upon deployment, this will be uncommented
		
		# If client already added, pass
		# otherwise, append client and send DiscoveryResponse packet
		# if aliasInPeers:
		# 	pass
		# else:
		
		# add to PeersTable
	PeersTable.appendRow([peerAlias, peerHost, peerAddress, peerTnPort, peerName])

		# if a client, send peer notification
		# if a server, send discovery response
	# SendPeerNotification(peerAddress, peerPort)

	if Mode.menuIndex == 1:
		SendPeerNotification(peerAddress, peerPort)
	elif Mode.menuIndex == 0:
		SendDiscoveryResponse(peerAddress, peerPort)


			#Comment out before deployment
		# PeersTable.appendRow([peerAlias, peerHost, peerAddress, peerTnPort, peerName])
		# SendDiscoveryResponse(peerAddress, peerPort)

	return 0

def HandleDiscoveryResponse(payload):
		# test if there is already a server present
	serverInPeers = PeersTable.findCell("Server", cols="Alias")

	if not serverInPeers:
			# unpack data and add to peers
		serverHost = payload["hostname"]
		serverAddress = payload["address"]
		serverName = payload["name"]

		PeersTable.appendRow(["Server", serverHost, serverAddress, 22199, serverName])

		if not SearchForever.eval():
			DiscoveryTimer.par.initialize.pulse()
		return 0
	
	return 1

def SendDiscoveryResponse(address, port):
	payload_dict = {
		"type":2,
		"alias":Alias.eval(),
		"hostname":Hostname,
		"address":IPAddress,
		"name":Name
	}
	
	payload_string = json.dumps(payload_dict)

		# assign peer address and port to unicast send
	DiscUCastOut.par.address = address
	DiscUCastOut.par.port = port

		# assigning a new value to the UDP DAT port is not very fast
		# the sending of the message has to be delayed by a frame
		# Because this happens in a callback, we also need the full path
		# to the discovery unicast out DAT, hence all this silliness
	DiscUCastOut_FullPath = DiscUCastOut.path
	delaySend = 'op(args[0]).send(args[1], terminator="")'
	run(delaySend, DiscUCastOut_FullPath, payload_string,delayFrames = 1)

	
	return 0
	
def SendPeerNotification(address, port):

	payload_dict = {
		"type":1,
		"alias":Alias.eval(),
		"hostname":Hostname,
		"address":IPAddress,
		"name":Name,
		"discPort":DiscUCastPort,
		"tnPort":TouchNetPort
		}

	payload_string = json.dumps(payload_dict)

	DiscUCastOut.par.address = address
	DiscUCastOut.par.port = port
	DiscUCastOut.send(payload_string, terminator="")


method_map = {
	"1":HandleDiscoveryAnnc,
	"2":HandleDiscoveryResponse
}