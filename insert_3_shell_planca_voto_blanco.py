from asamblea.models import Militante, Puesto, Plancha
puesto = Puesto.objects.create(id=1,dpto_name='AMAZONAS',mun_name='LETICIA',comuna_name='')
Plancha.objects.create(uc= Militante.objects.get(usename='daniel'), name='Voto en blanco')
exit()