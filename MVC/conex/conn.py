import pymysql

class Conex:
    def __init__(self, host="localhost", user="root", passwd="", database="viaja_seguro", port=3306):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.port = port
        self.__myconn = None
        self.connect()

    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.__myconn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                database=self.database,
                port=self.port,
                charset='utf8mb4'
                # SIN DictCursor - usa tuplas normales
            )
            print("✅ Conexión a MySQL establecida correctamente")
            print(f"✅ Base de datos: {self.database}")
        except Exception as ex:
            print(f"❌ Error de conexión: {ex}")
            print(f"   Host: {self.host}, User: {self.user}, Database: {self.database}")
            self.__myconn = None

    def closeConex(self):
        """Cierra la conexión"""
        if self.__myconn:
            self.__myconn.close()
            print("🔌 Conexión cerrada")

    def getConex(self):
        """Retorna la conexión para usar en otros archivos"""
        return self.__myconn

    def is_connected(self):
        """Verifica si la conexión está activa"""
        try:
            if self.__myconn and self.__myconn.open:
                cursor = self.__myconn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                return True
            return False
        except:
            return False