tnd = op.TouchNetDiscovery

parCollection = tnd.par
parCollection.Alias = ""
parCollection.Initialize.pulse()
parCollection.Enable = 0
parCollection.Mode.menuIndex = 1
parCollection.Discport = 9199
parCollection.Searchforever = 1

tnd.op("DiscUCastOut").par.address = ""

tnd.op("TouchNetDiscovery").par.file = ""
tnd.op("TouchNetDiscovery").par.syncfile = 0

tnd.op("ParHandler").par.file = ""
tnd.op("ParHandler").par.syncfile = 0

op.TouchNetDiscovery.save("../Build/TouchNetDiscovery.tox")