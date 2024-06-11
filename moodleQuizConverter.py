from bs4 import BeautifulSoup
import pandas as pd



def parse_xml(xml_data):
  # Initializing soup variable
    soup = BeautifulSoup(xml_data, 'lxml')

  # Creating column for table
    df = pd.DataFrame(columns=['question', 'title', 'questiontext', 'true'])

  # Iterating through item tag and extracting elements
    questions = soup.find_all('question')
    questions_length = len(questions)
    print(questions_length)
    
    for index, question in enumerate(questions):
        print(question)
            
        
        
       # Adding extracted elements to rows in table
        #row = {
       #     'qNameText': qNameText,
       #     'qText': qText,
       #
       # df = df.append(row, ignore_index=True)
       # print(f'Appending row %s of %s' % (index+1, items_length))

    #return df

with open('sample.xml', 'r') as f:
    file = f.read() 

mydf = parse_xml(file)
#print(mydf)
