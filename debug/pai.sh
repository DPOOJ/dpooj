target='cxc'
idx=0
while [ 1 ]
do 
    echo "round $idx:"
    python maker15.py ../static/workplace/users/$target/code.jar ./stdin.txt ./stdout.txt ./stderr.txt && python judge_unit4.py ./stdin.txt ./stdout.txt ./stderr.txt
    if [ $? -ne 0 ]; then
        break
    fi
    let idx++
done