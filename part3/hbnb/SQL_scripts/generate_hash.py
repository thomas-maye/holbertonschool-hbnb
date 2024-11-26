import bcrypt

password = "antoinepass".encode('utf-8')
hashed =  bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode('utf-8'))
