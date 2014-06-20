make-noagenda-lofi
==================

Convert incoming [No Agenda Show](http://www.noagendashow.com/) episodes from [BitTorrent Sync](http://www.bittorrent.com/sync) into 16kbps Opus audio files and post them to a WordPress instance.

**Unfinished.**

Requirements
------------

* imagemagick
* lame
* opus-tools
* inotify-tools
* Python 3.x
* mutagenx ( https://pypi.python.org/pypi/mutagenx/1.22.1 )
* python-pysqlite2
* python3-pyrss2gen

Operation
---------

- Setup a BitTorrent Sync client to continuously sync the public folder with the key `R5NSJBPWKW52OO5HCY27JUHKZSKOFAR2D`.
- Make a symlink from `make-noagenda-lofi/input` to the BTSync folder.
- Run `./scripts/watch-for-files.sh` at boot time. It will wait for new files in `./input` and call `scripts/process.py` when it finds any.
- `process.py` will select all `*.mp3` files in `./input` that it has not already processed before:
  * Extract title, artist, cover art, etc.
  * Convert mp3 file to 16kbps monaural Opus audio file in `./output/$year`.
  * Tag the Opus file and create external cover art jpg file and thumbnail jpg file in `./output/$year`.
  * Create `./output/queue/$filename.data` with all WordPress post attributes in JSON format.
- `./output` is rsynced to `./files` at the WordPress site, with "no deleting" option.
- More stuff happens.
