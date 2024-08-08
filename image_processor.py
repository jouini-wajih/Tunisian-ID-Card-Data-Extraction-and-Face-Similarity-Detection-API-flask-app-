import sys
import json
import os
import cv2
import re
import easyocr
import numpy as np
from PIL import Image
from object_extractor import Extractor, FRONTALFACE_ALT2
import difflib
from typing import Optional, List
import sim



dictionary = [
    "جانفي", "فيفري", "مارس", "أبريل", "ماي", "جوان", "جويلية", "أوت", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر",
    "الجمهورية", "التونسية", "مكانها", "تاريخ", "الولادة", "بطاقة", "تعريف", "وطني",
    "الاسم", "اللقب",

]
dictionary_p = [
    "تونس", "أريانة", "منوبة", "بن عروس", "زغوان", "نابل", "سوسة", "المهدية",
    "القيروان", "قفصة", "قابس", "مدنين", "تطاوين", "سليانة", "الكاف", "جندوبة",
    "باجة", "طبرقة", "المنستير", "صفاقس", "بنزرت", "توزر", "القلعة الكبرى",
    "قبلي", "برج السدرية", "الجم", "الرديف", "قصر هلال", "قصر قفصة", "بئر علي بن خليفة",
    "الشابة", "جربة", "قصر السعيد", "الزهراء", "المكنين", "أم العرائس", "المظيلة",
    "الشيحية", "قصر تونس", "المنيهلة", "بئر اللقطة", "القلعة الصغرى", "قصر المجاز",
    "قصر الشهداء", "بئر السلام", "العمران", "المرازقة", "الشباب", "التمرة", "الدوائر",
    "الزرار", "مكثر", "تازركة", "سليمان", "الرقاب", "الجزيرة", "حسينية", "الوردانين",
    "المستودع", "الزريبة", "الشراردة", "المهدي", "الهوارية", "تاجروين", "مراكش",
    "الحاجب", "الدويرات", "المرسى", "سيدي بوزيد", "القصرين", "سيدي حسين", "برج بوعريريج",
    "بني خداش", "خميس مليانة", "الجرف", "القلعة الجديدة", "بني مطير", "الرجيم",
    "المجان", "بن سدرين", "المصيف", "سوق الجمعة", "عين دراهم", "العوابد", "الجميلة",
    "قصر الشط", "فريانة", "العالية", "قصر المثلث", "الجرجيس", "البرج", "خنشلة",
    "الشابة", "الرديف", "العلا", "المرناقية", "بني حسان", "الذهيبة", "حلق الوادي",
    "قرطاج", "الصمار", "الأحيّ", "المحمدية", "عين الصبح", "عين البية", "غار الملح",
    "بوسالم", "سيدي مخلوف", "قصر بئر القصر", "قرمبالية", "عين زغوان", "سيدي عيسى",
    "الصخيرة", "الشرقية", "سيدي بوبكر", "الشعانبي", "المنازه", "قصر السعيدة",
    "الديماس", "عالية", "السواحلي", "الوسلاتية", "الميناء", "قصر العطايا", "السبالة",
    "قصر الحمرا", "الحمام", "الشرايع", "العرقوب", "التمور", "المنحلي", "الحي المحمدي",
    "بني خلدون", "بئر الباي", "بئر طبلبة", "الصافية", "برج العكارمة", "الزيتونة",
    "المسرج", "المرناق", "الملاسين", "برج المراقبة", "سيدي بوسعيد", "قصر قفصة",
    "الحامة", "العمارة", "الشعلة", "الزهراء", "سيدي بوسعيد", "الحمامات", "الجريصة",
    "الدندان", "البرج", "شعبي", "قصر الشهداء", "غزالة", "الورقي", "الزعفراني",
    "الدوير", "قصر الشوك", "عين الصرف", "البرج", "قصر الشهداء", "المطار",
    "العرائش", "الدرع", "الخزنة", "الشرايع", "العريش", "البرج", "المسعدين",
    "مساكن", "بئر طبلبة", "برج السدرية", "القيصرية", "الجرجيس", "التوة", "الزرار",
    "الحامة", "شابي", "البرج", "بني تونس", "المسعدين", "قصر الشريف", "الحمام"
]

