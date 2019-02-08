echo "Y=${1}" > headerdll.py
python test_server.py > log/try_${1}.txt
