from dotenv import load_dotenv
import os
import OCRText
import generateMergeFile
import imageProcessing

# load dotenv
load_dotenv()

MERGE_FILE_PATH = os.getenv("MERGE_FILE_PATH")
FILTERED_IMAGES_DIR_PATH = os.getenv("FILTERED_IMAGES_DIR_PATH")
OCR_OUTPUT_FILE_PATH = os.getenv("OCR_OUTPUT_FILE_PATH")
DRAWING_ANNOTATIONS_IMAGES_DIR_PATH = os.getenv("DRAWING_ANNOTATIONS_IMAGES_DIR_PATH")


def parse_mergefile(toedit, mergefile):
    readingcode = open(toedit,"r")
    cached_codefile=readingcode.readlines()
    readingcode.close()

    updated_codefile=cached_codefile

    with open(mergefile) as tomerge:
        for line in tomerge:
            try:
                parsedline=parse_line(line.rstrip(), toedit)
                updated_codefile=update_contents(parsedline,updated_codefile)
            except Exception as e:
                continue
    
    # print (updated_codefile)
    update_codefile(updated_codefile,toedit)

def parse_line(l, toedit)->(int, int, str):
    splitstring=l.split(',')

    linenum=int(splitstring[0]) - 1 # start from 1 index for line num
    index=int(splitstring[1])

    stuff=splitstring[2]
    for i in range(3,len(splitstring)):
        stuff+=","+splitstring[i]

    stuff=stuff.replace("[newline]", "\n")

    comment_char = getCommentChar(toedit)
    stuff=stuff.replace("[comment]", comment_char) # replace with function to get correct comment characters

    return (linenum,index,stuff)

def getCommentChar(code_file):
    commentChar = {"py": " #", 
                   "c": " //",
                   "cpp": " //",
                   "cc": " //",
                   "java": " //",
                   "js": " //",
                   "sql": " --",
                   "rb": " //",
                   "r": " #"}
    
    language = code_file.split(".")[-1]
    if language in commentChar:
        return commentChar[language]
    
    # default comment type 
    return " //"


def update_contents(tochange:tuple[int,int,str],contents):
    if (tochange[1]==-1):
        contents[tochange[0]]=contents[tochange[0]].rstrip()
        contents[tochange[0]]+=tochange[2]

    elif (tochange[1]==0):
        contents.insert(tochange[0],tochange[2])
    
    return contents

def update_codefile(contents,writepath):
    with open(writepath,"w") as writefile:
        writefile.writelines(contents)


def main(camera_dir, codefile_path):
    imageProcessing.parseAll(camera_dir)
    for filename in os.listdir(FILTERED_IMAGES_DIR_PATH):
        try:
            file_path = os.path.join(FILTERED_IMAGES_DIR_PATH, filename)
            OCRText.getText(file_path, OCR_OUTPUT_FILE_PATH)
        except Exception as e:
            # print(e)
            continue
    try:
        generateMergeFile.generateToMerge(OCR_OUTPUT_FILE_PATH, 
                                      DRAWING_ANNOTATIONS_IMAGES_DIR_PATH,
                                      MERGE_FILE_PATH)
        
        parse_mergefile(codefile_path, MERGE_FILE_PATH)
    except Exception as e:
        # print(e)
        pass

# main("/home/ronak/Desktop/project-code/utils/annotationImages", "/home/ronak/Desktop/project-code/utils/files/royIQ.py")
# main("C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\annotations", "C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\royIQ.py")
# parse_mergefile("C:\\Users\\zroy1\\SE101\\se101-team-21\\utils\\royIQ.py", "C:\\Users\\zroy1\\SE101\\se101-team-21\\utils\\tomerge.txt")
# parse_mergefile("C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\royIQ.py", "C:\\Users\\haris\\OneDrive\\Desktop\\SE101-2\\se101-team-21\\utils\\tomerge.txt")
# parse_mergefile("C:\\Users\\zroy1\\SE101\\se101-team-21\\src\\tests\\mergeFileTest.py", "C:\\Users\\zroy1\\SE101\\se101-team-21\\src\\tests\\tomerge_test.txt")