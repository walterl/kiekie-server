import os

from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from kiekie.models import Picture


class Command(BaseCommand):
    help = 'Manipulate pictures in the system'

    def add_arguments(self, parser):
        commands = parser.add_mutually_exclusive_group()
        commands.add_argument('--add', '-a', metavar='FILENAME',
                              help='Add a picture.')
        commands.add_argument('--list', '-l', action='store_true',
                              help='List all pictures.')
        commands.add_argument('--delete', '-D', metavar='PICTURE_ID',
                              help='Delete/undelete a picture.')
        commands.add_argument('--flag', '-f', metavar='PICTURE_ID',
                              help='Flag/unflag a picture.')

        parser.add_argument('--user', '-u',
                            help="Add picture this user's profile")
        parser.add_argument('--note', '-n', help="New picture's note.")

    def handle(self, *args, **options):
        output = []

        if options['list']:
            output = list(Picture.objects.all())
        elif options['add']:
            fname = options['add']
            if not os.path.isfile(fname):
                raise CommandError('Invalid file name: {}'.format(fname))

            if not options['user']:
                raise CommandError('--user required to add a file.')
            try:
                user = User.objects.get(username=options['user'])
            except User.DoesNotExist:
                raise CommandError('Invalid user name: {}'.format(
                    options['user']))

            _, fname_nodir = os.path.split(fname)
            pic = Picture.objects.create(owner=user, note=options['note'])
            pic.file.save(fname_nodir, File(open(fname, 'rb')))
            output.append(pic)
        elif options['delete']:
            pic = self.get_pic(options['delete'])
            pic.deleted = not pic.deleted
            pic.save()
            output.append(pic)
        elif options['flag']:
            pic = self.get_pic(options['flag'])
            pic.flagged = not pic.flagged
            pic.save()
            output.append(pic)
        else:
            raise CommandError('Specify command (--)add or (--)list')

        for pic in output:
            self.stdout.write(str(pic))

    def get_pic(self, pic_id):
        try:
            return Picture.objects.get(pk=pic_id)
        except Picture.DoesNotExist:
            raise CommandError('Invalid picture ID: {}'.format(pic_id))
