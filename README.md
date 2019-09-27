Bdf to image
=====
Converts bdf fonts to image file.

Usage
-----
`./bdftoimg.py <filename> <outputfile> [--jis-to-sjis]`

* `--jis-to-sjis` convert JIS X xxxx encoding to SHIFT JIS.

Example
-----
`./bdftoimg.py shnm6x12r.bdf shnm6x12r.png --jis-to-sjis`

If you have a [Shinonome font](http://openlab.ring.gr.jp/efont/shinonome/index.html.ja) file called shnm6x12r.bdf and run the command above, then you get the following image.

![command output](./shnm6x12r.png "Command output")

License
-----
This software is released under MIT License.
