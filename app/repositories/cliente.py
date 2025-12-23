from .base import Repository
from entities.cliente import Cliente

class ClienteRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Cliente, "Seg_Cliente")
        self.table_name = "Seg_Cliente"
        self.base_table = "Seg_Usuario"

    def get_all(self):
        cursor = self.conn.cursor(dictionary=True)
        # Join User, Client and Persona
        query = f"""
            SELECT U.*, C.NumeroCuenta, P.Nombres, P.Apellidos
            FROM {self.base_table} U
            JOIN {self.table_name} C ON U.Id = C.Id
            LEFT JOIN Adm_Persona P ON U.IdPersona = P.Id
            WHERE U.ESTADO = 1
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return [self.entity_class.from_dict({**row, 'NombreCompleto': f"{row['Nombres']} {row['Apellidos']}"}) for row in rows]
        # Note: The entity.from_dict might not exist or might need update. For now returning dicts or enhancing entity.
        # However, standard practice here uses entity constructor. The entity class usually doesn't have Nombres/Apellidos.
        # I will attach them dynamically to the object or dict.
        # Since get_paged returns dicts, I will stick to returning objects here but maybe I need to patch the Entity or just rely on get_paged for the Grid.
        # The Grid uses get_paged.
        
    def add(self, **kwargs):
        cursor = self.conn.cursor()
        
        # Split fields for Usuario and Cliente
        # Usuario Fields
        usuario_fields = ['Id', 'NombreUsuario', 'Contrasena', 'IdPersona', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        usuario_data = {k: v for k, v in kwargs.items() if k in usuario_fields}
        
        # Cliente Fields
        cliente_fields = ['Id', 'NumeroCuenta', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        cliente_data = {k: v for k, v in kwargs.items() if k in cliente_fields}

        # Insert Usuario
        columns_u = ", ".join(usuario_data.keys())
        placeholders_u = ", ".join(["%s"] * len(usuario_data))
        sql_u = f"INSERT INTO {self.base_table} ({columns_u}) VALUES ({placeholders_u})"
        cursor.execute(sql_u, list(usuario_data.values()))

        # Insert Cliente
        columns_c = ", ".join(cliente_data.keys())
        placeholders_c = ", ".join(["%s"] * len(cliente_data))
        sql_c = f"INSERT INTO {self.table_name} ({columns_c}) VALUES ({placeholders_c})"
        cursor.execute(sql_c, list(cliente_data.values()))

        self.conn.commit()
    

    def update(self, id, **kwargs):
        cursor = self.conn.cursor()
        
        # Split fields
        usuario_fields = ['NombreUsuario', 'IdPersona', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        usuario_data = {k: v for k, v in kwargs.items() if k in usuario_fields}
        
        cliente_fields = ['NumeroCuenta', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        cliente_data = {k: v for k, v in kwargs.items() if k in cliente_fields}

        # Update Usuario
        if usuario_data:
            set_clause_u = ", ".join([f"{k}=%s" for k in usuario_data.keys()])
            sql_u = f"UPDATE {self.base_table} SET {set_clause_u} WHERE Id=%s"
            cursor.execute(sql_u, list(usuario_data.values()) + [id])

        # Update Cliente
        if cliente_data:
            set_clause_c = ", ".join([f"{k}=%s" for k in cliente_data.keys()])
            sql_c = f"UPDATE {self.table_name} SET {set_clause_c} WHERE Id=%s"
            cursor.execute(sql_c, list(cliente_data.values()) + [id])

        self.conn.commit()
        cursor.close()

    def count_all(self, filters=None):
        cursor = self.conn.cursor()
        where_clause = "WHERE U.ESTADO = 1" # Default filter for active users
        params = []
        if filters:
            conditions = []
            for f in filters:
                prop = f.get('PropertyName')
                val = f.get('Value')
                op = f.get('Operator')
                if prop and val:
                    if op == 'Contains':
                        # Resolve ambiguity if needed, assuming props are unique enough or prefixed
                        # If filtering by Name, we might need P.Nombres or P.Apellidos
                        conditions.append(f"{prop} LIKE %s")
                        params.append(f"%{val}%")
            if conditions:
                where_clause += " AND " + " AND ".join(conditions)
        
        sql = f"SELECT COUNT(*) FROM {self.base_table} U JOIN {self.table_name} C ON U.Id = C.Id LEFT JOIN Adm_Persona P ON U.IdPersona = P.Id {where_clause}"
        cursor.execute(sql, tuple(params))
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def get_paged(self, start_index, length, filters=None, order=None):
        cursor = self.conn.cursor(dictionary=True)
        where_clause = "WHERE U.ESTADO = 1"
        params = []
        
        if filters:
            conditions = []
            for f in filters:
                prop = f.get('PropertyName')
                val = f.get('Value')
                op = f.get('Operator')
                if prop and val:
                    if op == 'Contains':
                        conditions.append(f"{prop} LIKE %s")
                        params.append(f"%{val}%")
            if conditions:
                where_clause += " AND " + " AND ".join(conditions)

        order_clause = ""
        if order:
            o_list = []
            for o in order:
                prop = o.get('Property')
                direction = o.get('OrderType')
                if prop:
                   o_list.append(f"{prop} {direction}")
            if o_list:
                order_clause = "ORDER BY " + ", ".join(o_list)

        limit_clause = f"LIMIT {length} OFFSET {start_index}"
        
        query = f"""
            SELECT U.*, C.NumeroCuenta, P.Nombres, P.Apellidos
            FROM {self.base_table} U
            JOIN {self.table_name} C ON U.Id = C.Id
            LEFT JOIN Adm_Persona P ON U.IdPersona = P.Id
            {where_clause} {order_clause} {limit_clause}
        """
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        
        # Enriched dict return
        results = []
        for row in rows:
            obj_dict = self.entity_class(**row).to_dict()
            obj_dict['NombreCompleto'] = f"{row.get('Nombres','')} {row.get('Apellidos','')}".strip()
            # Explicitly include password for demo purposes request
            obj_dict['Contrasena'] = row.get('Contrasena') 
            results.append(obj_dict)
        return results

    def add(self, **kwargs):
        cursor = self.conn.cursor()
        
        # Split fields for Usuario and Cliente
        # Usuario Fields
        usuario_fields = ['Id', 'NombreUsuario', 'Contrasena', 'IdPersona', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        usuario_data = {k: v for k, v in kwargs.items() if k in usuario_fields}
        
        # Cliente Fields
        cliente_fields = ['Id', 'NumeroCuenta', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        cliente_data = {k: v for k, v in kwargs.items() if k in cliente_fields}

        # Insert Usuario
        columns_u = ", ".join(usuario_data.keys())
        placeholders_u = ", ".join(["%s"] * len(usuario_data))
        sql_u = f"INSERT INTO {self.base_table} ({columns_u}) VALUES ({placeholders_u})"
        cursor.execute(sql_u, list(usuario_data.values()))

        # Insert Cliente
        columns_c = ", ".join(cliente_data.keys())
        placeholders_c = ", ".join(["%s"] * len(cliente_data))
        sql_c = f"INSERT INTO {self.table_name} ({columns_c}) VALUES ({placeholders_c})"
        cursor.execute(sql_c, list(cliente_data.values()))

        self.conn.commit()
    

    def update(self, id, **kwargs):
        cursor = self.conn.cursor()
        
        # Split fields
        usuario_fields = ['NombreUsuario', 'IdPersona', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        usuario_data = {k: v for k, v in kwargs.items() if k in usuario_fields}
        
        cliente_fields = ['NumeroCuenta', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        cliente_data = {k: v for k, v in kwargs.items() if k in cliente_fields}

        # Update Usuario
        if usuario_data:
            set_clause_u = ", ".join([f"{k}=%s" for k in usuario_data.keys()])
            sql_u = f"UPDATE {self.base_table} SET {set_clause_u} WHERE Id=%s"
            cursor.execute(sql_u, list(usuario_data.values()) + [id])

        # Update Cliente
        if cliente_data:
            set_clause_c = ", ".join([f"{k}=%s" for k in cliente_data.keys()])
            sql_c = f"UPDATE {self.table_name} SET {set_clause_c} WHERE Id=%s"
            cursor.execute(sql_c, list(cliente_data.values()) + [id])

        self.conn.commit()
        cursor.close()

    def count_all(self, filters=None):
        cursor = self.conn.cursor()
        where_clause = "WHERE U.ESTADO = 1" # Default filter for active users
        params = []
        if filters:
            conditions = []
            for f in filters:
                prop = f.get('PropertyName')
                val = f.get('Value')
                op = f.get('Operator')
                if prop and val:
                    if op == 'Contains':
                        # Resolve ambiguity if needed, assuming props are unique enough or prefixed
                        conditions.append(f"{prop} LIKE %s")
                        params.append(f"%{val}%")
            if conditions:
                where_clause += " AND " + " AND ".join(conditions)
        
        sql = f"SELECT COUNT(*) FROM {self.base_table} U JOIN {self.table_name} C ON U.Id = C.Id {where_clause}"
        cursor.execute(sql, tuple(params))
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def get_paged(self, start_index, length, filters=None, order=None):
        cursor = self.conn.cursor(dictionary=True)
        where_clause = "WHERE U.ESTADO = 1"
        params = []
        
        if filters:
            conditions = []
            for f in filters:
                prop = f.get('PropertyName')
                val = f.get('Value')
                op = f.get('Operator')
                if prop and val:
                    if op == 'Contains':
                        conditions.append(f"{prop} LIKE %s")
                        params.append(f"%{val}%")
            if conditions:
                where_clause += " AND " + " AND ".join(conditions)

        order_clause = ""
        if order:
            o_list = []
            for o in order:
                prop = o.get('Property')
                direction = o.get('OrderType')
                if prop:
                   o_list.append(f"{prop} {direction}")
            if o_list:
                order_clause = "ORDER BY " + ", ".join(o_list)

        limit_clause = f"LIMIT {length} OFFSET {start_index}"
        
        query = f"""
            SELECT U.*, C.NumeroCuenta
            FROM {self.base_table} U
            JOIN {self.table_name} C ON U.Id = C.Id
            {where_clause} {order_clause} {limit_clause}
        """
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        return [self.entity_class(**row).to_dict() for row in rows]

