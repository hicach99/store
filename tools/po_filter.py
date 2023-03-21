import sys
from deep_translator import GoogleTranslator

def translate(input=None,source=None,target=None):
    output=None
    try:
        output=GoogleTranslator(source=source, target=target).translate(text=input)
    except:
        pass
    return output
def generate_po(output,data:dict=None):
    f = open(output, "w", encoding="utf-8")
    for key,value in data.items():
        f.write(f'msgid "{key}"\nmsgstr "{value}"\n\n')
    f.close()
if __name__ == "__main__":
    data={}
    args = sys.argv
    # Handling the case when no file is passed
    if len(args) == 1:
        print("Please pass a file to translate")
        sys.exit(1)
    elif len(args) >= 2:
        keys = [ a.split('"')[1] for a in str(open(args[1], encoding='utf8', newline='\n').read()).strip().split('\n') if  a.startswith('msgid') or a.startswith('msgstr')]
        for i in range(0,len(keys),2):
            data[keys[i]]=keys[i+1]
    generate_po(args[2],data=data)