# -*- coding: latin-1 -*-

import random

#I've chosen not to use the default i18n/gettext way to handle languages,
#as I do not have any knowledge of the target machine this will run on

MESSAGES = { 'en': {},
             'nl': {},
             'fr': {}
            }


MESSAGES['en'] = {
    "lowappetite": {
        "title": u"Appetite",
        "messages": [
            u"Eating regular meals is important.",
            u"Wholesome meals will give you more energy.",
            u"Proper hydration helps clear thinking.",
            u"Proper hydration helps better concentration.",
            u"Staying hydrated ensures that your organs work properly.",
            u"Have a nutritious breakfast to fill you with energy for the day.",
            u"Keep your body fueled for the afternoon with a healthy lunch.",
            u"Let's try a new recipe.",
            u"How about inviting somebody over for lunch/dinner?",
            u"How about a small healthy snack?",
            u"Don't forget: eating 5 fruits and vegetables per day is good for your health!",
            u"An apple a day keeps a doctor away!",
            u"Try to eat some starchy foods every day as part of a healthy, balanced nutrition.",
            u"Eat varied and balanced products.",
            u"Pay attention to high-fat, high-salt or high-sugar products."
        ]
    },
    "highappetite": {
        "title": u"Appetite",
        "messages": [
            u"Choosing healthy foods will help you to stay fit for the future.",
            u"Choosing healthy foods will make you feel vibrant and healthy, inside and out.",
            u"Good nutrition is essential for the brain to do its job.",
            u"Good nutrition keeps muscles, bones and organs strong.",
            u"Include a healthy fruit or veggie at every meal.",
            u"Let's try a new recipe.",
            u"How about inviting somebody over for lunch/dinner?",
            u"Drinking water 30 minutes before a meal helps digestion.",
            u"Don't forget to take your medicine.",
            u"Don't forget to check a new receipt from Jamie's Oliver website! It looks delicious and simply to cook.",
            u"Don't forget to drink a lot of water, at least 1.5 per day."
        ]
    },
    "highbathroom": {
        "title": u"Health",
        "messages": [
            u"Be careful when getting in and out of the tub/shower.",
            u"Put your toiletries within reach when taking a bath/shower.",
            u"Pay attention on the slipper floor",
            u"Don't forget to hang on when you are getting in/out the bath tub/shower",
            u"Put non-slip mat or materials."
        ]
    },
    "lowbedroom": {
        "title": u"Sleep",
        "messages": [
            u"Sleeping well is essential to your physical health.",
            u"Sleeping well is important for your emotional well-being.",
            u"A good night's sleep helps improve memory formation.",
            u"A good night's sleep helps improve concentration.",
            u"A good night's sleep refreshes your immune system.",
            u"Reading a book may help you sleep better.",
            u"You must be relaxed to get to sleep"
        ]
    },
    "highbedroom": {
        "title": u"Sleep",
        "messages": [
            u"Don't forget to take your medicine.",
            u"Sleeping well is essential to your physical health.",
            u"Sleeping well is important for your emotional well-being.",
            u"A good night's sleep helps improve memory formation.",
            u"A good night's sleep helps improve concentration.",
            u"A good night's sleep refreshes your immune system.",
            u"Try to listen to some classical music in your bedroom. It may help you to get relaxed and to go to sleep.",
            u"Sleeping good is an important part of your physical and moral well-being"
        ]
    },
    "lowactivity": {
        "title": u"Activity",
        "messages": [
            u"Exercise will boost your mood.",
            u"Exercise reduces stress, depression, and anxiety.",
            u"How about going for a walk?",
            u"How about meeting with a friend?",
            u"How about visiting the family?",
            u"How about joining a seniors' group?",
            u"How about taking an adult education class?",
            u"How about becoming a volunteer?",
            u"Try to get at least two hours of sunlight a day.",
            u"Check out SONOPAs interests groups",
#            u"Maybe this is interesting for you: event X",
            u"Use SONOPA to give a friend/ your family a video call.",
            u"How about inviting some friends or family to your place?",
            u"How about playing a game in SONOPA network?"
        ]
    },
    "personenters": {
        "title": u"Activity",
        "messages": [
            u"Welcome Home!",
            u"How about a small healthy snack?",
            u"Have a glass of water/cup of tea/coffee",
            u"Check SONOPA to see what your friends have been up to",
            u"Check out SONOPA's interests groups",
#            u"You have 2 new calls from X.",
#            u"Today there is a good film on the TV at 7p.m.",
#            u"You have 4 new notifications from SONOPA members."
        ]
    },
    "personleaves": {
        "title": u"Activity",
        "messages": [
            u"Goodbye!",
            u"Did you pack everything you need?",
            u"How about visiting a friend later?",
            u"How about visiting the family later?",
            u"Don't forget to buy your medicine/pills/ some fruits/bread... go to the supermarket/shop/ grocery shop... on your way home!",
#            u"Don't forget your appointment at../ to call Mr X...!",
            u"Did you forget something?"
        ]
    }
}


