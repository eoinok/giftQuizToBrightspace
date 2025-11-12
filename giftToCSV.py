import re
import tkinter as tk
from tkinter import filedialog

# --- Hide the main tkinter window ---
root = tk.Tk()
root.withdraw()

# --- Ask user to select a GIFT file ---
gift_file = filedialog.askopenfilename(
    title="Select Moodle GIFT file",
    filetypes=[("GIFT Files", "*.gift"), ("Text Files", "*.txt"), ("All Files", "*.*")]
)

if not gift_file:
    print("No file selected, exiting.")
    exit()

# --- Ask where to save the CSV ---
csv_file = filedialog.asksaveasfilename(
    title="Save CSV as",
    defaultextension=".csv",
    filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
)

if not csv_file:
    print("No save location selected, exiting.")
    exit()

# --- Read the entire GIFT file ---
with open(gift_file, 'r', encoding='utf-8') as f:
    content = f.read()

# --- Regex to capture question blocks ---
# Pattern:
# ::q001::Question text { ~Wrong# =Right# ~Wrong# }
pattern = re.compile(
    r"::(?P<qname>[^:]+)::(?P<qtext>.+?)\{(?P<answers>.+?)\}",
    re.DOTALL
)

# --- Write the CSV output ---
with open(csv_file, "w", encoding='utf-8') as fw:
    for match in pattern.finditer(content):
        qname = match.group('qname').strip()
        qtext = match.group('qtext').strip().replace("\n", " ").replace('"', '""')
        answers_block = match.group('answers').strip()

        # Write Brightspace format headers
        fw.write("NewQuestion,MC\n")
        fw.write(f"Title,{qname}\n")
        fw.write(f'QuestionText,"{qtext}"\n')

        # Split answers: each begins with ~ or =
        answer_parts = re.findall(r"([~=])([^#]+)#?", answers_block)

        for symbol, answer_text in answer_parts:
            answer_text = answer_text.strip().replace('"', '""')
            fraction = "100" if symbol == "=" else "0"
            fw.write(f'Option,{fraction},"{answer_text}"\n')

print(f"✅ Conversion complete!\nSaved to: {csv_file}")
