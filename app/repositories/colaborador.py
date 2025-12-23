from .base import Repository
from entities.colaborador import Colaborador

class ColaboradorRepository(Repository):
    def __init__(self, conn):
        super().__init__(conn, Colaborador, "Seg_Colaborador")
        self.table_name = "Seg_Colaborador"
        self.base_table = "Seg_Usuario"

    def get_all(self):
        cursor = self.conn.cursor(dictionary=True)
        query = f"""
            SELECT U.*, C.IdRol, C.EsActivo, C.FechaContratacion, P.Nombres, P.Apellidos
            FROM {self.base_table} U
            JOIN {self.table_name} C ON U.Id = C.Id
            LEFT JOIN Adm_Persona P ON U.IdPersona = P.Id
            WHERE U.ESTADO = 1
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        # No special handling needed for get_all unless used by UI directly; assuming Grid uses get_paged.
        return [self.entity_class(**row) for row in rows]

    def add(self, **kwargs):
        cursor = self.conn.cursor()
        
        # Split fields
        usuario_fields = ['Id', 'NombreUsuario', 'Contrasena', 'IdPersona', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        usuario_data = {k: v for k, v in kwargs.items() if k in usuario_fields}
        
        colaborador_fields = ['Id', 'IdRol', 'EsActivo', 'FechaContratacion', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        colaborador_data = {k: v for k, v in kwargs.items() if k in colaborador_fields}

        # Insert Usuario
        # Enforce "ws_" prefix for Colaborador username
        if 'NombreUsuario' in usuario_data:
            if not usuario_data['NombreUsuario'].startswith('ws_'):
                usuario_data['NombreUsuario'] = 'ws_' + usuario_data['NombreUsuario']

        columns_u = ", ".join(usuario_data.keys())
        placeholders_u = ", ".join(["%s"] * len(usuario_data))
        sql_u = f"INSERT INTO {self.base_table} ({columns_u}) VALUES ({placeholders_u})"
        cursor.execute(sql_u, list(usuario_data.values()))

        # Insert Colaborador
        columns_c = ", ".join(colaborador_data.keys())
        placeholders_c = ", ".join(["%s"] * len(colaborador_data))
        sql_c = f"INSERT INTO {self.table_name} ({columns_c}) VALUES ({placeholders_c})"
        cursor.execute(sql_c, list(colaborador_data.values()))

        self.conn.commit()

    def update(self, id, **kwargs):
        cursor = self.conn.cursor()
        
        # Split fields
        usuario_fields = ['NombreUsuario', 'IdPersona', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        usuario_data = {k: v for k, v in kwargs.items() if k in usuario_fields}
        
        colaborador_fields = ['IdRol', 'EsActivo', 'FechaContratacion', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        colaborador_data = {k: v for k, v in kwargs.items() if k in colaborador_fields}

        # Update Usuario
        if usuario_data:
            set_clause_u = ", ".join([f"{k}=%s" for k in usuario_data.keys()])
            sql_u = f"UPDATE {self.base_table} SET {set_clause_u} WHERE Id=%s"
            cursor.execute(sql_u, list(usuario_data.values()) + [id])

        # Update Colaborador
        if colaborador_data:
            set_clause_c = ", ".join([f"{k}=%s" for k in colaborador_data.keys()])
            sql_c = f"UPDATE {self.table_name} SET {set_clause_c} WHERE Id=%s"
            cursor.execute(sql_c, list(colaborador_data.values()) + [id])

        self.conn.commit()
        cursor.close()

    def count_all(self, filters=None):
        cursor = self.conn.cursor()
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
            SELECT U.*, C.IdRol, C.EsActivo, C.FechaContratacion, P.Nombres, P.Apellidos
            FROM {self.base_table} U
            JOIN {self.table_name} C ON U.Id = C.Id
            LEFT JOIN Adm_Persona P ON U.IdPersona = P.Id
            {where_clause} {order_clause} {limit_clause}
        """
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        
        results = []
        for row in rows:
            obj_dict = self.entity_class(**row).to_dict()
            obj_dict['NombreCompleto'] = f"{row.get('Nombres','')} {row.get('Apellidos','')}".strip()
            obj_dict['Contrasena'] = row.get('Contrasena')
            results.append(obj_dict)
        return results

    def add(self, **kwargs):
        cursor = self.conn.cursor()
        
        # Split fields
        usuario_fields = ['Id', 'NombreUsuario', 'Contrasena', 'IdPersona', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        usuario_data = {k: v for k, v in kwargs.items() if k in usuario_fields}
        
        colaborador_fields = ['Id', 'IdRol', 'EsActivo', 'FechaContratacion', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        colaborador_data = {k: v for k, v in kwargs.items() if k in colaborador_fields}

        # Insert Usuario
        # Enforce "ws_" prefix for Colaborador username
        if 'NombreUsuario' in usuario_data:
            if not usuario_data['NombreUsuario'].startswith('ws_'):
                usuario_data['NombreUsuario'] = 'ws_' + usuario_data['NombreUsuario']

        columns_u = ", ".join(usuario_data.keys())
        placeholders_u = ", ".join(["%s"] * len(usuario_data))
        sql_u = f"INSERT INTO {self.base_table} ({columns_u}) VALUES ({placeholders_u})"
        cursor.execute(sql_u, list(usuario_data.values()))

        # Insert Colaborador
        columns_c = ", ".join(colaborador_data.keys())
        placeholders_c = ", ".join(["%s"] * len(colaborador_data))
        sql_c = f"INSERT INTO {self.table_name} ({columns_c}) VALUES ({placeholders_c})"
        cursor.execute(sql_c, list(colaborador_data.values()))

        self.conn.commit()

    def update(self, id, **kwargs):
        cursor = self.conn.cursor()
        
        # Split fields
        usuario_fields = ['NombreUsuario', 'IdPersona', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        usuario_data = {k: v for k, v in kwargs.items() if k in usuario_fields}
        
        colaborador_fields = ['IdRol', 'EsActivo', 'FechaContratacion', 'ESTADO', 'DISPONIBILIDAD', 'FECHA_CREACION', 'FECHA_MODIFICACION', 'USER_CREACION', 'USER_MODIFICACION']
        colaborador_data = {k: v for k, v in kwargs.items() if k in colaborador_fields}

        # Update Usuario
        if usuario_data:
            set_clause_u = ", ".join([f"{k}=%s" for k in usuario_data.keys()])
            sql_u = f"UPDATE {self.base_table} SET {set_clause_u} WHERE Id=%s"
            cursor.execute(sql_u, list(usuario_data.values()) + [id])

        # Update Colaborador
        if colaborador_data:
            set_clause_c = ", ".join([f"{k}=%s" for k in colaborador_data.keys()])
            sql_c = f"UPDATE {self.table_name} SET {set_clause_c} WHERE Id=%s"
            cursor.execute(sql_c, list(colaborador_data.values()) + [id])

        self.conn.commit()
        cursor.close()

    def count_all(self, filters=None):
        cursor = self.conn.cursor()
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
            SELECT U.*, C.IdRol, C.EsActivo, C.FechaContratacion
            FROM {self.base_table} U
            JOIN {self.table_name} C ON U.Id = C.Id
            {where_clause} {order_clause} {limit_clause}
        """
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        return [self.entity_class(**row).to_dict() for row in rows]