arabic_to_french = {
    "تونس": "Tunis",
    "أريانة": "Ariana",
    "منوبة": "Manouba",
    "بن عروس": "Ben Arous",
    "زغوان": "Zaghouan",
    "نابل": "Nabeul",
    "سوسة": "Sousse",
    "المهدية": "Mahdia",
    "القيروان": "Kairouan",
    "قفصة": "Gafsa",
    "قابس": "Gabes",
    "مدنين": "Medenine",
    "تطاوين": "Tatouine",
    "سليانة": "Siliana",
    "الكاف": "Kef",
    "جندوبة": "Jendouba",
    "باجة": "Béja",
    "طبرقة": "Tabarka",
    "المنستير": "Monastir",
    "صفاقس": "Sfax",
    "بنزرت": "Bizerte",
    "توزر": "Tozeur",
    "القلعة الكبرى": "El Kalaa Kebira",
    "قبلي": "Kebili",
    "برج السدرية": "Bordj Cedria",
    "الجم": "El Jem",
    "الرديف": "Redeyef",
    "قصر هلال": "Ksar Hellal",
    "قصر قفصة": "Ksar Gafsa",
    "بئر علي بن خليفة": "Bir Ali Ben Khalifa",
    "الشابة": "Chebba",
    "جربة": "Djerba",
    "قصر السعيد": "Ksar Said",
    "الزهراء": "El Zahra",
    "المكنين": "Moknine",
    "أم العرائس": "Om El Araies",
    "المظيلة": "Mdhila",
    "الشيحية": "Chihia",
    "قصر تونس": "Ksar Tunis",
    "المنيهلة": "Mnihla",
    "بئر اللقطة": "Bir El Lkta",
    "القلعة الصغرى": "El Kalaa Sghira",
    "قصر المجاز": "Ksar El Majaz",
    "قصر الشهداء": "Ksar El Chedda",
    "بئر السلام": "Bir Es-Salem",
    "العمران": "El Omrane",
    "المرازقة": "Marazka",
    "الشباب": "Chabab",
    "التمرة": "Tamra",
    "الدوائر": "Douar",
    "الزرار": "Zrar",
    "مكثر": "Mokthar",
    "تازركة": "Tazarka",
    "سليمان": "Sliema",
    "الرقاب": "Rekab",
    "الجزيرة": "Jazira",
    "حسينية": "Hassinia",
    "الوردانين": "Wardane",
    "المستودع": "Mestoudh",
    "الزريبة": "Zriba",
    "الشراردة": "Charrada",
    "المهدي": "Mehdi",
    "الهوارية": "Hawaria",
    "تاجروين": "Tajerouine",
    "مراكش": "Marrakech",
    "الحاجب": "Hajib",
    "الدويرات": "Douairate",
    "المرسى": "La Marsa",
    "سيدي بوزيد": "Sidi Bouzid",
    "القصرين": "Kasserine",
    "سيدي حسين": "Sidi Hussein",
    "برج بوعريريج": "Bordj Bou Arreridj",
    "بني خداش": "Beni Khedach",
    "خميس مليانة": "Khemis Miliana",
    "الجرف": "Jorf",
    "القلعة الجديدة": "El Kalaa El Jedida",
    "بني مطير": "Beni Mtir",
    "الرجيم": "Rejim",
    "المجان": "Majan",
    "بن سدرين": "Ben Sedrine",
    "المصيف": "Mousaaf",
    "سوق الجمعة": "Souk El Jomaa",
    "عين دراهم": "Ain Draham",
    "العوابد": "Aouabed",
    "الجميلة": "Jmila",
    "قصر الشط": "Ksar El Chet",
    "فريانة": "Feriana",
    "العالية": "Alya",
    "قصر المثلث": "Ksar El Mothallath",
    "الجرجيس": "Gharbi",
    "البرج": "Bordj",
    "خنشلة": "Khenchela",
    "الشابة": "Chebba",
    "الرديف": "Redayef",
    "العلا": "El Ala",
    "المرناقية": "Mornaguia",
    "بني حسان": "Beni Hassan",
    "الذهيبة": "Dhéhiba",
    "حلق الوادي": "Halq El Wadi",
    "قرطاج": "Carthage",
    "الصمار": "Smara",
    "الأحيّ": "El Ahyaa",
    "المحمدية": "Mohamedia",
    "عين الصبح": "Ain Sobah",
    "عين البية": "Ain El Bey",
    "غار الملح": "Ghar El Melh",
    "بوسالم": "Bousalem",
    "سيدي مخلوف": "Sidi Mekhlouf",
    "قصر بئر القصر": "Ksar Bir Ksar",
    "قرمبالية": "Kramable",
    "عين زغوان": "Ain Zaghouan",
    "سيدي عيسى": "Sidi Aissa",
    "الصخيرة": "Sakhria",
    "الشرقية": "Charkia",
    "سيدي بوبكر": "Sidi Bou Bker",
    "الشعانبي": "Chaambi",
    "المنازه": "El Menzah",
    "قصر السعيدة": "Ksar Saida",
    "الشابة": "Chebba",
    "الديماس": "Daimas",
    "عالية": "Alya",
    "السواحلي": "Sahli",
    "الوسلاتية": "Ouslatia",
    "الميناء": "Mina",
    "قصر العطايا": "Ksar El Ataya",
    "السبالة": "Sbabla",
    "قصر الحمرا": "Ksar El Hamra",
    "الحمام": "Hammam",
    "الشرايع": "Charaay",
    "البرج": "Bordj",
    "سيدي حسين": "Sidi Hussein",
    "العرقوب": "Akrub",
    "الزرار": "Zrar",
    "الدويرات": "Douairate",
    "التمور": "Tamour",
    "المنحلي": "Manhli",
    "قصر قصر": "Ksar Ksar",
    "السواق": "Souak",
    "بني خلدون": "Beni Kheloud",
    "الحي المحمدي": "Hay Mohamed",
    "المرسى": "La Marsa",
    "قصر السعيد": "Ksar Said",
    "برج السدرية": "Bordj Cedria",
    "الجم": "El Jem",
    "الرديف": "Redeyef",
    "قصر هلال": "Ksar Hellal",
    "بئر علي بن خليفة": "Bir Ali Ben Khalifa",
    "الشابة": "Chebba",
    "جربة": "Djerba",
    "قصر السعيد": "Ksar Said",
    "الزهراء": "El Zahra",
    "المكنين": "Moknine",
    "أم العرائس": "Om El Araies",
    "المظيلة": "Mdhila",
    "الشيحية": "Chihia",
    "قصر تونس": "Ksar Tunis",
    "المنيهلة": "Mnihla",
    "بئر اللقطة": "Bir El Lkta",
    "القلعة الصغرى": "El Kalaa Sghira",
    "قصر المجاز": "Ksar El Majaz",
    "قصر الشهداء": "Ksar El Chedda",
    "بئر السلام": "Bir Es-Salem",
    "العمران": "El Omrane",
    "المرازقة": "Marazka",
    "الشباب": "Chabab",
    "التمرة": "Tamra",
    "الدوائر": "Douar",
    "الزرار": "Zrar",
    "مكثر": "Mokthar",
    "تازركة": "Tazarka",
    "سليمان": "Sliema",
    "الرقاب": "Rekab",
    "الجزيرة": "Jazira",
    "حسينية": "Hassinia",
    "الوردانين": "Wardane",
    "المستودع": "Mestoudh",
    "الزريبة": "Zriba",
    "الشراردة": "Charrada",
    "المهدي": "Mehdi",
    "الهوارية": "Hawaria",
    "تاجروين": "Tajerouine",
    "مراكش": "Marrakech",
    "الحاجب": "Hajib",
    "الدويرات": "Douairate",
    "المرسى": "La Marsa",
    "سيدي بوزيد": "Sidi Bouzid",
    "القصرين": "Kasserine",
    "سيدي حسين": "Sidi Hussein",
    "برج بوعريريج": "Bordj Bou Arreridj",
    "بني خداش": "Beni Khedach",
    "خميس مليانة": "Khemis Miliana",
    "الجرف": "Jorf",
    "القلعة الجديدة": "El Kalaa El Jedida",
    "بني مطير": "Beni Mtir",
    "الرجيم": "Rejim",
    "المجان": "Majan",
    "بن سدرين": "Ben Sedrine",
    "المصيف": "Mousaaf",
    "سوق الجمعة": "Souk El Jomaa",
    "عين دراهم": "Ain Draham",
    "العوابد": "Aouabed",
    "الجميلة": "Jmila",
    "قصر الشط": "Ksar El Chet",
    "فريانة": "Feriana",
    "العالية": "Alya",
    "قصر المثلث": "Ksar El Mothallath",
    "الجرجيس": "Gharbi",
    "البرج": "Bordj",
    "خنشلة": "Khenchela",
    "الشابة": "Chebba",
    "الرديف": "Redayef",
    "العلا": "El Ala",
    "المرناقية": "Mornaguia",
    "بني حسان": "Beni Hassan",
    "الذهيبة": "Dhéhiba",
    "حلق الوادي": "Halq El Wadi",
    "قرطاج": "Carthage",
    "الصمار": "Smara",
    "الأحيّ": "El Ahyaa",
    "المحمدية": "Mohamedia",
    "عين الصبح": "Ain Sobah",
    "عين البية": "Ain El Bey",
    "غار الملح": "Ghar El Melh",
    "بوسالم": "Bousalem",
    "سيدي مخلوف": "Sidi Mekhlouf",
    "قصر بئر القصر": "Ksar Bir Ksar",
    "قرمبالية": "Kramable",
    "عين زغوان": "Ain Zaghouan",
    "سيدي عيسى": "Sidi Aissa",
    "الصخيرة": "Sakhria",
    "الشرقية": "Charkia",
    "سيدي بوبكر": "Sidi Bou Bker",
    "الشعانبي": "Chaambi",
    "المنازه": "El Menzah",
    "قصر السعيدة": "Ksar Saida",
    "الشابة": "Chebba",
    "الديماس": "Daimas",
    "عالية": "Alya",
    "السواحلي": "Sahli",
    "الوسلاتية": "Ouslatia",
    "الميناء": "Mina",
    "قصر العطايا": "Ksar El Ataya",
    "السبالة": "Sbabla",
    "قصر الحمرا": "Ksar El Hamra",
    "الحمام": "Hammam",
    "الشرايع": "Charaay",
    "البرج": "Bordj",
    "سيدي حسين": "Sidi Hussein",
    "العرقوب": "Akrub",
    "الزرار": "Zrar",
    "الدويرات": "Douairate",
    "التمور": "Tamour",
    "المنحلي": "Manhli",
    "قصر قصر": "Ksar Ksar",
    "السواق": "Souak",
    "بني خلدون": "Beni Kheloud",
    "الحي المحمدي": "Hay Mohamed",
    "المرسى": "La Marsa",
    "قصر السعيد": "Ksar Said",
    "برج السدرية": "Bordj Cedria",
    "الجم": "El Jem",
    "الرديف": "Redeyef",
    "قصر هلال": "Ksar Hellal",
    "بئر علي بن خليفة": "Bir Ali Ben Khalifa",
    "الشابة": "Chebba",
    "جربة": "Djerba",
    "قصر السعيد": "Ksar Said",
    "الزهراء": "El Zahra",
    "المكنين": "Moknine",
    "أم العرائس": "Om El Araies",
    "المظيلة": "Mdhila",
    "الشيحية": "Chihia",
    "قصر تونس": "Ksar Tunis",
    "المنيهلة": "Mnihla",
    "بئر اللقطة": "Bir El Lkta",
    "القلعة الصغرى": "El Kalaa Sghira",
    "قصر المجاز": "Ksar El Majaz",
    "قصر الشهداء": "Ksar El Chedda",
    "بئر السلام": "Bir Es-Salem",
    "العمران": "El Omrane",
    "المرازقة": "Marazka",
    "الشباب": "Chabab",
    "التمرة": "Tamra",
    "الدوائر": "Douar",
    "الزرار": "Zrar",
    "مكثر": "Mokthar",
    "تازركة": "Tazarka",
    "سليمان": "Sliema",
    "الرقاب": "Rekab",
    "الجزيرة": "Jazira",
    "حسينية": "Hassinia",
    "الوردانين": "Wardane",
    "المستودع": "Mestoudh",
    "الزريبة": "Zriba",
    "الشراردة": "Charrada",
    "المهدي": "Mehdi",
    "الهوارية": "Hawaria",
    "تاجروين": "Tajerouine",
    "مراكش": "Marrakech",
    "الحاجب": "Hajib",
    "الدويرات": "Douairate",
    "المرسى": "La Marsa",
    "سيدي بوزيد": "Sidi Bouzid",
    "القصرين": "Kasserine",
    "سيدي حسين": "Sidi Hussein",
    "برج بوعريريج": "Bordj Bou Arreridj",
    "بني خداش": "Beni Khedach",
    "خميس مليانة": "Khemis Miliana",
    "الجرف": "Jorf",
    "القلعة الجديدة": "El Kalaa El Jedida",
    "بني مطير": "Beni Mtir",
    "الرجيم": "Rejim",
    "المجان": "Majan",
    "بن سدرين": "Ben Sedrine",
    "المصيف": "Mousaaf",
    "سوق الجمعة": "Souk El Jomaa",
    "عين دراهم": "Ain Draham",
    "العوابد": "Aouabed",
    "الجميلة": "Jmila",
    "قصر الشط": "Ksar El Chet",
    "فريانة": "Feriana",
    "العالية": "Alya",
    "قصر المثلث": "Ksar El Mothallath",
    "الجرجيس": "Gharbi",
    "البرج": "Bordj",
    "خنشلة": "Khenchela",
    "الشابة": "Chebba",
    "الرديف": "Redayef",
    "العلا": "El Ala",
    "المرناقية": "Mornaguia",
    "بني حسان": "Beni Hassan",
    "الذهيبة": "Dhéhiba",
    "حلق الوادي": "Halq El Wadi",
    "قرطاج": "Carthage",
    "الصمار": "Smara",
    "الأحيّ": "El Ahyaa",
    "المحمدية": "Mohamedia",
    "عين الصبح": "Ain Sobah",
    "عين البية": "Ain El Bey",
    "غار الملح": "Ghar El Melh",
    "بوسالم": "Bousalem",
    "سيدي مخلوف": "Sidi Mekhlouf",
    "قصر بئر القصر": "Ksar Bir Ksar",
    "قرمبالية": "Kramable",
    "عين زغوان": "Ain Zaghouan",
    "سيدي عيسى": "Sidi Aissa",
    "الصخيرة": "Sakhria",
    "الشرقية": "Charkia",
    "سيدي بوبكر": "Sidi Bou Bker",
    "الشعانبي": "Chaambi",
    "المنازه": "El Menzah",
    "قصر السعيدة": "Ksar Saida",
    "الشابة": "Chebba",
    "الديماس": "Daimas",
    "عالية": "Alya",
    "السواحلي": "Sahli",
    "الوسلاتية": "Ouslatia",
    "الميناء": "Mina",
    "قصر العطايا": "Ksar El Ataya",
    "السبالة": "Sbabla",
    "قصر الحمرا": "Ksar El Hamra",
    "الحمام": "Hammam",
    "الشرايع": "Charaay",
    "البرج": "Bordj",
    "سيدي حسين": "Sidi Hussein",
    "العرقوب": "Akrub",
    "الزرار": "Zrar",
    "الدويرات": "Douairate",
    "التمور": "Tamour",
    "المنحلي": "Manhli",
    "قصر قصر": "Ksar Ksar",
    "السواق": "Souak",
    "بني خلدون": "Beni Kheloud",
    "الحي المحمدي": "Hay Mohamed",
    "المرسى": "La Marsa",
    "قصر السعيد": "Ksar Said",
    "برج السدرية": "Bordj Cedria",
    "الجم": "El Jem",
    "الرديف": "Redeyef",
    "قصر هلال": "Ksar Hellal",
    "بئر علي بن خليفة": "Bir Ali Ben Khalifa",
    "الشابة": "Chebba",
    "جربة": "Djerba",
    "قصر السعيد": "Ksar Said",
    "الزهراء": "El Zahra",
    "المكنين": "Moknine",
    "أم العرائس": "Om El Araies",
    "المظيلة": "Mdhila",
    "الشيحية": "Chihia",
    "قصر تونس": "Ksar Tunis",
    "المنيهلة": "Mnihla",
    "بئر اللقطة": "Bir El Lkta",
    "القلعة الصغرى": "El Kalaa Sghira",
    "قصر المجاز": "Ksar El Majaz",
    "قصر الشهداء": "Ksar El Chedda",
    "بئر السلام": "Bir Es-Salem",
    "العمران": "El Omrane",
    "المرازقة": "Marazka",
    "الشباب": "Chabab",
    "التمرة": "Tamra",
    "الدوائر": "Douar",
    "الزرار": "Zrar",
    "مكثر": "Mokthar",
    "تازركة": "Tazarka",
    "سليمان": "Sliema",
    "الرقاب": "Rekab",
    "الجزيرة": "Jazira",
    "حسينية": "Hassinia",
    "الوردانين": "Wardane",
    "المستودع": "Mestoudh",
    "الزريبة": "Zriba",
    "الشراردة": "Charrada",
    "المهدي": "Mehdi",
    "الهوارية": "Hawaria",
    "تاجروين": "Tajerouine",
    "مراكش": "Marrakech",
    "الحاجب": "Hajib",
    "الدويرات": "Douairate",
    "المرسى": "La Marsa",
    "سيدي بوزيد": "Sidi Bouzid",
    "القصرين": "Kasserine",
    "سيدي حسين": "Sidi Hussein",
    "برج بوعريريج": "Bordj Bou Arreridj",
    "بني خداش": "Beni Khedach",
    "خميس مليانة": "Khemis Miliana",
    "الجرف": "Jorf",
    "القلعة الجديدة": "El Kalaa El Jedida",
    "بني مطير": "Beni Mtir",
    "الرجيم": "Rejim",
    "المجان": "Majan",
    "بن سدرين": "Ben Sedrine",
    "المصيف": "Mousaaf",
    "سوق الجمعة": "Souk El Jomaa",
    "عين دراهم": "Ain Draham"
}


