echo "Getting system stats..."

echo "---Uptime---"

uptime


echo "---Memory usage---"

free | grep Mem -w | awk '{print "memory used :"($3/$2)*100"%\n" "available memory:" ($7/$2)*100"%\n" "total memory:"($2/1000000)"GB\n"}' 

echo "---CPU usage---"
top -b -n 1 | grep Cpu | cut -d "," -f 4 | awk '{print "CPU Usage:" (100 - $1)"%" }'

lscpu | grep "CPU(s)" | awk 'NR==1 {print"total cores:" $2}'



echo "---Top memory usage process---"
ps aux --sort -%mem | head -n 6 | awk '{print $1 "\t" $2 "\t" $4 "\t" $11}'

echo "---Top CPU usage process---"
ps aux --sort -%cpu | head -n 6 | awk '{print $1 "\t" $2 "\t" $3 "\t" $11}'

echo "---Total disk usage---"
df -h | grep / -w | awk '{print "Total: " $2 "\nUsed: "$3" (" ($3/$2)*100"%) " "\nFree: " $4 " (" ($4/$2)*100"%)"}'
