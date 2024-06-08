target='21374067'
idx=0
while [ 1 ]
do 
    echo "round $idx:"
    python maker14.py ../static/workplace/users/$target/code.jar ./stdin.txt ./stdout.txt ./stderr.txt && python judge_unit4.py ./stdin.txt ./stdout.txt ./stderr.txt
    if [ $? -ne 0 ]; then
        break
    fi
    let idx++
done