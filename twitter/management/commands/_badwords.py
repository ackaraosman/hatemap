# coding: utf-8
from __future__ import unicode_literals, print_function


BADWORDS_NOASCIIFY = [
    'kürt',
    'döl',
    'sik',
    'siktir',
    'göt',
]


homofobik = [
    'lezbiyen',
    'nonos',
    'homoseksuel',
    'ipne',
    'ibne',
    'oglanci',
    'got oglani',
    'gotcu',
    'kulampara',
]


irkci = [
    'ermeni köpegi',
    'ermeni dolu',
    'rum tohumu',
    'pis kurt',
    'sahtekar cerkez',
    'sahtekar cerkes',
    'alcak azeri',
    'hain arap',
    'gurcu domuzu',
    'terorist musluman',
    'ermeni',
]


hakaret = [
    'pezevenk',
    'pezeveng',
    'gavat',
    'godos',
    'durzu',
    'at kafasi',
    'got lalesi',
    'yavsak',
    'yavsak',
    'pic',
    'orospu',
    'gotveren',
    'got veren',
    'amcik',
    'amin oglu',
    'pust',
    'yarrak',
    'yarrrak',
    'yarram',
    'yarrram',
    'amk',
    'amina',
    'denyo',
    'subyanci',
    'kavat',
]


BADWORDS = homofobik + irkci + hakaret