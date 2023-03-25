import TouchNetDiscovery as TND

	# create an event emitter object
	# the call to th EventEmitter comes from the CHOP Execute

Parent = op.TouchNetDiscovery
Mode = Parent.par.Mode		# server = 0, client = 1
DiscoveryTimer = op("DiscoveryTimer")
PeersTable = op("Peers")
DiscUCastIn = op("DiscUCastIn")			# udp dat for receiving unicast
DiscMCastIn = op("DiscMCastIn")

def Initialize(val):

	# initialize is a pulse

	if val == 0.0:
		# we will only handle when it returns to 0
		PeersTable.clear(keepFirstRow = True)
		Parent.store("ClientAlias", None)
		Parent.store("ClientEnable", 1)
	
	return 0
	
def ManualSend(val):
	if val == 0.0:
		TND.SendDiscovery()

def Enable(val):
		# turn val into integer
	print(Mode.menuIndex)
	val = int(val)
	enableInt = val


		# use value to drive the on/off of discoverytimer
		# pulse the start par either way
			# if it's off, it won't start, so we avoid an if-statement
	DiscoveryTimer.par.active = val
	DiscoveryTimer.par.start.pulse()
	
	# if Mode.menuIndex == 1:
	# 	print(Mode)
	DiscMCastIn.par.active = val
	DiscUCastIn.par.active = val
	# else:
	# 	DiscMCastIn.par.active = 1
	

		# if in client mode, update the state in parent storage
	if Mode.menuIndex == 1: # Mode 1 is Client Mode
		Parent.store("ClientEnable", enableInt)
		return 1
	
	return 0

def HandleMode(val):
	
		# get client alias from dict
	ClientAlias = Parent.storage["ClientAlias"]

	DiscUCastIn.par.active = 0

	Parent.par.Enable = 0

	if Mode.menuIndex == 0:
		DiscMCastIn.par.active = 1
		Parent.par.Alias = "Server"
	else:
		DiscMCastIn.par.active = 0
		Parent.par.Alias = ClientAlias

def HandleAlias(val):
	print(Mode.menuIndex)
	if Mode.menuIndex == 0:
		return
		# if mode is client, store alias and enabled state in storage dict

	Parent.store("ClientAlias", Parent.par.Alias.eval())
	Parent.store("ClientEnable", Parent.par.Enable.eval())

method_map = {
	"Initialize":Initialize,
	"Manualsend":ManualSend,
	"Enable":Enable,
	"Mode":HandleMode,
	"Alias":HandleAlias
}


