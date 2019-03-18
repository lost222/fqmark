set $dir=/tmp
set $filesize = 1g
set $nthreads = 1
set $iosize = 1m

define file name=largefile0, path =$dir, size =$filesize, prealloc, reuse 
define file name=largefile1, path =$dir, size =$filesize, prealloc, reuse 
define file name=largefile2, path =$dir, size =$filesize, prealloc, reuse 
define file name=largefile3, path =$dir, size =$filesize, prealloc, reuse 
define file name=largefile4, path =$dir, size =$filesize, prealloc, reuse 

define process name=seqwrite,instances=1
{
thread name=write0,memsize=10m,instances=$nthreads
{
  flowop write name=write0,filename=largefile0,iosize=$iosize
}
thread name=write1,memsize=10m,instances=$nthreads
{
  flowop write name=write1,filename=largefile1,iosize=$iosize
}
thread name=write2,memsize=10m,instances=$nthreads
{
  flowop write name=write2,filename=largefile2,iosize=$iosize
}
thread name=write3,memsize=10m,instances=$nthreads
{
  flowop write name=write3,filename=largefile3,iosize=$iosize
}
thread name=write4,memsize=10m,instances=$nthreads
{
  flowop write name=write4,filename=largefile4,iosize=$iosize
}
}
run 60