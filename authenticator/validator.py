import re
def validate_password(password, confirm_password):
	if len(password) < 8:
		return 'Password must be 8 characaters long'

    # Check for at least one uppercase letter
	if not re.search(r'[A-Z]', password):
		return "Password must contain at least one uppercase letter."

    # Check for at least one lowercase letter
	if not re.search(r'[a-z]', password):
		return "Password must contain at least one lowercase letter."

    # Check for at least one digit
	if not re.search(r'\d', password):
		return "Password must contain at least one number."

    # Check for at least one special character
	if not re.search(r'[@$!%*?&]', password):
		return "Password must contain at least one special character: @$!%*?&"

    # Check if the password is too common
	common_passwords = ['password', '123456', 'qwerty', 'letmein']
	if password.lower() in common_passwords:
		return "This is a common password. Please choose a stronger one."
		
	print(password , " = " , confirm_password)
	if password != confirm_password:	
		return "Password does not match"

	return True
