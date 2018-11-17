from pydub import AudioSegment
import sys
import os


def getTimeInMilisecond(time, end):
    if time == 'begin':
        return 0
    if time == 'end':
        return end

    arr = time.split(':')
    if len(arr) == 2 :
        tmp = (int(arr[0]) * 60 + int(arr[1])) * 1000
        if tmp < 0:
            tmp = 0
        if tmp > end:
            tmp = end
        return tmp
    else :
        raise Exception("Invalid time expression")

def isPathValid(path):
    result = True
    if not os.access(path, os.W_OK):
        try:
            open(path, 'w').close()
            os.unlink(path)
        except OSError:
            print("Permission Denied")
            result = False
    return True

def isFileExist(path):
    if not os.access(path, os.R_OK):
        return False
    else:
        return True

if len(sys.argv) == 5:
    input_path = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    out_path = sys.argv[4]

    if not isFileExist(input_path):
        print("Input not found")
        sys.exit()

    if not input_path.endswith(".mp3"):
        print("Your input path is invalid")
        sys.exit()

    if not isPathValid(out_path) or not out_path.endswith(".mp3"):
        print("Your output path is invalid")
        sys.exit()

    try:
        sound = AudioSegment.from_mp3(input_path)
        end_time = len(sound)
        start_milisecond = getTimeInMilisecond(start, end_time)
        end_milisecond = getTimeInMilisecond(end, end_time)

        if end_milisecond <= start_milisecond:
            print("End time must be after start time")
            sys.exit()

        selected = sound[start_milisecond:end_milisecond]
        selected.export(out_path, format="mp3")
        print("Done")
    except Exception as ex:
        print("Exception: ", ex)
        sys.exit()
else:
    print("Your command is invalid, Let's try again")
    print("Example : python3 input.mp3 main.py 1:01 2:53 out.mp3")

