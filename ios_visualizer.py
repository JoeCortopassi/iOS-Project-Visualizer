import os
import sys
import cStringIO
import networkx as nx
import matplotlib.pyplot as plt


rootdir = sys.argv[1]

outputOfFiles = ""

for root, subFolders, files in os.walk(rootdir):
    for filename in files:
        filePath = os.path.join(root, filename)
        if filename.endswith(".h") or filename.endswith(".m"):
            #            print "\n%s" % (filePath)
            
            with open( filePath, 'r' ) as f:
                thisFilesContents = f.read()
                for item in thisFilesContents.split("\n"):
                    if "#import" in item and "<UIKit/UIKit.h>" not in item and "<" not in item:
                        #        print "~~ %s" % (item.strip())
                        clean_filename = filename.split('.')[0]
                        clean_import = item.split('"')[1].split('.')[0]
                        outputOfFiles += "%s\t%s\n" % (clean_filename, clean_import)

print(outputOfFiles)

e1=cStringIO.StringIO(outputOfFiles)
G1=nx.read_edgelist(e1,delimiter='\t')
pos=nx.spring_layout(G1,iterations=100)
plt.title(os.path.basename(os.path.normpath(rootdir)))
nx.draw(G1,pos,node_size=50,with_labels=True)
plt.savefig("visualized_ios_project.png") # save as png
