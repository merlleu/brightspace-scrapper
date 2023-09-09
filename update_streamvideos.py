import os
path = input()

def get_files(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.html' in file:
                files.append(os.path.join(r, file))
    return files

def update_file(file):
    try:
        with open(file, "r") as f:
            text = f.read()
    except Exception as e:
        print(e)
        return
    
    p = [
        "https://web.microsoftstream.com/embed/video/",
    ]
    

    for i in p:
        if i not in text:
            continue
        id = text.split(i)[1].split('?')[0][:36]
        
        print(id)

        with open(file.replace(".html", ".url"), "w") as f:
            f.write(f"[InternetShortcut]\nURL=https://web.microsoftstream.com/video/{id}")
        
        os.remove(file)

        

        break

for file in get_files(path):
    update_file(file)