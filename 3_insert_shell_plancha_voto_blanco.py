from django.db.models import Count
from asamblea.models import Militante, Puesto, Plancha
puesto =Puesto.objects.values('id','dpto_name','mun_name','comuna_name').annotate(t=Count('id'))
# print(puesto)
mostrar =True
#Usuario creacion
uc=Militante.objects.get(username='daniel')
print('Usuario creacion ', uc)
if uc :    
    for p in puesto:
        # print(p['id'],p['dpto_name'],p['mun_name'], p['comuna_name'])
        location =Puesto.objects.get(pk =p['id']) 
        # print(location)   
        plancha=Plancha.objects.filter(name__contains='Plancha Uno', location=location).first()
        if plancha is None:
            p=Plancha.objects.create(name='Plancha Uno', location=location, mostrar =mostrar, uc=uc )
            print('Crea plancha uno ', p)
        plancha=Plancha.objects.filter(name__contains='Plancha Dos', location=location).first()
        if plancha is None:
            p=Plancha.objects.create(name='Plancha Dos', location=location , mostrar =mostrar , uc=uc )
            print('Crea plancha dos ', p)
        plancha=Plancha.objects.filter(name__contains='Plancha Tres', location=location).first()
        if plancha is None:
            p=Plancha.objects.create(name='Plancha Tres', location=location , mostrar =mostrar, uc=uc )
            print('Crea plancha tres', p)
        plancha=Plancha.objects.filter(name__contains='Voto en blanco', location=location).first()
        if plancha is None:
            p=Plancha.objects.create(name='Voto en blanco', location=location, mostrar =mostrar, uc=uc)
            print('Voto en blanco', p)

exit()