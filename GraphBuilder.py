import datetime as dt
import ftplib, io, requests, time
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

count = 1
ftp = ftplib.FTP()
username, password, ip, port = io.open("login.txt").readline().split(',')
time1 = time.time()


def connectFTP(ip_in, port_in, username_in, password_in):
    ftp.connect(ip_in, int(port_in))
    ftp.login(username_in, password_in)
    print(ftp.getwelcome(), "  ", dt.datetime.now().ctime())


def gethouselog(txturl, file_save):
    r = requests.get(txturl, allow_redirects=True)
    open(file_save, 'wb').write(r.content)


def logtoarray(filename, xarrmin, xarrmax, yarrmin,yarrmax):  # take house_log.txt and return it as an array of temperatures #min and max x and y values
    # in read line
    gethouselog('http://andrewlcs.ddns.net/house_log.txt', 'house_log.txt')
    file = io.open(filename)
    array = []
    arraytime = []
    all_lines = file.readlines()
    num_entries = len(all_lines)
    for i, v in enumerate(all_lines[-89:]):
        arraytime.append(v[xarrmin:xarrmax])  # x axis data
        array.append(float(v[yarrmin:yarrmax]))  # y axis data
    print("Array complete at " + str(round(time1 - time.time(), 2)))
    return [arraytime, array]


def makeGraph(twodarrayXY, filename, labelX, labelY, title):
    arr1, arr2 = twodarrayXY
    x = np.array(arr1[-89:])
    y = np.array(arr2[-89:])
    ax = plt.gca()
    plt.xticks(rotation=45)
    plt.plot(x, y)

    ax = plt.gca()
    temp = ax.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::4]))
    for label in temp:
        label.set_visible(False)

    plt.title(dt.datetime.now().ctime() + "   " + title)

    plt.axvline(x="16.45", color="k")
    plt.axvline(x ="06.45", color='y')
    plt.xlabel(labelX)
    plt.ylabel(labelY)
    plt.savefig(filename)
    file = open(filename, 'rb')
    ftp.storbinary('STOR ' + filename, file)
    plt.close()
    print("Graph done" + str(round(time1 - time.time(), 2)))


def run_graph():
    gethouselog('http://andrewlcs.ddns.net/house_log.txt', 'house_log.txt')
    connectFTP(ip, port, username, password)
    print("login finished at " + str(round(time1 - time.time(), 2)))

    makeGraph(logtoarray('house_log.txt', 5, 10, 0, 4), 'temp.png', 'Time', 'Temp(c)', '  Inside Temperature')
    makeGraph(logtoarray('house_log.txt', 5, 10, 22, 25), 'outside.png', 'Time', 'Temp(c)', '  Outside Temperature')
    print("Success")
    time2 = time.time()
    print("\nFinsihed.. logging off.  Took ", round(time2 - time1, 2), " seconds")


def graph_loop():
    counter = 0
    while True:
        run_graph()
        counter += 1
        print(str(counter) + " times looped. Time:", dt.datetime.now().strftime('%H:%M , %d/%m/%y'))
        sleep(1800)

graph_loop()

