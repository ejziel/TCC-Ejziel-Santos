from os.path import join
from os.path import dirname, abspath

import sqlite3
import cv2
import dlib
import numpy as np
import math
import pandas as pd

conn = sqlite3.connect('usersORL.db')
cursor = conn.cursor()

def readOrl(pessoa, imagem):
    dir = join(dirname(dirname(abspath(__file__))), 'datasets', 'ORL_faces', 's')
    im = cv2.imread(join(dir + str(pessoa), str(imagem) + ".pgm"),-1)

    return im

def getNameFromID(id_p, cursor): # Pega o nome do usuário a partir do seu ID
    cursor.execute("""
    SELECT nome FROM pessoa
    WHERE id = ?
    """, (id_p,))

    return str(cursor.fetchone()[0])

def readPoints(cursor): # lendo os pontos que serão utilizados no calculo das distâncias
    cursor.execute("""
    SELECT point0, point1 FROM feature_points;
    """)
    points = cursor.fetchall()
    
    return points

def getMaxId(cursor):# Função que pega a quantidade de usuários cadastrados

    cursor.execute("""
    SELECT MAX(id_pessoa) FROM distances;
    """)
    number = cursor.fetchone()
    
    return int(number[0]);

def readDistances(cursor): #Função que pega as distâncias armazenadas no BD

    cursor.execute("""
    SELECT dis.id_distance, dis.id_pessoa, dis.distance_gravity
    FROM distances dis
    WHERE dis.id_pessoa = dis.id_pessoa;
    """) 

    return cursor.fetchall()

def getDistance(xlist, ylist, p1, p2):

    A = np.asarray((ylist[p1],xlist[p1]))
    B = np.asarray((ylist[p2],xlist[p2]))
    dis = np.linalg.norm(B-A)

    return dis

cascade = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
cascadeEye = cv2.CascadeClassifier("haarcascade_eye.xml")
width, height = 300, 350
total = [0,0]

for subject in range (1,11): #Pessoa 1 até 10
#for subject in range (11,16): #Pessoa 11 até 15
    list = [0,0] #[correto, incorreto] 

    for sample in range (2,10): #Imagem 3 até 10 de cada pessoa

        image = readOrl(subject, sample+1)
        #cv2.imshow('ata',image)
        #cv2.waitKey(3)
        #Encontra as faces nos frames
        faces = cascade.detectMultiScale(image, 1.1, 5, minSize=(20,20))

        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h+40),(255,0,0),2)
            region = image[y:y + h, x:x + w]
            detectedEyes = cascadeEye.detectMultiScale(region)

            for (ox,oy,ow,oh) in detectedEyes:
                faceImage = cv2.resize(image[y:y + h + 50, x:x +w], (width, height))

        #Buscando landmarks

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("\shape_predictor_68_face_landmarks.dat")

        #Equalização de histograma
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        clahe_image = clahe.apply(faceImage)
        detections = detector(clahe_image, 1)

        for k,d in enumerate(detections): #For all detected face instances individually
            shape = predictor(clahe_image, d) #Draw Facial Landmarks with the predictor class
            xlist = []
            ylist = []

            for i in range(0,68): #Store X and Y coordinates in two lists
                xlist.append(float(shape.part(i).x))
                ylist.append(float(shape.part(i).y))

            meannp = np.asarray((np.mean(ylist),np.mean(xlist))) #Find both coordinates of centre of gravity
            
        if len(detections) < 1:
            print("Face não detectada!")

        points = readPoints(cursor)
        id_distance = 1

        distancia = []
        #Calculando distância para cada ponto
        for linha in points:
            a = int(linha[0])
            b = int(linha[1])

            distancia.append(getDistance(xlist, ylist, a, b))

            id_distance += 1

        distanciasBD = readDistances(cursor)

        hash = {}

        for line in distanciasBD:
            if(line[1] not in hash):
                hash[line[1]] = {}
            if(line[0] not in hash[line[1]]):
                hash[line[1]][line[0]] = (line[2] / distancia[line[0] - 1])

        tresh = 0.05
        max = getMaxId(cursor) #Maior Id cadastrado

        perc = []
        v = []
        v_i = []

        for i in range(1, max+1):
            count = 0
            
            for j in range(2,38):
                if(abs(hash[i][j] - hash[i][1]) <= tresh): #Testa se a primeira proporção é igual as demais, em função do tresh
                    count += 1
            
            v_i.append(i)
            v.append(count)
    
        z = pd.DataFrame(v)
        m = z.max()
        index = v.index(m[0])
        
        perc.append([v_i[index],m[0]])

        print(perc)

        for line in perc:
            percentual = (line[1]*100 / 36)
            if (percentual >= 50):
                print(getNameFromID(line[0],cursor) +" com " +  str(percentual) + "% de chance")
                #list[1] += 1 #teste para usuário não cadastrado
            else:
                #list[0] += 1 #teste para usuário não cadastrado
                print("Usuário Desconhecido")
            
            if(subject == line[0] and percentual >= 50):
                list[0] += 1
            else:
                list[1] += 1

        
                        
        #print(getNameFromID(index+1,cursor) +" com " +  str(percentual) + "% de chance")
    print("Certo e Errado User "+ str(subject)+"\n")
    print(list)
    total[0] += list[0]
    total[1] += list[1] 
print("Total Certo e Errado \n")
print(total)


                
conn.close()

