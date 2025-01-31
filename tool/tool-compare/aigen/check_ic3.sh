# ./bin/aigtoaig aigerfile/gen$1.aag aigerfile/gen$1.aig
timeout 2h ./bin/IC3 -s < aigerfile/gen$1.aig | tail -n 14
# ./IC3 -s < temp/gen$1.aig | tail -n 14
echo $?