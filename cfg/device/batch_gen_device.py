
import shutil

for i in range(30000100,30001000):
    filename = 'tr069/data/device/' + 'M131101118' + str(i) + '.txt'
    print(filename)
    shutil.copy("tr069/data/device/M13110111830000026.txt",filename)
    with open(filename, "r") as f1:
        content = f1.read()
    t = content.replace("M13110111830000026", 'M131101118' + str(i))
    with open(filename, "w") as f2:
        f2.write(t)
#%%