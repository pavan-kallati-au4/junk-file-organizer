import argparse
import os
import shutil
import time
import random

# Function which helps to find whether the date of created/ modified is today, yesterday or earlier


def compareDate(path, flag):
    if flag == 'modifys':
        fileDate = time.localtime(os.path.getmtime(path))
    else:
        fileDate = time.localtime(os.stat(path).st_birthtime)
    todayDate = time.localtime(time.time())
    if fileDate.tm_year == todayDate.tm_year and fileDate.tm_mday == todayDate.tm_mday and fileDate.tm_mon == todayDate.tm_mon:
        # print(fileDate, path)
        return 0
    elif fileDate.tm_year == todayDate.tm_year and fileDate.tm_mday+1 == todayDate.tm_mday and fileDate.tm_mon == todayDate.tm_mon:
        return 1
    else:
        return 2


if __name__ == '__main__':
    allFiles = []
    filesDividedByTime = {
        "today": [],
        "yesterday": [],
        "earlier": []
    }

    parser = argparse.ArgumentParser(
        description="Junk File Organizer Script"
    )
    parser.add_argument(
        '-d', '--dir', help="Enter absolute directory path", default='/Users/pavankallati/Documents')
    parser.add_argument(
        '-o', '--option', help="Enter the option for organized folder", default="extension")
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print("Provide a valid folder path")
        exit()

    if os.path.isdir(args.dir+'/organized'):
        shutil.rmtree(args.dir+'/organized')

    for root, dirs, files in os.walk(args.dir):
        for file in files:
            allFiles.append(root+'/'+file)
    files = {}

    # This helps to organize the folder on the basis of extension
    if args.option == "extension":
        for file in allFiles:
            name, extension = os.path.splitext(file)
            if extension in files:
                files[extension].append(file)
            else:
                files[extension] = []
                files[extension].append(file)
        os.mkdir(args.dir+'/organized')

        for key, values in files.items():
            if key != "":
                os.mkdir(args.dir+'/organized/'+key[1:])
                for file in values:
                    if not os.path.isfile(args.dir+'/organized/' +
                                          key[1:]+'/'+os.path.basename(file)):
                        os.symlink(file, args.dir+'/organized/' +
                                   key[1:]+'/'+os.path.basename(file))
            else:
                os.mkdir(args.dir+'/organized/otherfiles')
                for file in values:
                    if not os.path.isfile(args.dir+'/organized/otherfiles' +
                                          '/'+os.path.basename(file)):
                        os.symlink(file, args.dir+'/organized/otherfiles' +
                                   '/'+os.path.basename(file))
        if(args.dir.endswith("/")):
            print("Path of the organized directory",
                  args.dir[:-1] + '/organized')
        else:
            print("Path of the organized directory", args.dir + '/organized')

    # Organizes the folder according to their size
    elif args.option == "size":
        os.mkdir(args.dir+'/organized')
        os.mkdir(args.dir+'/organized/Bytes')
        os.mkdir(args.dir+'/organized/KB')
        os.mkdir(args.dir+'/organized/MB')
        os.mkdir(args.dir+'/organized/GB')
        for file in allFiles:
            try:
                size = os.path.getsize(file)
                if size < 1024:
                    if not os.path.isfile(args.dir+"/organized/Bytes/"+os.path.basename(file)):
                        os.symlink(file, args.dir+"/organized/Bytes/" +
                                   os.path.basename(file))
                elif size < 1000*1024:
                    if not os.path.isfile(args.dir+"/organized/KB/"+os.path.basename(file)):
                        os.symlink(file, args.dir+"/organized/KB/" +
                                   os.path.basename(file))
                elif size < 1000*1024*1024:
                    if not os.path.isfile(args.dir+"/organized/MB/"+os.path.basename(file)):
                        os.symlink(file, args.dir+"/organized/MB/" +
                                   os.path.basename(file))
                else:
                    if not os.path.isfile(args.dir+"/organized/GB/"+os.path.basename(file)):
                        os.symlink(file, args.dir+"/organized/GB/" +
                                   os.path.basename(file))
            except:
                pass
        if(args.dir.endswith("/")):
            print("Path of the organized directory",
                  args.dir[:-1] + '/organized')
        else:
            print("Path of the organized directory", args.dir + '/organized')

    # Organizes the folder according to their created or modified date
    elif args.option == "createDate" or args.option == "modifiedDate":
        for file in allFiles:
            # print(time.localtime(os.stat(file).st_birthtime), file)
            if args.option == "createDate":
                value = compareDate(file, 'create')
            else:
                value = compareDate(file, 'modifys')
            if value == 0:
                filesDividedByTime["today"].append(file)
            elif value == 1:
                filesDividedByTime["yesterday"].append(file)
            else:
                filesDividedByTime["earlier"].append(file)
        os.mkdir(args.dir+'/organized')
        if len(filesDividedByTime["today"]) != 0:
            os.mkdir(args.dir+'/organized/today')
        if len(filesDividedByTime["yesterday"]) != 0:
            os.mkdir(args.dir+'/organized/yesterday')
        if len(filesDividedByTime["earlier"]) != 0:
            os.mkdir(args.dir+'/organized/earlier')
        for key, values in filesDividedByTime.items():
            if len(values) != 0:
                for file in values:
                    if not os.path.isfile(args.dir+'/organized/' +
                                          key + '/' + os.path.basename(file)):
                        os.symlink(file, args.dir+'/organized/' +
                                   key + '/' + os.path.basename(file))
                    else:
                        os.symlink(file, args.dir+'/organized/' +
                                   key + '/' + str(random.randint(1, 1000)) + os.path.basename(file))
        if(args.dir.endswith("/")):
            print("Path of the organized directory",
                  args.dir[:-1] + '/organized')
        else:
            print("Path of the organized directory", args.dir + '/organized')
