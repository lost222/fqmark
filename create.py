import subprocess


def exec_cmd(cmd, out=None):
    p = subprocess.Popen(cmd, shell=True, stdout=out, stderr=out)
    p.wait()
    return p


def out_benchfile(threadNum, dir):

    with open("testmode"+str(threadNum)+".f", "w") as file:
        # set $dir=/tmp
        # set $nfiles=50000
        # set $meandirwidth=100
        # set $meanfilesize=16k
        # set $iosize=10m
        # set $nthreads=16
        dir = "set $dir="+dir
        nfiles = "set $nfiles=50000"
        meandirwidth = "set $meandirwidth=100"
        meanfilesize = "set $meanfilesize=16k"
        nthreads = "set $nthreads = 1"
        iosize = "set $iosize = 5m"
        setList = [dir, nfiles,meandirwidth, meanfilesize, nthreads, iosize]
        setList = [i+"\n" for i in setList]
        file.writelines(setList)
        file.write("set mode quit firstdone")
        file.write("\n")

        # define fileset name=bigfileset,path=$dir,size=$meanfilesize,entries=$nfiles,dirwidth=$meandirwidth
        fileSetDefile = "define fileset name=bigfileset,path=$dir,size=$meanfilesize,entries=$nfiles,dirwidth=$meandirwidth"
        file.write(fileSetDefile + "\n")

        # define process name=filecreate,instances=1
        processName = "Wpro"
        processDefine = "define process name="+processName+",instances=1"
        file.write(processDefine+"\n")
        file.write("{"+"\n")

        #   thread name=filecreatethread,memsize=10m,instances=$nthreads
        #   {
        #     flowop createfile name=createfile1,filesetname=bigfileset,fd=1
        #     flowop writewholefile name=writefile1,fd=1,iosize=$iosize
        #     flowop closefile name=closefile1,fd=1
        #   }

        treadDefine0 = "thread name="
        treadDefine2 = ",memsize=10m,instances=$nthreads"

        flowCreate0 = "flowop createfile name="
        flowCreate2 = ",filesetname=bigfileset,fd=1"

        flowopDefine0 = "flowop writewholefile name="
        flowopDefine2 = ",fd=1,iosize=$iosize"

        flowopClose0 = "flowop closefile name="
        flowopClose2 = ",fd=1"

        for i in range(threadNum):
            threadName = "write" + str(i)
            file.write(treadDefine0+threadName+treadDefine2+"\n")
            file.write("{"+"\n")
            # create flow op
            file.write(flowCreate0+"create"+str(i)+flowCreate2+"\n")

            # write flow op
            file.write(flowopDefine0+"writeOp"+str(i)+flowopDefine2+"\n")

            # close flow op
            file.write(flowopClose0+"close"+str(i)+flowopClose2+"\n")

            file.write("}"+"\n")
        file.writelines("}"+"\n")
        file.write("\n")
        file.write("run ")


data = open("data.txt", "w")

for i in range(10, 80, 5):
    out_benchfile(i, "/home")
    fileBenchCmd = "filebench -f ./" + "testmode"+str(i)+".f"
    file = open("log"+str(i)+".log", "w")
    exec_cmd(fileBenchCmd, file)
    file.close()

    data.write("when i=" + str(i) + "\n")
    dataCCmd = "tail -2" + "log"+str(i)+".log"
    exec_cmd(dataCCmd, data)

    print("log done", i)

data.close()