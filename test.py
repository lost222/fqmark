import subprocess


def exec_cmd(cmd, out=None):
    p = subprocess.Popen(cmd, shell=True, stdout=out, stderr=out)
    p.wait()
    return p


def out_benchfile(threadNum, dir, runtime):

    with open("testmode"+str(threadNum)+".f", "w") as file:
        # set $dir = / tmp
        # set $filesize = 1g
        # set $nthreads = 1
        # set $iosize = 1m
        dir = "set $dir="+dir
        filesize = "set $filesize = 10m"
        nthreads = "set $nthreads = 1"
        iosize = "set $iosize = 5m"
        setList = [dir, filesize, nthreads, iosize]
        setList = [i+"\n" for i in setList]
        file.writelines(setList)
        file.write("\n")

        # define file name = largefile1, path =$dir, size =$filesize, prealloc, reuse
        filesetdefine0 = "define file name="
        filesetdefine2 = ", path =$dir, size =$filesize, reuse "
        for i in range(threadNum):
            filesetname = "largefile" + str(i)
            file.write(filesetdefine0+filesetname+filesetdefine2+"\n")
        file.write("\n")

        # define process name=seqwrite, instances=1
        processDefine = "define process name=seqwrite,instances=1"
        file.write(processDefine+"\n")
        file.write("{"+"\n")

        #   thread name=seqwrite1,memsize=10m,instances=$nthreads
        #   {
        #     flowop write name=seqwrite1,filename=largefile1,iosize=$iosize
        #   }
        #   thread name=seqwrite2,memsize=10m,instances=$nthreads
        #   {
        #     flowop write name=seqwrite2,filename=largefile2,iosize=$iosize
        #   }
        treadDefine0 = "thread name="
        treadDefine2 = ",memsize=10m,instances=$nthreads"
        flowopDefine0 = "flowop write name="
        flowopDefine2 = ",filename="
        filesetdefine3 = ",iosize=$iosize"
        for i in range(threadNum):
            threadName = "write" + str(i)
            filesetName = "largefile" + str(i)
            file.write(treadDefine0+threadName+treadDefine2+"\n")
            file.write("{"+"\n")
            file.write("  "+flowopDefine0+threadName+flowopDefine2+filesetName+filesetdefine3+"\n")
            file.write("}"+"\n")
        file.writelines("}"+"\n")
        file.write("run " + str(runtime))


for i in range(5, 55, 5):
    out_benchfile(i, "/home", 60)
    fileBenchCmd = "filebench -f ./" + "testmode"+str(i)+".f"
    file = open("log"+str(i)+".log", "w")
    exec_cmd(fileBenchCmd, file)
    file.close()
    print("log %d done", i)
