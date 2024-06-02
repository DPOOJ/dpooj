target='XuanYu'
while [ 1 ]
do 
    python maker14.py ../static/workplace/users/$target/code.jar ./stdin.txt ./stdout.txt ./stderr.txt && python judge_unit4.py ./stdin.txt ./stdout.txt ./stderr.txt
    if [ $? -ne 0 ]; then
        break
    fi
done