# Preprocessing function
def preprocess_image(image_path):
    print("Preprocessing image...")
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error loading image at {image_path}")
        return None, None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    print("Image preprocessing complete.")
    return thresh, img

# Text detection function
def detect_text(image):
    print("Detecting text...")
    reader = easyocr.Reader(['ar'])
    
    results = reader.readtext(image)
    print("text detection complete...")
    results_sorted = sorted(results, key=lambda x: (x[0][0][1], x[0][0][0]))
    print(f"Detected {len(results_sorted)} text regions.")
    return results_sorted

# Text aggregation function
def aggregate_text_by_lines(results):
    print("Aggregating text by lines...")
    lines = []
    current_line = []
    previous_y = None
    box_expansion = 10

    for (bbox, text, prob) in results:
        top_left = bbox[0]
        bottom_right = bbox[2]
        x1, y1 = top_left
        x2, y2 = bottom_right
        expanded_y_min = y1 - box_expansion
        expanded_y_max = y2 + box_expansion

        if previous_y is None:
            current_line = [(bbox, text)]
            line_y_min = expanded_y_min
            line_y_max = expanded_y_max
        else:
            if y1 < line_y_max:
                current_line.append((bbox, text))
                line_y_min = min(line_y_min, expanded_y_min)
                line_y_max = max(line_y_max, expanded_y_max)
            else:
                lines.append(' '.join([text for (_, text) in current_line]))
                current_line = [(bbox, text)]
                line_y_min = expanded_y_min
                line_y_max = expanded_y_max

        previous_y = y2

    if current_line:
        lines.append(' '.join([text for (_, text) in current_line]))

    print(f"Aggregated text into {len(lines)} lines.")
    return lines

