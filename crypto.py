"""
Dimitrios Diamantogiannis
Postgraduate Student
Athens University of Economics and Business
Department of Computer Science
Applied Cryptography
2020-2021
Encrypt (**Vigenere**) and Decrypt (**Kasiski**)
"""

from pathlib import Path
import os

Ic = 0.065
MIN_KEY_LENGTH = 4
MAX_KEY_LENGTH = 8

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Array containing the relative frequency of each letter in the English language
english_frequences = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
					  0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
					  0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
					  0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

# Raw text (Starter) ATTENTION Remove punctuation by hand
plain_path = "insert plain text path here"
# Raw text (Starter) Capitalized
plainCap_path = "insert here capitalized one row plain text path"
# Text Ecrypted Capitalized
cipher_path = "insert cipher text path here"
# Text Decrypted Capitalized 
decrypt_path = "insert decrypted text path here"

"""@ Capitalize the text. Insert filepath."""

def capitalizeMsg(plainInsert):

    # Check if plainCap file exists, if so delete it    
    my_file = Path(plainCap_path)    
    if my_file.is_file():
        os.remove(plainCap_path)

    # open or create plain and cipher files
    plainTxt = open(plainInsert, "r")
    plainCapTxt = open(plainCap_path, "a")

    total_chars = 0

    # Read char by char plain file
    # Capitilize chars
    # Remove spaces and line spaces
    while True:       
        char = plainTxt.read(1)           
        if not char:  
            break        

        if char==" " or char=="\n":
            continue

        plainCapTxt.write(char.capitalize()) 
        total_chars += 1

    plainCapTxt.close()
    plainTxt.close() 

    print ("FILE "+ plainInsert + " CAPITALIZED SUCCESSFULLY IN FILE " + str(my_file) + " " + str(total_chars) + " chars.")

"""@ Count Capitalized chars from file (**isfile==1**) or string (**isfile==0**) """

def countCapLetters(onlyCap, isfile):
    if isfile == 1:
        plainCapTxt = open(onlyCap, "r")

    #letters counter list
    ab_count = []
    total_chars = 0

    #init list [[0,0],[1,0],...,[25,0]]
    for i in range(26):
        ab_count.append([i,0])

    if isfile == 1:#check file
        while True:              
            char = plainCapTxt.read(1)           
            if not char:  
                break 
            ab_count[ord(char)-65][1] += 1 
            total_chars += 1 
            
    else: #check string
        for char in onlyCap:
            ab_count[ord(char)-65][1] += 1
            total_chars += 1
    
    ab_count.sort(key = lambda x: x[1], reverse=True)
    
    for cch in range(26):
        print (chr(ab_count[cch][0] + 65) + " = " + str(ab_count[cch][1]) + " | ", end="")
        if cch % 5 == 0 and cch != 0:
            print()

    if isfile == 1:
        plainCapTxt.close()

    print("LETTERS = "+str(total_chars))
    
    return ab_count

"""@ Encrypt data by inserting plainCap.txt"""

def encryption_Vigenere(plainCapIndi):

    # Check if cipher file exists, if so delete it
    my_file = Path(cipher_path)
    if my_file.is_file():
        os.remove(cipher_path)

    # open or create plain and cipher files
    plainCapTxt = open(plainCapIndi, "r")
    cipherTxt = open(cipher_path, "a")

    # Set the key (for example LIBERTY)
    k = ['L','I','B','E','R','T','Y']
    m = len(k)

    counter_m = 0 # 0 to m

    while True:  
             
        char = plainCapTxt.read(1) 

        if not char:  
            break

        if counter_m == m :
            counter_m = 0
        cipherTxt.write(chr( ((ord(char) + (ord(k[counter_m]))) % 26 ) + 65))
        print(chr( ((ord(char) + (ord(k[counter_m]))) % 26 ) + 65), end="")
        counter_m += 1
    
    print()
    plainCapTxt.close()
    cipherTxt.close()

    print("FILE " + plainCapIndi + " ENCRYPTED SUCCESSFULLY IN FILE " + str(my_file))

"""Call decryption Kasiski"""

def decryption_Kasiski(cipherIndi, subs, ab_sort, m):
    print("\nDECRYPTION \n")
    # Check if decryption file exists, if so delete it
    my_file = Path(decrypt_path)
    if my_file.is_file():
        os.remove(decrypt_path)

    decryptTxt = open(decrypt_path, "a")

    # create sorted list of frequencies
    sorted_freq = []
    for cch in range(26):
        sorted_freq.append([cch, english_frequences[cch]])  
    sorted_freq.sort(key = lambda x: x[1], reverse=True)

    for fr in sorted_freq:
        if chr(fr[0]+65) == "M":
            print()
        print(chr(fr[0]+65) + " = " + str(fr[1]) + " || ", end="")
    print()

    #decrypted subsequencies
    dec_subs = []

    dec_sub = []
    i = 0

    # for each sub find the frequency of each char and replace it with the char of endlish char frequencies e.g. most frequent char will be replaced by 'E' and so on...
    # decrypted subs are in dec_sub
    for sub in subs:
        print("DECRYPTION SUBSEQUENCE "+ str(i+1))
        for char in sub:
            position = 0
            for fre_ch in ab_sort[i]:
                if (ord(char)-65) == fre_ch[0]:
                    dec_sub.append(chr(sorted_freq[position][0]+65))
                    print(chr(sorted_freq[position][0]+65), end="")
                    break
                position += 1 
        print()       
        i += 1
        dec_subs.append(dec_sub)
        dec_sub = []
        
    # concatenate all subsequencies to one depending on the length of the key
    pos = 0
    err_tol = 0
    # some subsequencies might contain one more char than the others. When error tolerance equals m then i don't have any more chars to write
    while err_tol < m:
        for sub in dec_subs:
            if pos < len(sub):
                print(sub[pos], end="")
                decryptTxt.write(sub[pos])
            else:
                err_tol += 1 
        print(" ", end="")       
        pos += 1

    decryptTxt.close()
    # cipherTxt.close()

    print("\nFILE " + cipherIndi + " DECRYPTED SUCCESSFULLY IN FILE " + str(my_file))

