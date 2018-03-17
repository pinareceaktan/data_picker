from googletrans import Translator

translator = Translator()

file = open('swear_list', 'r')

tr_swears = []
for line in file:
    t = line.split()
    # Get rid of \n s in the end of the last element
    t[-1] = t[-1].strip()
    tr_text = translator.translate(' '.join(t), dest='tr').text
    tr_swears.append(tr_text)
file.close()

write_dest = open('tr_swear_list', 'w')

for swear in tr_swears:
    write_dest.write(swear+'\n')

write_dest.close()
