class Repository:
    def __init__(self, conn, entity_class, table_name):
        self.conn = conn
        self.entity_class = entity_class
        self.table_name = table_name

    def get_all(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE ESTADO = 1")
        rows = cursor.fetchall()
        cursor.close()
        return [self.entity_class(**row) for row in rows]

    def get_by_id(self, id):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE Id=%s AND ESTADO = 1", (id,))
        row = cursor.fetchone()
        cursor.close()
        return self.entity_class(**row) if row else None

    def add(self, **kwargs):
        cursor = self.conn.cursor()
        cols = ", ".join(kwargs.keys())
        # MySQL/Python connector specific placeholder %s
        vals = ", ".join(["%s"] * len(kwargs))
        sql = f"INSERT INTO {self.table_name} ({cols}) VALUES ({vals})"
        cursor.execute(sql, tuple(kwargs.values()))
        self.conn.commit()
        cursor.close()

    def update(self, id, **kwargs):
        cursor = self.conn.cursor()
        
        set_clauses = []
        values = []
        for col, val in kwargs.items():
            set_clauses.append(f"{col} = %s")
            values.append(val)
        
        values.append(id)
        sql = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE Id = %s"
        cursor.execute(sql, tuple(values))
        self.conn.commit()
        cursor.close()

    def delete(self, id):
        # Soft Delete
        cursor = self.conn.cursor()
        sql = f"UPDATE {self.table_name} SET ESTADO = 0 WHERE Id = %s"
        cursor.execute(sql, (id,))
        self.conn.commit()
        cursor.close()

    def count_all(self, filters=None):
        cursor = self.conn.cursor()
        where_clause = "WHERE ESTADO = 1"
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
        
        sql = f"SELECT COUNT(*) FROM {self.table_name} {where_clause}"
        cursor.execute(sql, tuple(params))
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def get_paged(self, start_index, length, filters=None, order=None):
        cursor = self.conn.cursor(dictionary=True)
        where_clause = "WHERE ESTADO = 1"
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
                direction = o.get('OrderType') # ASC or DESC
                if prop:
                    o_list.append(f"{prop} {direction}")
            if o_list:
                order_clause = "ORDER BY " + ", ".join(o_list)

        limit_clause = f"LIMIT {length} OFFSET {start_index}"
        
        sql = f"SELECT * FROM {self.table_name} {where_clause} {order_clause} {limit_clause}"
        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        return [self.entity_class(**row).to_dict() for row in rows]
