def get_bool_input(prompt):
    YES_VALUES = {'y', 'yes'}
    return input(prompt).lower() in YES_VALUES

def auto_confirmation(prompt):
    return True