MESSAGES['nl'] = {
    "lowappetite": {
        "title": u"Eetlust",
        "messages": [
            u"Regelmatig eten is belangrijk.",
            u"Van gezonde maaltijden krijgt u meer energie. ",
            u"Voldoende drinken helpt helder denken.",
            u"Voldoende drinken helpt beter te concentreren.",
            u"Blijvend gehydrateerd zijn zorgt ervoor dat je organen goed werken.",
            u"Neem een voedzaam ontbijt zo krijgt u energie voor de hele dag.",
            u"Houd uw lichaam aangewakkerd voor de middag met een gezonde lunch",
            u"Laten we een nieuw recept proberen.",
            u"Wat denk je ervan om iemand uit te nodigen voor lunch/diner?",
            u"Zin in een kleine gezonde snack?",
            u"Niet vergeten: 5 stuks groenten en fruit per dag eten is goed voor uw gezondheid!",
            u"Een appel per dag houdt een dokter weg!",
            u"Probeer elke dag een paar zetmeelrijke voedingsmiddelen te eten als onderdeel van een gezonde, evenwichtige voeding.",
            u"Eet gevarieerde en evenwichtige producten.",
            u"Let op voor producten die veel vet, zout en suiker bevatten."
        ]
    },
    "highappetite": {
        "title": u"Eetlust",
        "messages": [
            u"Kiezen voor gezond voedsel zal u helpen om fit te blijven voor de toekomst.",
            u"Kiezen voor gezond voedsel zal je levendig en gezond doen voelen, vanbinnen en vanbuiten.",
            u"Goede voeding is essentieel voor de hersenen.",
            u"Goede voeding houdt spieren, botten en organen sterk.",
            u"Elke maaltijd moet fruit of groente bevatten.",
            u"Laten we een nieuw recept proberen.",
            u"Wat denk je ervan om iemand uit te nodigen voor lunch/diner?",
            u"Water drinken 30 minuten voor een maaltijd helpt de spijsvertering.",
            u"Niet vergeten uw geneesmiddel in te nemen.",
            u"Vergeet niet om de nieuwe recepten te bekijken op de website van Jamie Oliver! Het ziet er heerlijk en eenvoudig uit om te koken.",
            u"Vergeet niet om veel water te drinken, ten minste 1,5 liter per dag."
        ]
    },
    "highbathroom": {
        "title": u"Gezondheid",
        "messages": [
            u"Wees voorzichtig als je in en uit het bad of de douche stapt.",
            u"Zet uw toiletartikelen binnen handbereik bij het nemen van een bad/douche.",
            u"Pas op dat je niet uitglijdt.",
            u"Niet vergeten om je goed vast te houden wanneer je in / uit het bad  of de douche komt.",
            u"Plaats een anti-slip mat of andere anti-slip materialen"
        ]
    },
    "lowbedroom": {
        "title": u"Slapen",
        "messages": [
            u"Goed slapen is essentieel voor uw fysieke gezondheid.",
            u"Goed slapen is belangrijk voor uw emotionele welzijn ",
            u"Een goede nachtrust komt uw geheugen ten goede",
            u"Een goede nachtrust verbetert je concentratie ",
            u"Een goede nachtrust verbetert uw immuunsysteem ",
            u"Een boek lezen zou je kunnen helpen om beter te slapen",
            u"Je moet ontspannen zijn wanneer je gaat slapen."
        ]
    },
    "highbedroom": {
        "title": u"Slapen",
        "messages": [
            u"Vergeet uw geneesmiddel niet in te nemen.",
            u"Goed slapen is essentieel voor uw fysieke gezondheid.",
            u"Goed slapen is belangrijk voor uw emotionele welzijn ",
            u"Een goede nachtrust komt uw geheugen ten goede",
            u"Een goede nachtrust verbetert je concentratie ",
            u"Een goede nachtrust verbetert uw immuunsysteem ",
            u"Probeer te luisteren naar wat klassieke muziek in uw slaapkamer. Het kan helpen u te ontspannen en om te gaan slapen.",
            u"Goed slapen is een belangrijk onderdeel van uw fysieke en morele welzijn"
        ]
    },
    "lowactivity": {
        "title": u"Activiteit",
        "messages": [
            u"Oefening zal je gemoedstoestand verbeteren.",
            u"Oefening vermindert stress, depressie, en angst",
            u"Wat denk je van een wandeling?",
            u"Zin om af te spreken met een vriend?",
            u"Wat denk je van een bezoek aan de familie?",
            u"Wat denk je van je aan te sluiten bij een groep voor senioren?",
            u"Zin om een cursus te volgen?",
            u"Misschien kun je vrijwilliger worden?",
            u"Probeer om minstens twee uur zonlicht te krijgen per dag.",
            u"Bekijk de interessegroepen van SONOPA.",
#            u"Misschien heb je interesse in: gebeurtenis X ",
            u"Gebruik SONOPA om een videogesprek te hebben met een vriend/uw familie.",
            u"Wat denk je ervan om vrienden of familie uit te nodigen?",
            u"Zin om een spel te spelen in het SONOPA netwerk?"
        ]
    },
    "personenters": {
        "title": u"Activiteit",
        "messages": [
            u"Welkom thuis!",
            u"Zin in een kleine gezonde snack?",
            u"Neem een glas water/kopje koffie/ thee",
            u"Controleer SONOPA om te zien wat uw vrienden gedaan hebben. ",
            u"Bekijk de SONOPA interesse groepen",
#            u"Je hebt 2 nieuwe oproepen van X.",
#            u"Vandaag is er een goede film op de TV om 19u",
#            u"Er zijn 4 nieuwe meldingen van SONOPA leden."
        ]
    },
    "personleaves": {
        "title": u"Activiteit",
        "messages": [
            u"Tot ziens!",
            u"Heb je alles mee? ",
            u"Zin om later een bezoek te brengen aan een vriend?",
            u"Zin om later een bezoek te brengen aan de familie?",
            u"Vergeet niet om uw geneeskunde/pillen/vruchten/brood... te kopen. Ga naar de supermarkt/winkel... op uw weg naar huis!",
#            u"Niet vergeten uw afspraak bij... / Bel heer X...!",
            u"Ben je iets vergeten?"
        ]
    }
}


