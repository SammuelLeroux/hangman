import sys
from numpy import random
from datetime import datetime

mots_txt = sys.argv[1]

def hangman_game(fichier_txt):

    # recuperer la liste de mot du fichier mots.txt
    file_mot= open(fichier_txt, "r")
    liste_mot = file_mot.readlines()
    file_mot.close()

    nb_partie_perdue = 3
    nb_partie_gagnee = 0
    winstreak = 0

    # lvl 1 -> mot de 3 a 4 lettres => trouver 3 mots
    lvl = 1

    # on def les points
    # -> +10 par bonne reponse, si winstreak points = 10 + winstreak
    # -> -10 si mauvaise reponse => point = -10 et winstreak = 0
    points = 0

    # on stocke les mots choisis pour eviter d'avoir 2 fois le meme mot dans un BO3
    liste_mots_choisis = []

    while (nb_partie_perdue > 0):

        if (nb_partie_gagnee == 3):
            # lvl 2 -> mot de 3 a 5 lettres => trouver 4 mots
            lvl += 1
        elif (nb_partie_gagnee == 7):
            # lvl 3 -> mot de 3 a 6 lettres => trouver 5 mots
            lvl += 1
        elif (nb_partie_gagnee == 10):
            # lvl 4 -> tous les mots => mode survie
            lvl += 1

        # choix d'un mot au hazard dans cette liste de mot
        mot_choisi = liste_mot[random.randint(0, len(liste_mot) - 1)].strip()

        # taille du mot en fonction du lvl
        if (lvl == 1):
            while (len(mot_choisi) > 4):
                mot_choisi = liste_mot[random.randint(0, len(liste_mot) - 1)].strip()
        elif (lvl == 2):
            while (len(mot_choisi) > 5):
                mot_choisi = liste_mot[random.randint(0, len(liste_mot) - 1)].strip()
        elif (lvl == 3):
            while (len(mot_choisi) > 6):
                mot_choisi = liste_mot[random.randint(0, len(liste_mot) - 1)].strip()

        if (mot_choisi in liste_mots_choisis):
            while (mot_choisi in liste_mots_choisis):
                mot_choisi = liste_mot[random.randint(0, len(liste_mot) - 1)].strip()
        else:
            liste_mots_choisis.append(mot_choisi)
        
        # nb de chance pour trouver un mot
        nb_chance = 5
        if (len(mot_choisi) > 5):
            if (len(mot_choisi) - lvl > 5):
                nb_chance = random.randint(5, len(mot_choisi) - lvl)
            elif (len(mot_choisi) - lvl == 5):
                nb_chance = 5
            else:
                nb_chance = random.randint(len(mot_choisi) - lvl, 5)

        # on affiche des underscore de la taille du mot
        underscore_mot_choisi = ''
        for i in range(len(mot_choisi)):
            underscore_mot_choisi += '_ '

        if (len(liste_mots_choisis) > 1):
            print('\n======================================== MOT SUIVANT ==============================================')
        
        #print(mot_choisi)
        #print(liste_mots_choisis)

        # on affiche le lvl
        print('\nNiveau :', lvl)

        # on affiche le nombre de points
        print('Score =', points)

        # on affiche le nombre de partie gagnee
        print('win streak =', winstreak, '\n')

        # on affiche le nombre de mots trouves
        if (nb_partie_gagnee == 0):
            print(nb_partie_gagnee, 'mot trouve\n')
        else:
            print(nb_partie_gagnee, 'mots trouves\n')

        print('Vous avez le droit a', nb_chance, 'mauvaises reponses')
        print(underscore_mot_choisi, '\n')

        reponse = []
        mauvaises_lettres = []
        points_perdus = 0

        while (points_perdus < nb_chance):
            # on demande a l'utilisateur de choisir une lettre
            lettre_user = (input('Choisi une lettre : ')).lower()

            flag_points_perdus = False
            flag_mauvaise_lettre = False
            if (len(lettre_user) > 1):
                # l'utilisateur a entre un mot en entier

                # l'utilisateur veut quitter la partie
                if (lettre_user == 'fin de partie'):
                    nb_partie_perdue = 0
                    print('\nFin de partie')
                    break

                if (lettre_user == mot_choisi):
                    nb_partie_gagnee += 1
                    if points < 0:
                        points += 10
                    else:
                        points += 10 + winstreak * 2
                    winstreak += 1
                    print('\nBravo, vous avez trouvé le bon mot')
                    break
                else:
                    flag_points_perdus = True
            else:
                # l'utilisateur a entre une lettre

                # la lettre n'a pas encore ete trouvee
                if (lettre_user not in reponse):
                    # la lettre est dans le mot_choisi
                    if (lettre_user not in mot_choisi):
                        # la lettre est mise dans la liste des mauvaises_lettres
                        flag_mauvaise_lettre = True
                        # perte de point
                        flag_points_perdus = True
                else:
                    # l'utilisateur a rentre une lettre qu'il avait deja utilise => perte de point

                    # la lettre est mise dans la liste des mauvaises_lettres
                    flag_mauvaise_lettre = True
                    # perte de point
                    flag_points_perdus = True
                
                if (flag_mauvaise_lettre):
                    mauvaises_lettres.append(lettre_user)
                else:
                    reponse.append(lettre_user)

            if (flag_points_perdus):
                points_perdus += 1

            if (points_perdus == nb_chance):
                print('Perdu')
                print('Le mot a trouver était :', mot_choisi, '\n')
                nb_partie_perdue -= 1
                points -= 10
                winstreak = 0
                break
            else:
                # on affiche la reponse
                reponse_affichee = ['_'] * len(mot_choisi)
                if (len(reponse) > 0):
                    for i in range(len(reponse)):
                        for j in range(len(mot_choisi)):
                            if (reponse[i] == mot_choisi[j]):
                                reponse_affichee[j] = mot_choisi[j]

                if (''.join(reponse_affichee) == mot_choisi):
                    nb_partie_gagnee += 1
                    if (points < 0):
                        points += 10
                    else:
                        points += 10 + winstreak * 2
                    winstreak += 1
                    print('Bravo, vous avez trouvé le bon mot')
                    break
                else:
                    # on affiche les points perdus
                    #print('points perdus = ', points_perdus)

                    # on affiche les mauvaises_lettres
                    print('Les mauvaises lettres que vous avez utilisées sont : ', ' '.join(mauvaises_lettres))
                    
                    # on affiche le bout de mot trouvé pour le moment
                    print('Vous avez trouvé :', ' '.join(reponse_affichee), '\n')

        if (nb_partie_perdue == 0):
            print('GAME OVER\n')
            break
        else:
            print('Il vous reste', nb_partie_perdue, 'partie avant de perdre definitivement')        

    # on boucle sur les records
    file_records = open("records.txt", "r")
    records = file_records.readlines()
    file_records.close()

    if (points > 0):

        # l'utilisateur a trouve au moins 1 mot => on cherche si il a battu un record

        # on trouve le max des records , normalement c'est la derniere ligne mais on ne sait jamais
        if (len(records) <= 0):
            # il n'y a pas encore eu de record
            current_record = 0
        else:
            # on a au moins 1 record
            current_record = 0
            for i in records:
                if (int(i.split(' - ')[1]) > current_record):
                    current_record = int(i.split(' - ')[1])
        
        # si il a battu le record
        if (points > current_record):
            print("Vous venez d'établir un nouveau record, bravo !!!\n")
            pseudo = input("Comment vous nomme-t-on ? ")
            if (' - ' in pseudo):
                pseudo = pseudo.replace(' - ', ' ')
            if (' -' in pseudo):
                pseudo = pseudo.replace(' -', ' ')
            if ('- ' in pseudo):
                pseudo = pseudo.replace('- ', ' ')
            # if ('-' in pseudo):
            #   pseudo = pseudo.replace('-', ' ')

            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            current_date = now.strftime("%d/%m/%Y %H:%M:%S")

            with open("records.txt", "w") as file_records:
                if (len(records) > 0):
                    for line in records:
                        file_records.write(line)

                file_records.write(pseudo + ' - ' + str(points) + ' - ' + current_date + '\n')

hangman_game(mots_txt)
