import os
import sys
import cStringIO
import networkx as nx
import matplotlib.pyplot as plt


rootdir = sys.argv[1]

outputOfFiles = ""
outputOfFileSize = {}

for root, subFolders, files in os.walk(rootdir):
    for filename in files:
        filePath = os.path.join(root, filename)
        if filename.endswith(".h") or filename.endswith(".m"):
            #            print "\n%s" % (filePath)
            
            with open( filePath, 'r' ) as f:
                thisFilesContents = f.read()
                clean_filename = filename.split('.')[0]
                outputOfFileSize[clean_filename] = len(thisFilesContents)
                for item in thisFilesContents.split("\n"):
                    if "#import" in item and "<UIKit/UIKit.h>" not in item and "<" not in item:
                        clean_import = item.split('"')[1].split('.')[0]
                        outputOfFiles += "%s\t%s\n" % (clean_filename, clean_import)

#print(outputOfFiles)

e1=cStringIO.StringIO(outputOfFiles)
G1=nx.read_edgelist(e1,delimiter='\t')
d = nx.degree(G1)
#print("\n")
#print(d.keys())
#print("\n")
node_sizes = []
for fileKey in d.keys():
    size_of_node = 1
    if fileKey in outputOfFileSize.keys():
        size_of_node = outputOfFileSize[fileKey]
    node_sizes.append(size_of_node)
#print("\n")
#print(node_sizes)
#print("\n")

pos=nx.spring_layout(G1,k=1,iterations=20)
plt.title(os.path.basename(os.path.normpath(rootdir)))
nx.draw(G1,pos,with_labels=True, node_size=node_sizes)
plt.savefig("visualized_ios_project.png") # save as png
