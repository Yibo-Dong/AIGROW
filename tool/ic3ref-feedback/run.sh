rm -rf result_thread
rm -rf aigerfile_thread
rm -rf temp
chmod +x validation_ic3.sh
chmod +x generate_thread.sh
chmod +x re_generate_thread.sh
chmod +x bin/aigtoaig
mkdir result_thread
mkdir aigerfile_thread
mkdir temp
python3 feedback_ic3.py 2>/dev/null