"""@ Get the most probable key length"""

def get_key_length(ciphertext):
    ic_table=[]
	# Split ciphertext into subsequencies e.g for ciphertext c = c1c2c3...
    # y1 = c1, cm+1, c2m+1, ...
    # y2 = c2, cm+2, c2m+2, ...
    # .
    # .
    # ym = cm, c2m, c3m, ...
    # The guessed key length with the highest Index of coincidence is the most probable key length
    for guess_len in range(MIN_KEY_LENGTH, MAX_KEY_LENGTH+1):
        ic_sum=0.0
        avg_ic=0.0
        for i in range(guess_len):
            subsequence=""            
            # breaks the ciphertext into subsequences
            for j in range(0, len(ciphertext[i:]), guess_len):
                subsequence += ciphertext[i+j]            
            ic_sum+=index_of_coincidence(subsequence)
        if not guess_len==0:
            avg_ic=ic_sum/guess_len
        ic_table.append(avg_ic)
   
    print (ic_table)

    max_ic = 0.0
    max_m = 0
    for i in range (MAX_KEY_LENGTH + 1 - MIN_KEY_LENGTH):
        if ic_table[i] > max_ic:
            max_m = i
            max_ic = ic_table[i]
    # return the key length (that's why +4) with the best Index of coincidence
    return max_m + 4

"""@ Find frequencies of encrypted characters in subsequences"""

def countInSubsequence(ciphertext, m):

    cipherTxt = open(ciphertext, "r")
    encText = cipherTxt.read()

    if m == 0:
        m =  get_key_length(encText)
    print ("\nm = "+str(m))
    subs = []
    sub=""   
    # Store all subsequencies         
    for i in range(m):
        for j in range(0, len(encText[i:]), m):
            sub += encText[i+j]
        subs.append(sub)
        sub = ""

    # Find the frequence of each char
    i=1
    sorted_subs = []
    for sub in subs:
        print("\nSUBSEQUENCE _"+str(i))
        print(sub + " ||| len = "+str(len(sub)))
        sorted_subs.append(countCapLetters(sub, 0))
        i += 1

    return [subs, sorted_subs]

"""@ Find Index of Coincidence"""

def index_of_coincidence(subsequence):
    n = float(len(subsequence))
    frequency_sum = 0.0

    # counting Σ( 0<= i <=25 ) fi*(fi-1)
    for letter in alphabet:        
        frequency_sum += subsequence.count(letter)*(subsequence.count(letter)-1)         
	# counting (Σ( 0<= i <=25 ) fi*(fi-1))/n*(n-1)
    ic = frequency_sum/(n*(n-1))

    return ic

"""@ Call only the functions you need"""

if __name__ == "__main__":
    #capitalizeMsg(plain_path)
    #countCapLetters(plainCap_path, 1)
    #encryption_Vigenere(plainCap_path)
    #countCapLetters("./cipher.txt", 1) 

                                    #file, key length (if key set 0 fun get_key_length will be called)
    #subs_sorted_subs = countInSubsequence(cipher_path,0)
                                    #file, all subsequencies, freq of each subsequence's letter, key length
    #decryption_Kasiski(cipher_path, subs_sorted_subs[0], subs_sorted_subs[1], 4)

"""@ ALPHABET ORDER"""

for i in range(26):
  print(chr(i+65) + " : " + str(i))

"""@ CHANGE SUBSTRING ACCORDING TO SHIFT"""

# substring, shift
def change_sub(sub, c):
  N = 26
  for ch in sub:
    pos = ord(ch) + c
    if pos<65:
      pos += N
    elif pos>90:
      pos = (pos % 91) + 65
    print(chr(pos), end="")

change_sub("insert substring here", "insert shift here, for example 9 or -5")

"""@ CONNECT DECRYPTED SUBSTRINGS (INPUTS BY HAND)"""

substr = ['insert',
          'substrings',
          'here']

str_len = len(substr[0])
sublen = len(substr)
print(str_len, sublen)
for i in range(str_len):  
  for j in range(sublen):
    if i<len(substr[j]):
      if(substr[j][i].isalpha()):
        print(substr[j][i], end="")

"""@ FIND KEY"""

#According to key length (m), use the first m chars from cipher and decrypted string to find the key
cipher_str = "insert cipher chars here"
decrypt_str = "insert decrypted chars here"
key = ""

for i in range(len(cipher_str)):
  for j in alphabet:
    tmp = chr( ( (ord(cipher_str[i]) - ord(j)) %26 ) + 65 )
    if tmp == decrypt_str[i]:
      key += j
print(key)