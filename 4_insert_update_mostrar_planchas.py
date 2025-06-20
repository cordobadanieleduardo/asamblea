from asamblea.models import Plancha
planchas=Plancha.objects.all()
for p in planchas:
    if p.name.lower().__contains__('plancha uno'):
        p.mostrar = not p.mostrar
    
    if p.name.lower().__contains__('plancha dos'):
        p.mostrar = not p.mostrar
    if p.name.lower().__contains__('plancha tres'):
        # p.mostrar = not p.mostrar
        p.mostrar = False
    
    if p.name.lower().__contains__('voto en blanco'):
        p.mostrar = not p.mostrar

# <- Esto guarda el cambio en la base de datos
Plancha.objects.bulk_update(planchas, ["mostrar"])
print('terminó de actualizar')
