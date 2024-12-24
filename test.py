from werkzeug.security import check_password_hash, generate_password_hash

password = 'ChihiroMuñeca1234!'

hashed_password = generate_password_hash(password)

print(hashed_password)