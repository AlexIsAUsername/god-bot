
striped_bible_lines = []

with open("kjv.txt", "r") as f:
    lines = f.readlines()
    
    for line in lines:     
        # print(line)
        parts = line.split("\t")
        # print(parts[1])
        text = parts[1]
                
        
        striped_bible_lines.append(text)
    


punc = ["[","]",":",",",";","’","—","!","(", ")","?"]

cleaned_bible_lines = []

for line in striped_bible_lines:
    
    temp_line = line
    
    for mark in punc:
        temp_line = temp_line.replace(mark, "", -1)
        
    temp_line = temp_line.replace("\n", " ", -1)
    
    temp_line = temp_line.lower()
    


    cleaned_bible_lines.append(temp_line)

clean = open("kjvc.txt","w")



for line in cleaned_bible_lines:
    clean.write(line)


clean.close()

print("got here")