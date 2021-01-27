import glob
import os
import shutil
import re
import mutagen
from mutagen.id3 import ID3, TIT2
from mutagen.easyid3 import EasyID3, Metadata
from pathlib import Path

# glob to cache file paths for .osu, .mp3, .ogg
# os and Path for paths in working directories
# shutil to copy audio files
# re to filter characters not allowed in FAT/NTFS
# mp3_tagger to retag audio

# set of characters which will be filtered out because they throw errors on Windows/NTFS/FAT
# not necessary on unix
forbiddenSymbols = ['\\', '/', ':', '*', '?', '<', '>', '|']

# create variables to work with later
fileFolderCache = []
fileCopyDone = []
fileCache = ''
titleCache = ''
artistCache = ''
destname = ''
n = 0

# create folder to which all files will be copied to
destfolder = Path('osuCoPY')
destfolder.mkdir(parents=True, exist_ok=True)

# get all .osu, .mp3 and .ogg files which later will all be processed; causes a slight delay before the copy runs
osufiles = glob.glob('Songs/**/*.osu', recursive=True)
oggfiles = glob.glob('Songs/**/*.[oO][gG][gG]', recursive=True)
mp3files = glob.glob('Songs/**/*.[mM][pP][3]', recursive=True)

# cache all audio to a list
files_grabbed = []
files_grabbed.extend(oggfiles)
files_grabbed.extend(mp3files)

# I should definitely put some defs here to get some structure in this cluttered code

# todo: check if file from the same folder has already been copied
# evtl. Variable oder Liste, die Dateinamen innerhalb eines Ordners speichert und beim velassen des Ordners geleert wird


def ogg_copy():
	destname = ('osuCoPY/' + artistCache + ' - ' + titleCache + '.ogg')
	shutil.copyfile(folderfile, destname)

def mp3_copy():
	destname = ('osuCoPY/' + artistCache + ' - ' + titleCache + '.mp3')
	shutil.copyfile(folderfile, destname)

def audio_retag():
	id3destname = destname
	id3destname['title'] = titleCache
	id3destname['artist'] = artistCache

# actual code bois
for file in osufiles:
	n += 1
	print(n)
	with open(file, 'r', encoding='utf-8', errors='ignore') as osufiletemp:
		for line in osufiletemp:
			if 'TitleUnicode' in line:
				continue
			elif 'ArtistUnicode' in line:
				break
			elif 'AudioFilename' in line:
				fileCacheTemp = line.split(':')[1]
				fileCache = fileCacheTemp.strip()
				if fileCache in fileFolderCache:
					break
				else:
					fileFolderCache.append(fileCache)
			elif 'Title' in line:
				titleCacheTemp = line.split(':')[1]
				titleCacheTemp1 = titleCacheTemp.strip()
				titleCache = re.sub(r'[:*?!<>|"/\\]', '', titleCacheTemp1)
			elif 'Artist' in line:
				artistCacheTemp = line.split(':')[1]
				artistCacheTemp1 = artistCacheTemp.strip()
				artistCache = re.sub(r'[:*?!<>|"/\\]', '', artistCacheTemp1)
				break
			else:
				continue
	for folderfile in fileFolderCache:
		if folderfile in files_grabbed:
			if folderfile in fileCopyDone:
				break
			elif '.ogg' in folderfile:
				ogg_copy()
				audio_retag()
				fileCopyDone.append(folderfile)
			elif '.mp3' in folderfile:
				mp3_copy()
				audio_retag()
				fileCopyDone.append(folderfile)
