import xml.etree.ElementTree

# enter number of source file and open it
source_number = input('Enter two digit source number (01 - 50): ')
source_file_path = 'AutoTS_Corpus\DIP2017_source_10' + str(source_number) + '.xml'
xml_tree = xml.etree.ElementTree.parse(source_file_path)
root = xml_tree.getroot()

# save all sentences in a string and save the number of sentences
all_sentences = ''
no_sentences = 0
for s in root.iter('s'):
    # ignore unknown unicode characters
    sentence_text = s.find('content').text.encode('ascii', 'ignore').decode('ascii')
    all_sentences += sentence_text + '\n'
    no_sentences += 1

print(all_sentences)
print(no_sentences)
