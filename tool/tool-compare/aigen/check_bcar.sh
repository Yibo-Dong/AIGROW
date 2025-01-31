# ./bin/aigtoaig aigerfile/gen$1.aag aigerfile/gen$1.aig
timeout 2h ./bin/simplecar -b -e "aigerfile/gen$1.aig" res_log
# 不设置超时
# ./simplecar -b -e "temp/gen$1.aig" temp
echo $?