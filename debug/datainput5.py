import sys, time

def testOneSample(testfile_path):
    inputs = open(testfile_path, "r", encoding="utf-8").readlines()
    start_time = time.time()
    for line in inputs:
        if line.strip() == "":
            break
        command_time = float(line.strip("[").split("]")[0])
        command = line.strip("[").split("]")[1].strip()
        cur_time = time.time() - start_time
        if cur_time < command_time:
            time.sleep(command_time - cur_time)
        sys.stdout.write(command + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    testfile_path = "stdin.txt"
    args = sys.argv
    if len(args) >= 2:
        testfile_path = args[1]
    testOneSample(testfile_path)