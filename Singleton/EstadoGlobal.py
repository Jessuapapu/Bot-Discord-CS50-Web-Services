
from models import OfficeClass, EstudianteClass 


class EstadoGlobal:
    """ 
        OfficesActivas -> { str(Id): Offices }, Es la estructura la cual guarda las offices que estan activas
        
        OfficesRevision -> { str(Id): Offices }, Es la estructura la cual guarda la offices que ya terminaron y esta en revision
        
        CanalesDeVoz -> { str(Canal): IdOffices }, Es la estructura que asocia una offices con un canal de voz
    """

        
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        self.OfficesActivas: dict[str,OfficeClass.Offices] = {} # { str(Id): Offices }, Es la estructura la cual guarda las offices que estan activas
        self.OfficesRevision: dict[str,OfficeClass.Offices] = {}   # { str(Id): Offices }, Es la estructura la cual guarda la offices que ya terminaron y esta en revision
        self.CanalesDeVoz: dict[str,str] = {}      # { str(Canal): IdOffices }, Es la estructura que asocia una offices con un canal de voz
        
        # Lista de roles que se excluyen o se aceptan en el servidor cs|web 
        self.ListaDeRolesPermitidos: list[str] = ["Staff", "Admin", "Admin Staff", "Profesor", "staff", "Bot", "Bots"] 
        self.ListaDeRolesPermitidosAdmin: list[str] = ["Admin", "Admin Staff", "Profesor"]
        self.pruebas()
        
        
    def getKeyCanalesDeVoz(self) -> list:
        """ Retorna Todas la key de los canales de voz """
        return list(self.CanalesDeVoz.keys())
    
    def getKeyOfficesActivas(self) -> list:
        """ Retorna todas las keys de la offices que estan en lista (activas), la key es su Id """
        return list(self.OfficesActivas.keys())
    
    def getKeyOfficesRevision(self) -> list:
        """ Retorna todas las keys de la offices que estan en revision, la key es su Id  """
        return list(self.OfficesRevision.keys())
    
    def getOffices(self, Id: str) -> OfficeClass.Offices | None:
        """ retorna una offices, ya sea activa o en revision """
        
        # Valida si es que esta en alguna parte de la offices, si no la encuentra retorna None
        if Id in self.getKeyOfficesActivas():
            return self.OfficesActivas[Id] 
        if Id in self.getKeyOfficesRevision():
            return self.OfficesRevision[Id]

        # Si no encuentra nada retorna None
        return None
    
    def getOfficesActivasDict(self) -> dict:
        """_summary_

        Returns:
            dict: Retorna el diccionario de offices activas
        """
        dic = {}
        for offices in self.OfficesActivas.values():
            dic[offices.Id] = offices.to_dict()
        return dic
    
    
    def getOfficesRevisionDict(self) -> dict:
        """_summary_

        Returns:
            dict: Retorna el diccionario de offices Revision
        """
        dic = {}
        for offices in self.OfficesRevision.values():
            dic[offices.Id] = offices.to_dict()
        return dic
    
    def to_dict(self):
        dicc = {}
        for OfficesKey in self.OfficesActivas.keys():
            dicc[OfficesKey] = self.OfficesActivas[OfficesKey].to_dict()

        for OfficesKey in self.OfficesActivas.keys():
            dicc[OfficesKey] = self.OfficesActivas[OfficesKey].to_dict()

        return dicc
        
    
    def getEstudiante(self, Estudiante: str, Id) -> EstudianteClass.Estudiante | None:
        """ Metodo para retornar un estudiante directo de la offices """
        office = self.getOffices(Id)
        
        if not office:
            # Si no encuentra la offices retorna None
            return None
        
        for User in office.Usuarios:
            
            # Valida por el Nombre (IdUsuario)
            if User.IdUsuario == Estudiante:
                return User
        # Si no lo encuentra Retorna None
        
        return None


    def pruebas(self):
        self.OfficesActivas["pipi"] = OfficeClass.Offices("pipi", "JEssua",{"luis":1},[EstudianteClass.Estudiante("Luis","Luis mamaturca","189267348","pipi","Grupo A",150,0.0,"https://cdn.discordapp.com/avatars/730480482621456484/ef9a998e968154797a77fef510f27a86.png?size=64")],"1-5","15:00","los pns",["jsolis","dalvarez","sduarte"])
        self.OfficesActivas["pipi2"] = OfficeClass.Offices("pipi2", "JEssua",{"luis":1},[EstudianteClass.Estudiante("Luis","Luis mamaturca","11111111111","pipi","Grupo A",0,0.0,"https://img.entnerd.com/upload/2025/02/17161D514C43466D17100F55524944721F131A185046467513-2000x1125.jpg")],"1-5","15:00","los pns",["lcruz"])
        self.OfficesActivas["pipi3"] = OfficeClass.Offices("pipi3", "JEssua",{"luis":1},[EstudianteClass.Estudiante("Luis","Luis mamaturca","189267348","pipi","Grupo A",60,0.0,"https://img.entnerd.com/upload/2025/02/17161D514C43466D17100F55524944721F131A185046467513-2000x1125.jpg")],"1-5","15:00","los pns",["akelly"])
    
        
    def to_DictActivasEstudiantes(self):
        dicc = {}
        for OfficesKey in self.OfficesActivas.keys():
            dicc[OfficesKey] = self.OfficesActivas[OfficesKey].to_dictEstudiantes()
            
        return dicc
    
    def to_DictInformacion(self):
        dicc = {}
        for OfficesKey in self.OfficesActivas.keys():
            dicc[OfficesKey] = self.OfficesActivas[OfficesKey].to_dictInfo()
        return dicc