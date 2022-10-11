from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *_, **options):
        from moviepy.editor import VideoFileClip
        mp4_file = r'/Users/chenhaiou/Documents/S01E01.mp4'
        mp3_file = r'/Users/chenhaiou/Documents/S01E01.wav'
        videoclip = VideoFileClip(mp4_file)
        audioclip = videoclip.audio
        audioclip.write_audiofile(mp3_file)
        audioclip.close()
        videoclip.close()
