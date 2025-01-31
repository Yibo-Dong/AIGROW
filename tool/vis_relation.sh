mkdir -p RQ3_result/abc-pdr
mkdir -p RQ3_result/ic3-ref
mkdir -p RQ3_result/backward_car
mkdir -p RQ3_result/forward_car

cp pdr-feedback/result_thread/record.txt RQ3_result/abc-pdr/
cp ic3ref-feedback/result_thread/record.txt RQ3_result/ic3-ref/
cp forward-car-feedback/result_thread/record.txt RQ3_result/forward_car/
cp backward-car-feedback/result_thread/record.txt RQ3_result/backward_car/

cd RQ3_result
./vis_relation.sh