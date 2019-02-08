echo "Y=${1}" > headerdll.py
python test_client.py > log/try_${1}.txt
