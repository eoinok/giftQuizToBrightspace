from lxml import etree

with open('sample.xml', 'rt') as f:
    tree = etree.parse(f)

fw = open("sample.csv", "w")
    
    
for question in tree.iter('question'):
    fw.write("NewQuestion,MC" + "\n")
    
    answers = question.findall('answer')
    for node in question.getiterator():
        if node.tag=='name':
            for subnode in node.getiterator():
                if subnode.tag=='text':
                    fw.write("Title,")
                    fw.write(subnode.text + "\n")
        elif node.tag=='questiontext':
            for subnode in node.getiterator():
                if subnode.tag=='text':
                    fw.write("QuestionText,")
                    fw.write('"' + subnode.text + '"' + "\n")
    for answer in answers:
        attribs = answer.attrib
        answerweight = attribs['fraction']
        answertext = answer.find("text")
        fw.write("Option,")
        fw.write(answerweight)
        fw.write(",")
        fw.write('"' + answertext.text + '"' + "\n")
        
fw.close()
