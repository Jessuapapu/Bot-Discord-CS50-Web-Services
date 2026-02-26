
import asyncio
class Estudiante:
    def __init__(self, Usuario: str, UsuarioDiscord: str, IdDiscord: str, IdOffices: str, grupo: str,
                 TiempoTotal: int,cumplimientoReal: float | int, avatar: str):
        """_summary_

        Args:
            Usuario (str): Nombre de usuario (Display name)
            UsuarioDiscord (str): Nombre de Usuario de discord
            IdDiscord (str): Id de discord 
            IdOffices (str): Id de offices 
            grupo (str): Grupo del Usuario
            TiempoTotal (int): cumplimiento en segundos totales
            cumplimientoReal (float | int): cumplimiento en tiempo de 1 hora
        """
        # Como los estudiantes estan formateados desde el singleton del bot, solo se mandan los datos
        self.IdUsuario = Usuario
        self.UsuarioDiscord = UsuarioDiscord
        self.IdDiscord = IdDiscord
        self.grupo = grupo
        self.IdOffice = IdOffices
        self.TiempoTotal = TiempoTotal
        self.cumplimientoReal = cumplimientoReal
        self.avatar = avatar
        
        # Validar contador y no se hagan 2 o mas
        self.Contador = None

    def calcularCumplimieto(self):
        # Valida si ha estado al menos 20 minutos en la offices
        if round(self.TiempoTotal / 3600,1) >= 1.75:
            self.cumplimientoReal = 2.0
        
        elif round(self.TiempoTotal / 3600,1) >= 1.3:
            self.cumplimientoReal = 1.5
        
        elif round(self.TiempoTotal / 3600,1) >= 0.75:
            self.cumplimientoReal = 1
            
        elif round(self.TiempoTotal / 3600,1) >= 0.3:
            self.cumplimientoReal = 0.5
                 
        else:
            self.cumplimientoReal = 0.0
        
        return
    
    async def DetenerContador(self):
        if self.Contador and not self.Contador.done():
            self.Contador.cancel()
            try:
                await self.Contador
            except asyncio.CancelledError:
                pass
        self.calcularCumplimieto()
    
    
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

        except asyncio.CancelledError:
            pass
    
    def toString(self):
        return f"{self.IdUsuario} | {self.grupo} | {self.cumplimientoReal} \n"
    
    # Forma de comparar duplicados
    def __eq__(self, other):
        return (isinstance(other,Estudiante) and self.IdDiscord == other.IdDiscord)
    
    def __hash__(self):
        return hash(self.IdDiscord)

        
    def to_dict(self):
        return {
            "IdUsuario": self.IdUsuario,
            "IdDiscord": self.IdDiscord,
            "grupo": self.grupo,
            "IdOffice": self.IdOffice,
            "TiempoTotal": self.TiempoTotal,
            "cumplimientoReal": self.cumplimientoReal,
            "avatar": self.avatar
        }