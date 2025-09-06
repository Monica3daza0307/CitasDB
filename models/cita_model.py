# models/cita_model.py
class Cita:
    def __init__(self, id, paciente, medico, fecha, hora, motivo):
        self.id = id
        self.paciente = paciente
        self.medico = medico
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo

    def to_dict(self):
        return {
            "id": self.id,
            "paciente": self.paciente,
            "medico": self.medico,
            "fecha": self.fecha,
            "hora": self.hora,
            "motivo": self.motivo
        }