# ./bin/aigtoaig aigerfile/gen$1.aag aigerfile/gen$1.aig
timeout 2h ./bin/abc -c "pdr;write_cex -a 'log.cex'" "aigerfile/gen$1.aig"
echo $?