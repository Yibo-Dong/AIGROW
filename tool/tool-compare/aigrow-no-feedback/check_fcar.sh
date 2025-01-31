# ./bin/aigtoaig aigerfile/gen$1.aag aigerfile/gen$1.aig
timeout 2h ./bin/simplecar -f -dead -propagate -muc -e "aigerfile/gen$1.aig" res_log

echo $?