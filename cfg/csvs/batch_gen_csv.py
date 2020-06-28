import csv


def gen_1000():
    for i in range(30000100,30001000):
        cfg_path = 'cfg/cfg/FFFFFF-OBU-' + 'M131101118' + str(i) + '.cfg'
        device_path = 'cfg/device/' + 'M131101118' + str(i) + '.txt'
        with open('./1000.csv', "a+") as file:
            csv_file = csv.writer(file)
            myCsvRow = device_path +',' + cfg_path + '\n'
            file.write(myCsvRow)


def gen_1():
    for i in range(30000100, 30000101):
        cfg_path = 'cfg/cfg/FFFFFF-OBU-' + 'M131101118' + str(i) + '.cfg'
        device_path = 'cfg/device/' + 'M131101118' + str(i) + '.txt'
        with open('./1.csv', "a+") as file:
            csv_file = csv.writer(file)
            myCsvRow = device_path +',' + cfg_path + '\n'
            file.write(myCsvRow)


def gen_200():
    for i in range(30000100, 30000300):
        cfg_path = 'cfg/cfg/FFFFFF-OBU-' + 'M131101118' + str(i) + '.cfg'
        device_path = 'cfg/device/' + 'M131101118' + str(i) + '.txt'
        with open('./200.csv', "a+") as file:
            csv_file = csv.writer(file)
            myCsvRow = device_path +',' + cfg_path + '\n'
            file.write(myCsvRow)


def gen_500():
    for i in range(30000100, 30000600):
        cfg_path = 'cfg/cfg/FFFFFF-OBU-' + 'M131101118' + str(i) + '.cfg'
        device_path = 'cfg/device/' + 'M131101118' + str(i) + '.txt'
        with open('./500.csv', "a+") as file:
            csv_file = csv.writer(file)
            myCsvRow = device_path +',' + cfg_path + '\n'
            file.write(myCsvRow)

def gen_sn():
    for i in range(30000100, 30000110):
        with open('./sn.csv', "a+") as file:
            csv_file = csv.writer(file)
            myCsvRow = 'M131101118' + str(i) + '\n'
            file.write(myCsvRow)


if __name__ == '__main__':
    gen_1()
    gen_200()
    gen_500()
    gen_1000()
