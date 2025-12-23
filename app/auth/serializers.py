def serialize_user(user_data):
    """
    Serializes user data for the session cookie/storage.
    """
    if not user_data:
        return None

    # Base dictionary
    model = {
        'Id': user_data.get('Id'),
        'Username': user_data.get('NombreUsuario'),
        'Tipo': user_data.get('Tipo', 'Usuario'), # Cliente or Colaborador
        'Nombres': user_data.get('Nombres'),
        'Apellidos': user_data.get('Apellidos'),
        'DNI': user_data.get('DNI'),
        'Correo': user_data.get('Correo'),
        'Roles': []
    }

    # Helper to add role
    if user_data.get('RolNombre'):
        model['Roles'].append(user_data['RolNombre'])
    
    # Specific fields
    if user_data.get('Tipo') == 'Colaborador':
        model['EsActivo'] = user_data.get('EsActivo')
        model['FechaContratacion'] = user_data.get('FechaContratacion')
    elif user_data.get('Tipo') == 'Cliente':
        model['NumeroCuenta'] = user_data.get('NumeroCuenta')

    return model