# Correct Arabic text function
def correct_arabic_text(text, dictionary, min_match_ratio=0.7):
    print("Correcting Arabic text...")
    words = re.findall(r'\b\w+\b', text)

    def correct_word(word):
        matches = difflib.get_close_matches(word, dictionary, n=1, cutoff=min_match_ratio)
        if matches:
            return matches[0]
        else:
            return word
    
    corrected_words = []
    for word in words:
        corrected_word = correct_word(word)
        if corrected_word != word and difflib.SequenceMatcher(None, word, corrected_word).ratio() < min_match_ratio:
            segments = re.findall(r'\b\w+\b', word)
            corrected_segments = [correct_word(segment) for segment in segments]
            corrected_words.append(' '.join(corrected_segments))
        else:
            corrected_words.append(corrected_word)
    
    corrected_text = ' '.join(corrected_words)
    print("Arabic text correction complete.")
    return corrected_text

# Extract birthdate function
def extract_birthdate(text: str) -> Optional[str]:
    print("Extracting birthdate...")
    arabic_months = ["جانفي", "فيفري", "مارس", "أبريل", "ماي", "جوان", "جويلية", "أوت", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
    mois_arabes = {
    "جانفي": "Janvier",
    "فيفري": "Février",
    "مارس": "Mars",
    "أبريل": "Avril",
    "ماي": "Mai",
    "جوان": "Juin",
    "جويلية": "Juillet",
    "أوت": "Août",
    "سبتمبر": "Septembre",
    "أكتوبر": "Octobre",
    "نوفمبر": "Novembre",
    "ديسمبر": "Décembre"
}
    day_matches = re.findall(r'\b\d{2}\b', text)
    year_matches = re.findall(r'\b\d{4}\b', text)
    month_matches = [month for month in arabic_months if month in text]
    
    if not (day_matches and year_matches and month_matches):
        print("Birthdate extraction failed: No valid date components found.")
        return None

    day = min(day_matches, key=lambda d: int(d))
    year = max(year_matches, key=lambda y: int(y))
    month = mois_arabes[month_matches[0]]

    birthdate = f"{day} {month} {year}"
    print(f"Extracted birthdate: {birthdate}")
    return birthdate

# Extract 8-digit number function
def extract_eight_digit_number(text):
    print("Extracting 8-digit number...")
    pattern = r'\b\d{8}\b'
    match = re.search(pattern, text)
    if match:
        id_number = match.group(0)
        print(f"Extracted 8-digit number: {id_number}")
        return id_number
    else:
        print("No 8-digit number found.")
        return None


def sol4(results):
        text_list = [r[1] for r in results]
        text = ' '.join(text_list)
        text=correct_arabic_text(text, dictionary)
        for p in text.split():
          if p in dictionary_p:
            return arabic_to_french[p]

        return None

def sol1(results):
      dictionary = [
        "مكانها"
      ]
      mid=0
      for r in results:
        if correct_arabic_text(r[1], dictionary)=="مكانها":
          mid=((r[0][0][1]+r[0][3][1])/2)
     

      for r in results:
        if  r[0][0][1] <mid<r[0][3][1] and (correct_arabic_text(r[1], dictionary)!="مكانها"):
          for p in r[1].split():
            print(p)
            if p in dictionary_p:
              return arabic_to_french[p]
            else :
              return None 

      
def sol2(results):
   results_sorted = sorted(results, key=lambda x: (x[0][0][1], x[0][0][0]))
   rev=reversed(results_sorted)
   for x in rev:
     place=correct_arabic_text(x[1], dictionary_p)
     
     for p in place.split():
       if p in dictionary_p:
         return arabic_to_french[p]
       else :
        return None


def sol3(results):
  for r in results:
        pattern = re.compile(r'\b\w+\b', re.UNICODE)
        words = pattern.findall(correct_arabic_text(r[1], dictionary))
        if "مكانها" in words:
          for i in range(0,len(words)):
            if words[i] in dictionary_p:
              return arabic_to_french[words[i]]
  return None          



def get_place(results):
    res= sol1(results)
    res2= sol2(results)
    res3= sol3(results)
    res4 = sol4(results)
    if res4:
       return res4
    if res :
      return res
    else :
      if res2 :
        return res2
      else : 
        return res3






def process_image(image_path):
    print("Starting image processing...")
    result = {'birth': None, 'id': None,'place':None,'sim':None}
    extracted_face_path = sim.extract_face_from_image(image_path)
    thresh, img = preprocess_image(image_path)
    best_distance = sim.get_best_similarity_distance(extracted_face_path)
    extracted_face_path = sim.extract_face_from_image(image_path,"./output")
    if img is not None:
        results = detect_text(img)
        text_list = [r[1] for r in results]
        text = ' '.join(text_list)
        text = correct_arabic_text(text, dictionary)
        result['birth'] = extract_birthdate(text)
        result['id'] = extract_eight_digit_number(text)
        result["place"]=get_place(results)
        result["sim"]=best_distance
    
    print("Image processing complete.")
    return result

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(json.dumps({'error': 'Invalid arguments'}), file=sys.stderr)
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = process_image(image_path)
    print(json.dumps(result))
