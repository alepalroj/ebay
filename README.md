# ebay
Consuming Web services

categories.py
  #default category to get from ws 10542 
  response = request.getCategories(10542)

before  
https://github.com/kratark/ebay/issues

=========================
     Sample Session
=========================

% python categories.py --rebuild
% python categories.py --rebuild
% python categories.py --render 179281
% ls 179281.html
179281.html
% ls 179022.html
179022.html
% python categories.py --render 6666666666
No category with ID: 6666666666

requirements
dominate
ConfigParser
sqlite3
urllib2
lxml


  

