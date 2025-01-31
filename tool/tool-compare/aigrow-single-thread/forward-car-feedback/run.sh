rm -rf result_thread
rm -rf aigerfile_thread
rm -rf temp
rm -rf res_log
chmod +x generate_car.sh
chmod +x re_generate_car.sh
chmod +x validation_car.sh
chmod +x bin/aigtoaig
chmod +x bin/simplecar
mkdir result_thread
mkdir aigerfile_thread
mkdir temp
mkdir res_log
python3 feedback_car.py
