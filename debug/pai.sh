target='21374067'
while [ 1 ]
do 
    python maker13.py ../static/workplace/std/code13.jar ./stdin.txt ./stdout.txt ./stderr.txt && python judge_unit4.py ./stdin.txt ./stdout.txt ./stderr.txt
    if [ $? -ne 0 ]; then
        break
    fi
done