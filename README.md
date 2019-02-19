## Python Movie Barcode
A simple command line script to generate movie barcodes. Assumes there are more frames than the specified width.

### Usage

`"Z:\Media\Movies\Black Swan\Black Swan (2010).mkv" -s 7200 2400 -o 0.005 0.05`

```
usage: movie_barcode.py [-h] [-s SIZE SIZE] [-o OFFSETS OFFSETS] file

positional arguments:
  file                  path to the video file

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE SIZE, --size SIZE SIZE
                        size of the image, in width height (1920 1080)
  -o OFFSETS OFFSETS, --offsets OFFSETS OFFSETS
                        percent of beginning and end to ignore, otherwise
                        results in large black portions for the intro and
                        credits.
```

#### Requirements
* opencv-python
* numpy
* Pillow

### Examples

The AristoCats (1970)
![The Aristocats](https://raw.githubusercontent.com/thrushd/Python-Movie-Barcode/master/output/The%20AristoCats%20(1970).png)

The Fifth Element (1997)
![The Fifth Element](https://raw.githubusercontent.com/thrushd/Python-Movie-Barcode/master/output/The%20Fifth%20Element%20(1997).png)

Ghost in the Shell (1995)
![Ghost in the Shell](https://raw.githubusercontent.com/thrushd/Python-Movie-Barcode/master/output/Ghost%20in%20the%20Shell%20(1995).png)
