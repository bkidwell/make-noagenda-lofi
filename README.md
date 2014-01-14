make-noagenda-lofi
==================

Convert incoming No Agenda Show episodes from BTSync into 16kbps Opus audio files and post them to a WordPress instance.

**Unfinished.**

Requirements
------------

* imagemagick
* lame
* opus-tools
* inotify-tools
* Python 2.7
* python-mutagen
* python-pysqlite2

Operation
---------

- Setup a BTSync client to continuously sync the public folder with the key `R5NSJBPWKW52OO5HCY27JUHKZSKOFAR2D`.
- Make a symlink from `make-noagenda-lofi/input` to the BTSync folder.
- Run `./scripts/watch-for-files.sh` at boot time. It will wait for new files in `./input` and call `scripts/process.py` when it finds any.
- `process.py` will select all `*.mp3` files in `./input` that it has not already processed before:
  * Extract title, artist, cover art, etc.
  * Convert mp3 file to 16kbps monaural Opus audio file in `./output/$year`.
  * Tag the Opus file and create external cover art jpg file and thumbnail jpg file in `./output/$year`.
  * Create `./output/queue/$filename.data` with all WordPress post attributes in JSON format.
- `./output` is rsynced to `./files` at the WordPress site, with "no deleting" option.
- A plugin in the WordPress site is pinged by the converter script; the plugin scans for files in `./files/queue` and creates any new WordPress podcast posts needed.
- Files in `./output` older than 3 weeks are purged.
