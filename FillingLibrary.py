import redis
from PublisherSubscriber import *

publisherSport = BookPublisher("Sport")
publisherArt = BookPublisher("Art")
publisherScience = BookPublisher("Science")
publisherNovel = BookPublisher("Novel")

### Publish Sport Books
publisherSport.add_book('1001','Sport','Handball','Dika Mem','French','2018',number=3)
publisherSport.add_book('1002','Sport','Basketball','Jimmy Butler','English','2003')
publisherSport.add_book('1003','Sport','Football','Pele','Brasilian','1980')
publisherSport.add_book('1004','Sport','Tennis','Roger Federer','German','2005',number=5)
publisherSport.add_book('1005','Sport','Rugby History','Jonah Lomu','Maori','1995',number=2)
publisherSport.add_book('1006','Sport','F1 superstar','Lewis Hamilton','English','2006')
publisherSport.add_book('1007','Sport','How to become Athletic','The Mountain','Icelandic','2009',number=2)
publisherSport.add_book('1008','Sport','Calisthenic basics','Simone Biles','English','2013')
publisherSport.add_book('1009','Sport','Swimming like a butterfly : Really ?','Michael Phelps','English','1999')
publisherSport.add_book('1010','Sport','Running like Forest','Usain Bolt','English','1994')

###Publish Art Books
publisherArt.add_book('2001','Art','Street Art','Banksy','English','2002',number=3)
publisherArt.add_book('2002','Art','Smiling Face','Mona Lisa','Italian','1509')
publisherArt.add_book('2003','Art','Modern Art','Monet Claude','French','1902')
publisherArt.add_book('2004','Art','Carving a curve','Robin Rodin','English','1911')
publisherArt.add_book('2005','Art','Frozen human','Pompei Volcano','Italian','79')
publisherArt.add_book('2006','Art','Decorate your house','Stephane Plaza','French','2017',number=6)
publisherArt.add_book('2007','Art','Ink Mastering','Freaky Hoody','English','2022')

###Publish Science Books
publisherScience.add_book('3001','Science','Terraforming Mars !?','Elon Musk','English','2019')
publisherScience.add_book('3002','Science','Molecular Gastronomy','Einstein Etchebest','German','2008')
publisherScience.add_book('3003','Science','Apple Gravity','Isaac Newton','English','1703',number=3)
publisherScience.add_book('3004','Science','Magic electricity','Alessandro Volta','Italian','1799')
publisherScience.add_book('3005','Science','Buffalo Anatomy','David Crocket','English','1802')
publisherScience.add_book('3006','Science','Climate Change','Greta Thunberg','English','2015',number=4)
publisherScience.add_book('3007','Science','Dealing with nuclear waste','Sebastien Quinn','English','2023')
publisherScience.add_book('3008','Science','Finance model and equation','Christopher Tks','Chinese','2020',number=10)
publisherScience.add_book('3009','Science','Modelization in aeronautics','Louis-Hadrien Gros','English','2019',number=3)

###Publish Novel Books
publisherNovel.add_book('4001','Novel','Immortal','Chuck Norris','English','1980')
publisherNovel.add_book('4002','Novel','Canice Glowen','Edmond Fauret','French','1869',number=2)
publisherNovel.add_book('4003','Novel','Orientation Adventure','Zoro Roronoa','English','1997')