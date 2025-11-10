import tkinter as tk
from tkinter import filedialog
from lxml import etree

# Hide the main tkinter window
root = tk.Tk()
root.withdraw()

# Ask user to select an XML file
xml_file = filedialog.askopenfilename(
    title="Select Moodle XML file",
    filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
)

if not xml_file:
    print("No file selected, exiting.")
    exit()

# Ask where to save the CSV
csv_file = filedialog.asksaveasfilename(
    title="Save CSV as",
    defaultextension=".csv",
    filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
)

if not csv_file:
    print("No save location selected, exiting.")
    exit()

# Parse the XML file
with open(xml_file, 'rt', encoding='utf-8') as f:
    tree = etree.parse(f)

with open(csv_file, "w", encoding='utf-8') as fw:
    for question in tree.iter('question'):
        fw.write("NewQuestion,MC\n")

        answers = question.findall('answer')
        for node in question.iter():
            if node.tag == 'name':
                for subnode in node.iter():
                    if subnode.tag == 'text':
                        fw.write("Title,")
                        fw.write(subnode.text or "")
                        fw.write("\n")
            elif node.tag == 'questiontext':
                for subnode in node.iter():
                    if subnode.tag == 'text':
                        fw.write("QuestionText,")
                        text = subnode.text or ""
                        fw.write(f'"{text}"\n')

        for answer in answers:
            answerweight = answer.attrib.get('fraction', '')
            answertext = answer.find('text')
            text = answertext.text if answertext is not None else ""
            fw.write(f"Option,{answerweight},\"{text}\"\n")

print(f"✅ Conversion complete!\nSaved to: {csv_file}")
