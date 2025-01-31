rm -rf aigerfile
rm -rf result
rm -rf res_log
chmod +x check_$1.sh
mkdir aigerfile
mkdir result
mkdir res_log

python3 generate_$1.py
