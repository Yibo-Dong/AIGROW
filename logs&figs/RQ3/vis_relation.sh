abc_dir="$PWD/abc-pdr"
ic3_dir="$PWD/ic3-ref"
bcar_dir="$PWD/backward_car" 
fcar_dir="$PWD/forward_car" 


# deal abc
cp $abc_dir/record.txt $abc_dir/table.txt
python3 deal_record_pdr.py $abc_dir
sed -i -e "s/  */ /g" abc-pdr/table.txt 
sort -r -n -k 4 -t " " $abc_dir/table.txt|grep -e " [1-9][0-9][0-9][0-9]\.\|7200" |head -n 10 > $abc_dir/top.txt
cat $abc_dir/top.txt|wc -l 
python3 deal_relation.py $abc_dir
dot -Tpdf -Nlabel='' $abc_dir/relation.dot -o $abc_dir/relation.pdf

# deal ic3
cp $ic3_dir/record.txt $ic3_dir/table.txt
python3 deal_record_car.py $ic3_dir
sort -r -n -k 4 -t " " $ic3_dir/table.txt|grep -e " [1-9][0-9][0-9][0-9]\.\|7200" |head -n 10 > $ic3_dir/top.txt
cat $ic3_dir/top.txt|wc -l 
python3 deal_relation.py $ic3_dir
dot -Tpdf -Nlabel='' $ic3_dir/relation.dot -o $ic3_dir/relation.pdf

# deal bcar
cp $bcar_dir/record.txt $bcar_dir/table.txt
python3 deal_record_car.py $bcar_dir
sort -r -n -k 4 -t " " $bcar_dir/table.txt|grep -e " [1-9][0-9][0-9][0-9]\.\|7200" |head -n 10 > $bcar_dir/top.txt
cat $bcar_dir/top.txt|wc -l 
python3 deal_relation.py $bcar_dir
dot -Tpdf -Nlabel='' $bcar_dir/relation.dot -o $bcar_dir/relation.pdf

# deal fcar
cp $fcar_dir/record.txt $fcar_dir/table.txt
python3 deal_record_car.py $fcar_dir
sort -r -n -k 4 -t " " $fcar_dir/table.txt|grep -e " [1-9][0-9][0-9][0-9]\.\|7200" |head -n 10 > $fcar_dir/top.txt
cat $fcar_dir/top.txt|wc -l 
python3 deal_relation.py $fcar_dir
dot -Tpdf -Nlabel='' $fcar_dir/relation.dot -o $fcar_dir/relation.pdf

