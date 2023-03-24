from pymitter import EventEmitter
import TouchNetDiscovery as TND

	# create an event emitter object
	# the call to th EventEmitter comes from the CHOP Execute
events = EventEmitter()


Parent = op.TouchNetDiscovery
Mode = Parent.par.Mode		# server = 0, client = 1
DiscoveryTimer = op("DiscoveryTimer")
PeersTable = op("Peers")
DiscUCastIn = op("DiscUCastIn")			# udp dat for receiving unicast
DiscMCastIn = op("DiscMCastIn")

# the name of each event is the name of the parameter

@events.on("Initialize")
def Initialize(args):

	# initialize is a pulse

	if args[0] == 0.0:
		# we will only handle when it returns to 0
		PeersTable.clear(keepFirstRow = True)
		Parent.store("ClientAlias", None)
		Parent.store("ClientEnable", 1)
	
	return 0
	
@events.on("Manualsend")
def ManualSend(args):
	if args[0] == 0.0:
		TND.SendDiscovery()

@events.on("Enable")
def Enable(args):
		# turn val into integer
	print(Mode.menuIndex)
	enableInt = int(args[0])


		# use value to drive the on/off of discoverytimer
		# pulse the start par either way
			# if it's off, it won't start, so we avoid an if-statement
	DiscoveryTimer.par.active = int(args[0])
	DiscoveryTimer.par.start.pulse()
	
	# if Mode.menuIndex == 1:
	# 	print(Mode)
	DiscMCastIn.par.active = int(args[0])
	DiscUCastIn.par.active = int(args[0])
	# else:
	# 	DiscMCastIn.par.active = 1
	

		# if in client mode, update the state in parent storage
	if Mode.menuIndex == 1: # Mode 1 is Client Mode
		Parent.store("ClientEnable", enableInt)
		return 1
	
	return 0

@events.on("Mode")
def HandleMode(args):
	
		# get client alias from dict
	ClientAlias = Parent.storage["ClientAlias"]
	# ClientEnable = Parent.storage["ClientEnable"]

		# evalulate mode as int to drive other values
	# modeInt = int(args[0])

		# can use mode as an index into the following lists
		# modeStr is the *alias* name
		# enabled is the enable state
		# server has default values, client values will be filled
		# with what was pulled from dict
	# modeStr = ["Server", ClientAlias]
	# enabled = [0, ClientEnable]

		# deactivate receiving unicast if in server mode
	DiscUCastIn.par.active = 0#modeInt

	# Parent.par.Alias = modeStr[modeInt]
	Parent.par.Enable = 0

	if Mode.menuIndex == 0:
		DiscMCastIn.par.active = 1
		Parent.par.Alias = "Server"
	else:
		DiscMCastIn.par.active = 0
		Parent.par.Alias = ClientAlias

@events.on("Alias")
def HandleAlias(args):
	print(Mode.menuIndex)
	if Mode.menuIndex == 0:
		return
		# if mode is client, store alias and enabled state in storage dict

	Parent.store("ClientAlias", Parent.par.Alias.eval())
	Parent.store("ClientEnable", Parent.par.Enable.eval())

	


