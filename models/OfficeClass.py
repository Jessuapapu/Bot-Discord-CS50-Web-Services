from models.EstudianteClass import Estudiante
import asyncio
from Socket.WebSocket import sio

class Offices:

    def __init__(self, Id, IdUsuario, ListaDeVotos: dict,
                Usuarios: list[Estudiante], bloque: str, HoraCreacion: str,CanalVoz: str, Staff: list = []):
        """_summary_

        Args:
            Id (_type_): Id offices
            IdUsuario (_type_): Creador de la offices
            ListaDeVotos (_type_): cantidad de votos
            Usuarios (list[Estudiante]): Lista de estudiantes
            bloque (str): Bloque de offices
            HoraCreacion (str): Hora de creacion
            CanalVoz (str): Canal de voz
            Staff (list, optional): Staff en la offices. Defaults to [].
        """
        # Informacion de la offices
        self.Id = Id
        self.IdUsuario = IdUsuario
        self.HoraCreacion = HoraCreacion
        self.bloque = bloque
        self.canal = CanalVoz
        
        # Informacion del Staff
        self.NombresStaff = Staff
        
        # Es la lista de estudiantes activos
        self.Usuarios = Usuarios
        self.ListaDeVotos = ListaDeVotos
        
        # Se refiere al estado, 1: Activa, 0: Finalizada
        self.Estado = True
        self._Limpieza = None
        
        for estudiante in Usuarios:
            asyncio.create_task(estudiante.iniciarContador())
        
        # Validar contador y no se hagan 2 o mas
        self.Contador = None
        self.TiempoTotal = 0
        self._Contador = asyncio.create_task(self.iniciarContador())
        
        
        
    async def iniciarContador(self):
        # Si ya hay un contador activo, cancelarlo y luego volver activarlo
        if self.Contador is not None:
            if not self.Contador.done():
                self.Contador.cancel()
            try:
                await self.Contador
            except asyncio.CancelledError:
                pass

        # Crear uno nuevo y asignarlo
        self.Contador = asyncio.create_task(self.CalcularTiempo())

    
    async def CalcularTiempo(self):
        try:
            while True:
                await asyncio.sleep(1)
                self.TiempoTotal += 1
                await sio.emit("ActualizarTabla",self.to_dictEstudiantes())
        except asyncio.CancelledError:
            pass    

     # Creo que se puede refactorizar mejor esto       
    def getEstudiantes(self):
        return [user.IdUsuario for user in self.Usuarios]

    
    def getUnicoEstudiante(self,IdUsuario):
        # si no lo encuentra retorna None
        for user in self.Usuarios:
            if IdUsuario == user.IdUsuario:
                return user
       
        return None   
    
    
    def iniciarContadorDeVotos(self):
        if len(list(self.ControlDeVotos.keys())) == 0:
            for nombre in self.getNombreEstudiantes():
                self.ControlDeVotos[nombre] = 0
            return
        
        else:
            for nombre in list(self.ControlDeVotos.keys()):
                del self.ControlDeVotos[nombre]
            self.iniciarContadorDeVotos()
    
    
    async def Barrido50(self):  
        if self._Limpieza is not None:
            if not self._Limpieza.done():
                self._Limpieza.cancel()
        
        self._Limpieza = asyncio.create_task(self.limpieza())
            
              
    async def limpieza(self):
        try:
            while True:
                if self.Estado != 1:
                    break
                
                # Eliminar duplicados manteniendo el orden
                tmp = list(dict.fromkeys(self.Usuarios))

                for User in tmp:
                    await User.iniciarContador()

                self.Usuarios = tmp

                await asyncio.sleep(30*60)
        except asyncio.CancelledError:
            pass


    def setStaff(self,Nombres:list[str]):
        self.NombresStaff = Nombres
        return
    
    
    def to_dict(self):
        return {
            "Id": self.Id,
            "IdUsuario": self.IdUsuario,
            "HoraCreacion": self.HoraCreacion,
            "bloque": self.bloque,
            "canal": self.canal,
            "staff": self.NombresStaff,
            "Usuarios": [u.to_dict() for u in self.Usuarios],
            "Estado": self.Estado
        }
        
    def to_dictEstudiantes(self):
        return {
            "Id": self.Id,
            "Usuarios": [u.to_dict() for u in self.Usuarios], 
        }
        
    def to_dictInfo(self):
        return {
            "Id": self.Id,
            "IdUsuario": self.IdUsuario,
            "HoraCreacion": self.HoraCreacion,
            "bloque": self.bloque,
            "canal": self.canal,
            "staff": self.NombresStaff,
            "Estado": self.Estado
        }