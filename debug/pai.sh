target='121312'
while [ 1 ]
do 
    python wicked_maker.py > wicked1.txt && echo target: &&time java -jar ../static/workplace/users/$target/code.jar < wicked1.txt >acc.txt && echo cxc: &&time java -jar ../static/workplace/users/cxc/code.jar < wicked1.txt >stdout.txt && diff acc.txt stdout.txt
done