MESSAGES['fr'] = {
    "lowappetite": {
        "title": u"Appétit",
        "messages": [
            u"Mangez des repas à intervalle régulier",
            u"Les repas vous apporteront plus d'énergie",
            u"Une bonne hydratation aide à penser clairement",
            u"Une bonne hydratation apporte une meilleure concentration",
            u"Rester hydraté vous assure un bon fonctionnement de l'organisme",
            u"Un bon petit-déjeuner vous apporte de l'énergie pour la journée",
            u"Un déjeuner sain permet de conserver plein d'énergie pour l'après-midi",
            u"Testons une nouvelle recette !",
            u"Pourquoi ne pas inviter quelqu'un pour le déjeuner/dîner ?",
            u"Pourquoi ne pas préparer un petit encas sain ?",
            u"Cinq fruits et légumes par jour, c'est bon pour la santé !",
            u"Manger une pomme chaque jour permet de conserver une bonne santé !",
            u"Manger des féculents à chaque repas aide à maintenir une alimentation saine et équilibrée",
            u"Manger des produits variés et équilibrés",
            u"Veiller à ne pas manger trop gras, trop sucré ou trop salé"
        ]
    },
    "highappetite": {
        "title": u"Appétit",
        "messages": [
            u"Choisir des produits sains aide à rester en forme",
            u"Choisir des produits sains aide à se sentir dynamique et à garde bonne mine",
            u"Une bonne alimentation est essentielle pour l'esprit",
            u"Une bonne alimentation conserve les muscles, les os et les organes en bonne santé",
            u"Inclure un fruit ou un légume à chaque repas",
            u"Testons une nouvelle recette",
            u"Pourquoi ne pas inviter quelqu'un pour le déjeuner/dîner ? ",
            u"Boire de l'eau 30 minutes avant le repas facilite la digestion",
            u"N'oubliez pas de prendre vos médicaments",
            u"Pourquoi ne pas essayer une nouvelle recette sur le site de Jamie Oliver ? Cela semble délicieux et simple à cuisiner.",
            u"Boire beaucoup d'eau, au moins 1,5 litre par jour"
        ]
    },
    "highbathroom": {
        "title": u"Santé",
        "messages": [
            u"Faites attention lorsque vous entrez ou sortez de la douche/de la baignoire",
            u"Gardez vos articles de toilette à portée de main lorsque vous prenez un bain/une douche",
            u"Prenez garde au sol glissant !",
            u"N'oubliez pas de vous accrocher lorsque vous entrez/sortez de la baignoire/de la douche",
            u"Placer des matériaux et des tapis antidérapants "
        ]
    },
    "lowbedroom": {
        "title": u"Dormir",
        "messages": [
            u"Bien dormir est essentiel pour votre santé",
            u"Bien dormir est important pour votre bien-être psychologique",
            u"Une bonne nuit de sommeil aide améliore la mémoire",
            u"Une bonne nuit de sommeil améliore la concentration",
            u"Une bonne nuit de sommeil revigore le système immunitaire",
            u"Lire un livre aide à trouver le sommeil et à bien dormir",
            u"Il faut être détendu pour trouver le sommeil"
        ]
    },
    "highbedroom": {
        "title": u"Dormir",
        "messages": [
            u"N'oubliez pas de prendre vos médicaments",
            u"Bien dormir est essentiel pour votre santé",
            u"Bien dormir est important pour votre bien-être psychologique",
            u"Une bonne nuit de sommeil aide améliore la mémoire",
            u"Une bonne nuit de sommeil améliore la concentration",
            u"Une bonne nuit de sommeil revigore le système immunitaire",
            u"Ecoutez un peu de musique classique et cela vous permettra de vous détendre et de trouver le sommeil",
            u"Une bonne nuit de sommeil joue un grand rôle pour ton bien-être physique et psychologique"
        ]
    },
    "lowactivity": {
        "title": u"Santé",
        "messages": [
            u"Faire de l'exercice améliore l'humeur",
            u"Faire de l'exercice réduit le stress, la dépression et l'anxiété",
            u"Pourquoi ne pas aller faire un tour ?",
            u"Pourquoi ne pas rendre visite à un ami ?",
            u"Pourquoi ne pas rendre visite à la famille ?",
            u"Pourquoi ne pas rejoindre un groupe de seniors ?",
            u"Pourquoi ne pas se rendre à un cours pour adulte ?",
            u"Pourquoi ne pas devenir bénévole ?",
            u"Essayez de prendre l'air et le soleil au moins deux heures par jour",
            u"Consultez les groupes d'intérêt sur SONOPA",
#            u"Peut-être que cet événement pourrait vous intéresser ?",
            u"Pourquoi ne pas lancer un appel vidéo avec un ami ou membre de votre famille ?",
            u"Pourquoi ne pas inviter des amis ou des membres de votre famille chez vous ?",
            u"Pourquoi ne pas jouer à un jeu sur SONOPA ?"
        ]
    },
    "personenters": {
        "title": u"Activité",
        "messages": [
            u"Bienvenue !",
            u"Pourquoi ne pas préparer un petit encas sain ? ",
            u"Prenez un verre d'eau/un thé/un café",
            u"Vérifier si un ami ne serait pas connecté sur SONOPA",
            u"Vérifier les groupes d'intérêt sur SONOPA",
#            u"Vous avez 2 nouveaux messages de X",
#            u"Aujourd'hui il y a un bon film à la télévision à 19h",
#            u"Vous avez 4 nouvelles notifications de la part des membres de SONOPA"
        ]
    },
    "personleaves": {
        "title": u"Activité",
        "messages": [
            u"Au revoir !",
            u"Avez-vous pensé à tout ce qu'il vous fallait ?",
            u"Pourquoi ne pas rendre visite plus tard à un ami ?",
            u"Pourquoi ne pas rendre visite plus tard à votre famille ?",
            u"N'oubliez pas d'acheter vos médicaments/des fruits/du pain… d'aller au supermarché/à l'épicerie ou de faire des courses sur le chemin du retour !",
#            u"N'oubliez pas votre rendez-vous à... / d'appeler X",
            u"Avez-vous oublié quelque chose ?"
        ]
    }
}



def get_message(condition, lang):
    title = MESSAGES[lang][condition]['title']
    msg = random.choice(MESSAGES[lang][condition]['messages'])
    return (title, msg)
