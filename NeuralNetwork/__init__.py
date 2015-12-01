import neuralnetwork

mynet = neuralnetwork.searchnet('nn.db')
# mynet.maketables()
wWorld, wRiver, wBank = 101, 102, 103
uWorldBank, uRiver, uEwarth = 201, 202, 203
mynet.generatehiddennode([wWorld, wBank], [uWorldBank, uRiver, uEwarth])
for c in mynet.con.execute("SELECT * FROM wordhidden"): print c
print "------------------"
for c in mynet.con.execute("SELECT * FROM hiddenurl"): print c
