<p># ebay<br />
Consuming Web services</p>

<p>before &nbsp;<br />
https://github.com/kratark/ebay/issues</p>

<p>$ python categories.py --help<br />
-----------------------------------------------------<br />
categories --rebuild<br />
categories --render &lt;category_id&gt;<br />
categories -h | categories --help<br />
categories --level &lt;LevelLimit&gt;<br />
categories --parent &lt;CategoryParent&gt;<br />
categories --pool &lt;threeds&gt;<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;level | LevelLimit 6 default value<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;parent | CategoryParent 0 default value<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;pool | Threads 350 default value<br />
-----------------------------------------------------</p>

<p>&nbsp;</p>

<p>=========================<br />
&nbsp; &nbsp; &nbsp;Sample Session<br />
=========================</p>

$ python categories.py --rebuild<br />
$ python categories.py --rebuild<br />
$ python categories.py --render 179281<br />
$ ls 179281.html<br />
179281.html<br />
$ ls 179022.html<br />
179022.html<br />
$ python categories.py --render 6666666666<br />
No category with ID: 6666666666</p>

<p>requirements<br />
dominate<br />
ConfigParser<br />
sqlite3<br />
urllib2<br />
lxml</p>
