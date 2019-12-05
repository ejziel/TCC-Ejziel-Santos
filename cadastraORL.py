from os.path import dirname, abspath
from os.path import join
from warnings import warn

import sqlite3
import cv2
import dlib
import numpy as np
import math
from SelecionaImagem import SelectImage
from tkinter import *


conn = sqlite3.connect('usersORL.db')
cursor = conn.cursor()


def readOrl(pessoa, imagem):
    dir = join(dirname(dirname(abspath(__file__))), 'datasets', 'ORL_faces', 's')
    im = cv2.imread(join(dir + str(pessoa), str(imagem) + ".pgm"),-1)

    return im

def insertPeople(nome, cursor):
    cursor.execute("""INSERT INTO pessoa (nome) VALUES (?)""", (nome,))
    cursor.execute("""SELECT last_insert_rowid() from pessoa""")
    id = cursor.fetchone()[0]
    print('Pessoa inserida com sucesso.')
    return id

# inserindo dados na tabelas
def insertDistance(id_distance, distance_gravity, id_pessoa, cursor):
    params = (id_distance, distance_gravity, id_pessoa)
    cursor.execute("""INSERT INTO distances VALUES (?, ?, ?)""", params)
    

def readPoints(cursor):
    # lendo os pontos que serão utilizados no calculo das distâncias
    cursor.execute("""
    SELECT point0, point1 FROM feature_points;
    """)
    points = cursor.fetchall()
    
    return points

def getDistance(xlist, ylist, p1, p2):

    A = np.asarray((ylist[p1],xlist[p1]))
    B = np.asarray((ylist[p2],xlist[p2]))
    dis = np.linalg.norm(B-A)

    return dis

def plotPoints(image, xlista, ylista, points):

    for i in range(0,68):
        cv2.circle(image, (int(xlista[i]), int(ylista[i])), 1, (0,255,255), thickness=4)
    for linha in points:
        cv2.line(image, (int(xlista[linha[0]]), int(ylista[linha[0]])), (int(xlista[linha[1]]), int(ylista[linha[1]])), (255,255,255)) 
    cv2.imshow("Landmarks", image) #Display the frame
    cv2.waitKey(0)

cascade = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
cascadeEye = cv2.CascadeClassifier("haarcascade_eye.xml")
width, height = 300, 350

for subject in range (10):

    image = readOrl(subject+1,1)

    #Encontra as faces nos frames
    faces = cascade.detectMultiScale(image, 1.1, 5, minSize=(20,20))

    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h+40),(255,0,0),2)
        region = image[y:y + h, x:x + w]
        detectedEyes = cascadeEye.detectMultiScale(region)

        for (ox,oy,ow,oh) in detectedEyes:
            faceImage = cv2.resize(image[y:y + h + 50, x:x +w], (width, height))

    #Informações da pessoa

    id_pessoa = insertPeople("User " + str(subject+1), cursor)

    #Buscando landmarks

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

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


    #lendo pontos
    points = readPoints(cursor)
    id_distance = 1

    #Calculando distância para cada ponto
    for linha in points:
        a = int(linha[0])
        b = int(linha[1])

        distancia = getDistance(xlist, ylist, a, b)

        insertDistance(id_distance, distancia, id_pessoa, cursor)
        id_distance += 1

    print('Distancias inseridas com sucesso.')

    #plotPoints(faceImage,xlist,ylist,points) #Mostra imagem cadastrada

    conn.commit()

conn.close()



