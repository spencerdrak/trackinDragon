with open("spencerComp.reg", 'rb') as source_file:
  with open("test.txt", 'w+b') as dest_file:
    contents = source_file.read()
    dest_file.write(contents.decode('utf-16').encode('utf-8'))