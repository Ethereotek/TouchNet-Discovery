tnd = op.TouchNetDiscovery
tnd.op("DiscUCastOut").par.address = "127.0.0.1"

tnd.op("TouchNetDiscovery").par.file = "../Python/Tox-Protocol-Modules/TouchNetDiscovery.py"
tnd.op("TouchNetDiscovery").par.syncfile = 1

tnd.op("ParHandler").par.file = "../Python/Tox-Protocol-Modules/TouchNetDiscovery.py"
tnd.op("ParHandler").par.syncfile = 1


