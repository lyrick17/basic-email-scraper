#! python3

# This simple program will scrap the email addresses
# from the text copied in a clipboard
# and it would return all the emails in the clipboard (one email per line) 

# NOTE: this program requires a copied text in clipboard before
# running it

import re, pyperclip

# regex for email addresses that will handle
#   (.), (+), (_) characters


emailRegex = re.compile(r'''
[a-zA-Z0-9]{1,1}            # makes sure it starts with alphanum
[a-zA-Z0-9._-]*[a-zA-Z0-9]+ # username
@                           # @ symbol
[a-zA-Z0-9.-]+[.]\w+        # domain and top doomain name
''', re.VERBOSE)

text = pyperclip.paste()

extractedEmail = emailRegex.findall(text)

results = '\n'.join(extractedEmail)

pyperclip.copy(results)

# DEBUGGING:
# print(extractedEmail)
