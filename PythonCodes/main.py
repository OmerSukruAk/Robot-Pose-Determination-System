import robotPoseDeterminer as rpd
import rpdScenarios as scenarios

rpd.generateDirectory()
inp = 0
path = ""
name = ""
while(inp != 6):
    print(f"1) Examine a video")
    print(f"2) Examine a image folder (.jpg images)")
    print(f"3) Create frames from a video")
    print(f"4) Create video from a image folder (.jpg images)")
    print(f"5) Examine a frame (.jpg image)")
    print(f"6) Exit")

    inp = int(input("\n>>> Select:"))
    
    if (inp == 1):
        path = input("Video path:")
        name = input("Project name:")
        scenarios.examineVideo(path, 0, name, 1)
        print("\n>>"+name+".mp4 created")
    elif(inp == 2):
        path = input("Folder path:")
        name = input("Project name:")
        scenarios.examineFrames(path, 0, name, 1)
        print("\n>>" + name + ".mp4 created")
    elif(inp == 3):
        path = input("Video path:")
        name = input("Project name:")
        rpd.video2Frame(path,name)
        print("\n>> Folder created")
    elif(inp == 4):
        path = input("Folder path:")
        name = input("Project name:")
        rpd.frame2Video(path,(name+".mp4"),1)
        print("\n>>" + name + ".mp4 created")
    elif(inp == 5):
        path = input("Frame path:")
        name = input("Project name:")
        scenarios.examineFrame(path,(name+".jpg"),1,1,name,1)
        print("\n>> Folder created")