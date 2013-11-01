function killer()
{
i=`lsof -i tcp:$port|grep LISTEN`
i=`echo $i|cut -d ' ' -f 2`
#print $i
kill -9 $i 2>/dev/null
}
for port in $(seq 6001 6004)
do
killer
done
