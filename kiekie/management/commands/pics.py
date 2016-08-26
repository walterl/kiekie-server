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
        user = None

        if options['user']:
            try:
                user = User.objects.get(username=options['user'])
            except User.DoesNotExist:
                raise CommandError('Invalid user name: {}'.format(
                    options['user']))

        if options['list']:
            output = self.list_pics(user)
        elif options['add']:
            output.append(self.add_pic(options['add'], user, options['note']))
        elif options['delete']:
            output.append(self.delete_pic(options['delete']))
        elif options['flag']:
            output.append(self.flag_pic(options['flag']))
        else:
            raise CommandError(
                'Specify command (--)add, (--)delete, (--)flag or (--)list')

        for pic in output:
            self.stdout.write(str(pic))

    def add_pic(self, fname, user, note):
        if not os.path.isfile(fname):
            raise CommandError('Invalid file name: {}'.format(fname))

        if not user:
            raise CommandError('--user required to add a file.')

        _, fname_nodir = os.path.split(fname)
        pic = Picture.objects.create(owner=user, note=note)
        pic.file.save(fname_nodir, File(open(fname, 'rb')))
        return pic

    def delete_pic(self, pic_id):
        pic = self.get_pic(pic_id)
        pic.deleted = not pic.deleted
        pic.save()
        return pic

    def flag_pic(self, pic_id):
        pic = self.get_pic(pic_id)
        pic.flagged = not pic.flagged
        pic.save()
        return pic

    def list_pics(self, user=None):
        pics = Picture.objects.all()
        if user:
            pics = pics.filter(owner=user)
        return list(pics)

    def get_pic(self, pic_id):
        try:
            return Picture.objects.get(pk=pic_id)
        except Picture.DoesNotExist:
            raise CommandError('Invalid picture ID: {}'.format(pic_id))
