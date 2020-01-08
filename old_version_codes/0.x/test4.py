
scode, sxh = str(a.content)[2:-1].split("#")

i = 0

userAccount = '111111'
userPassword = 'aaaaaa'
code = userAccount + '%%%' + userPassword
encoded = ''

i = 0

for x in range(i, len(code)):
    i += 1
    if i < 20:
        encoded = encoded + code[i: i+1] + scode[0: int(sxh[i: i+1])]
        scode = scode[int(sxh[i: i+1]): len(scode)]
    else:
        encoded = encoded + code[i: len(code)]
        i = len(code)

print(encoded)
