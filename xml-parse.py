import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLParser
from bs4 import BeautifulSoup
import io



def main():


    markup = open("/Users/its/Dropbox/END main folder/END 2015 Cataloging/XML 2015 full/7.27.15.xml")

    soup = BeautifulSoup(markup, "xml")

    masterPubs = []

    for record in soup.find_all("record"):
        # get BOOK
        #r = record.find(tag="245")
        #book = r.find(code="a").get_text()
        
        # get PUBLISHERS
        pubs = []
        names = record.find_all(tag="700")
        for n in names:
            if not n.find(code="4") == None:
                if n.find(code="4").string == "Printed for":
                    pubs.append({'name':n.find(code="a").string})
        if (not pubs==None) and (len(pubs)>0):
            masterPubs.append(pubs)
                    
    
    nodes = []
    links = []
    linksBackUp = []

    for nameList in masterPubs:
        posList = []
        for name in nameList:
            if name in nodes:
                posList.append(nodes.index(name))
            if not name in nodes:
                nodes.append(name)
                posList.append(nodes.index(name))        

        for x in posList:
            for y in posList:    
                if not x==y:
                    link = {"source":x,"target":y,"value":1}
                    linkRev = {"source":y,"target":x,"value":1}
                    if not (link in links) and not (linkRev in links):
                        links.append(link)

    #make JSON
    with open('marc.json', 'w') as outfile:
        #nodes: creates a dictionary around publishers
        #indent: adds pretty print
        json.dump({'nodes': nodes,'links': links},outfile,indent=2)
    

             

if __name__ == "__main__":
    main()

    

