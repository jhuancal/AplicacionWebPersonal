def serialize_user(user_data):
    """
    Serializes user data for the session cookie/storage.
    """
    if not user_data:
        return None

    # Base dictionary
    model = {
        'Id': user_data.get('Id'),
        'Username': user_data.get('Username'),
        'Tipo': user_data.get('Tipo', 'Usuario'), 
        'Nombres': user_data.get('Nombres'),
        'Apellidos': user_data.get('Apellidos'),
        'Dni': user_data.get('Dni'),
        'Email': user_data.get('Email'),
        'Roles': []
    }

    # Helper to add role
    if user_data.get('RolNombre'):
        model['Roles'].append(user_data['RolNombre'])
    
    return model
