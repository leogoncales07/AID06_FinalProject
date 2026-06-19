from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria os três membros da equipa (leo, max, theo) como administradores/staff'

    def handle(self, *args, **kwargs):
        members = ['leo', 'max', 'theo']
        default_password = 'admin' # Password super simples para facilidade

        for username in members:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_superuser(
                    username=username,
                    email=f'{username}@comicstore.local',
                    password=default_password
                )
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Sucesso: Utilizador "{username}" criado com sucesso! (Password: {default_password})'))
            else:
                self.stdout.write(self.style.WARNING(f'Aviso: O utilizador "{username}" já existe.'))
        
        self.stdout.write(self.style.SUCCESS('\nA equipa foi configurada. Podem aceder ao /dashboard/ após o Login!'))
