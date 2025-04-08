from django.shortcuts import render
from .models import Usuario, Login, ESenha,  RGraficos
import pymongo
#from typing import Any
from django.db.models.query import QuerySet
#from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.http import HttpResponse
#from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
#from django.urls import reverse
#from django.template import loader
#from django.views import generic
#from django.core.mail import send_mail
#from django.shortcuts import redirect
from django.conf import settings
#import uuid
#import os
#import pandas as pd
#from plotly.offline import plot
import plotly.graph_objects as go
#import plotly.io as pio
#import plotly.express as px
import matplotlib.pyplot as plt
from io import BytesIO
import base64
#from plotly.io import to_image
import paho.mqtt.client as mqtt
import json
import threading
import datetime
#from django.shortcuts import render, redirect

from django.conf import settings 
#from django.template.loader import get_template  
from django.core.mail import EmailMessage 

def mqtt_receive():
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("EstacaoMetIFPE")

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        data = json.loads(msg.payload)
        temperature = data['Temperatura']
        humidity = data['Umidade']
        pressao = data['Pressao']
        vento = data['Vento']
        volt = data['Volt']
        luz = data['Luz']
        rpm = data['Rpm']
        gas = data['Gas']
        ar = data['Ar']
        print("Temperature:", temperature)
        print("Humidity:", humidity)
        print("Pressão:", pressao)
        print("Vento:", vento)
        print("Volt:", volt)
        print("Luz:", luz)
        print("Rpm:", rpm)
        print("Gas:", gas)
        print("Ar:", ar)
       
        myclient = pymongo.MongoClient("mongodb+srv://phpvn:sacul0499@cluster0.u9irlhy.mongodb.net/")
        mydb = myclient["Dados"]
        mycol = mydb["DadosEstacao"]
        thedate = str(datetime.date.today().day)+'/'+str(datetime.date.today().month)+'/'+str(datetime.date.today().year)
        thetime = str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute)+':'+str(datetime.datetime.now().second)
        mydict = { "Temperatura": temperature,"Umidade": humidity, "Pressão": pressao, "Vento": vento,
                   "Volt":volt,"Luz":luz,"Rpm":rpm,"Gás":gas,"Ar":ar,"Data":thedate,"Hora":thetime}

        x = mycol.insert_one(mydict)
        client = mqtt.Client()
        client.connect("test.mosquitto.org", 1883)

    # Suponha que você tenha dados a serem enviados em um formato similar
        dados = {
            'Temperatura': temperature,
            'Umidade': humidity,
            'Pressao': pressao,
            'Luz': luz,
            'Gas': gas,
            'Rpm': rpm,
            'Vento': vento,
            'Ar': ar,
        }

        client.publish("EstacaoMetIFPED", json.dumps(dados))
        client.disconnect()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect("test.mosquitto.org", 1883)
    client.loop_forever()


mqtt_thread = threading.Thread(target=mqtt_receive)
mqtt_thread.daemon = True  # A thread será encerrada quando o programa principal terminar
mqtt_thread.start()

def cria_grafico(x, y, cor):
    plt.figure(figsize=(5,3))
    plt.plot(x, y, color=cor)
    plt.ylim((min(y)-2, max(y)+2))
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return img

def cria_gauge(data, min, max, cor_inicio, cor_meio, cor_fim, unidade):
    go_temp = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = data[-1],
        number = {'suffix': unidade, 'font': {'size': 64, 'color': '#444', 'family': 'sans-serif'}},
        gauge = {
            'axis':{'range': [min, max], 'tickwidth': 1, 'tickcolor': '#000'},
            'bar': {'color': '#444'},
            'borderwidth' : 2,
            'bordercolor': 'black',
            'steps': [
                {'range': [min,min + (max-min)/3], 'color': cor_inicio},
                {'range': [min + (max-min)/3,min + 2*(max-min)/3], 'color': cor_meio},
                {'range': [min + 2*(max-min)/3,max], 'color': cor_fim}
            ]

        }
    ))

    go_temp.update_layout(font=dict(size=36))

    img = go_temp.to_image(format='png')
    img_b64 = "data:image/png;base64," + base64.b64encode(img).decode()
    return img_b64

def home(request):
    
    return render(request,'usuarios/home.html')
# Create your views here.

def usuarios(request):
    # Salvar os dados da tela para o banco de dados.
    

    myclient = pymongo.MongoClient("mongodb+srv://phpvn:sacul0499@cluster0.u9irlhy.mongodb.net/")
    mydb = myclient["Dados"]
    mycol = mydb["Usuarios"]
    verifica_usuario = Usuario()
    verifica_usuario.email = request.POST.get('meuemail')
    verifica_usuario.cpf = request.POST.get('meucpf')
    verifica_usuario.celular = request.POST.get('meucel')
    CelularInvalido = False
    CpfInvalido = False
    EmailInvalido = False
    email = mycol.find_one({ "Email":  verifica_usuario.email})
    cpf = mycol.find_one({ "Cpf": verifica_usuario.cpf})
    celular = mycol.find_one({ "Celular": verifica_usuario.celular})
    # Exibir todos os usuários já cadastrados em uma nova página
    
    # Retornar os dados para a página de listagem de usuários
    print(celular)
    print(email)
    print(cpf)
    
    if email != None and cpf != None and celular != None:
        CelularInvalido = True
        CpfInvalido = True
        EmailInvalido = True
        usuarioss ={
         'usuarios': Usuario.objects.all(),
         'CelularInvalido': True,
        'CpfInvalido': True,
        'EmailInvalido': True
        }
    elif cpf != None and celular != None:
        CelularInvalido = True
        CpfInvalido = True
        EmailInvalido = False
        usuarioss ={
         'usuarios': Usuario.objects.all(),
         'CelularInvalido': True,
        'CpfInvalido': True,
        'EmailInvalido': False
        }
    elif email != None and cpf != None:
        CelularInvalido = False
        CpfInvalido = True
        EmailInvalido = True
        usuarioss ={
         'usuarios': Usuario.objects.all(),
         'CelularInvalido': False,
        'CpfInvalido': True,
        'EmailInvalido': True
        }
    elif email != None and  celular != None:
        CelularInvalido = True
        CpfInvalido = False
        EmailInvalido = True
        usuarioss ={
         'usuarios': Usuario.objects.all(),
         'CelularInvalido': True,
        'CpfInvalido': False,
        'EmailInvalido': True
        }
    elif email != None:
        CelularInvalido = False
        CpfInvalido = False
        EmailInvalido = True
        usuarioss ={
         'usuarios': Usuario.objects.all(),
         'CelularInvalido': False,
        'CpfInvalido': False,
        'EmailInvalido': True
        }
    elif cpf != None:
        CelularInvalido = False
        CpfInvalido = True
        EmailInvalido = False
        usuarioss ={
         'usuarios': Usuario.objects.all(),
         'CelularInvalido': False,
        'CpfInvalido': True,
        'EmailInvalido': False
        }
    elif celular != None:
        CelularInvalido = True
        CpfInvalido = False
        EmailInvalido = False
        usuarioss ={
         'usuarios': Usuario.objects.all(),
         'CelularInvalido': True,
         'CpfInvalido': False,
         'EmailInvalido': False
        }
    else:
         usuarioss ={
         'usuarios': Usuario.objects.all(),
         
        }
    print(CelularInvalido)
    print(EmailInvalido)
    print(CpfInvalido)
    global onome
    global osobrenome
    global adata
    global oemail
    global oddi
    global ocelular
    global osexo
    global ocpf
    global asenha
    if email == None and cpf == None and celular == None:
        novo_usuario = Usuario()
        novo_usuario.nome = request.POST.get('meunome')
        novo_usuario.sobrenome = request.POST.get('meusobrenome')
        novo_usuario.idade = request.POST.get('minhadata')
        novo_usuario.email = request.POST.get('meuemail')
        novo_usuario.ddi = request.POST.get('meuddi')
        novo_usuario.celular = request.POST.get('meucel')
        novo_usuario.sexo = request.POST.get('meusexo')
        novo_usuario.cpf = request.POST.get('meucpf')
        novo_usuario.senha = request.POST.get('minhasenha')
        
        onome = novo_usuario.nome
        osobrenome = novo_usuario.sobrenome
        adata = novo_usuario.idade
        oemail = novo_usuario.email
        oddi = novo_usuario.ddi
        ocelular = novo_usuario.celular
        osexo = novo_usuario.sexo
        ocpf = novo_usuario.cpf 
        asenha = novo_usuario.senha
        assunto = 'Confirmação de E-mail'
        #mensagem = f'Por favor, clique no link abaixo para confirmar seu cadastro: http://localhost:8000/ce'
        mensagem = f'Por favor, clique no link abaixo para confirmar seu cadastro:  https://8114-2804-14d-5482-97c1-91aa-3c33-2cea-8ece.ngrok-free.app/ce'
        remetente = settings.EMAIL_HOST_USER
        destinatarios = [novo_usuario.email]
            
        try:
                email = EmailMessage(assunto, mensagem, remetente, destinatarios)
                
                email.send()
                return render(request, 'usuarios/confirmacao_enviada.html')
        except Exception as e:
                return HttpResponse(f"Erro ao enviar e-mail: {e}")
        #novo_usuario.save()
        #x = mycol.insert_one(mydict)
        
        #return render(request,'usuarios/usuarios.html',usuarioss)
    else:
       
        return render(request,'usuarios/ErroDeCadastro.html',usuarioss)
def confirmar(request):
    novo_usuario = Usuario()
    novo_usuario.nome = request.POST.get('meunome')
    novo_usuario.sobrenome = request.POST.get('meusobrenome')
    novo_usuario.idade = request.POST.get('minhadata')
    novo_usuario.email = request.POST.get('meuemail')
    novo_usuario.ddi = request.POST.get('meuddi')
    novo_usuario.celular = request.POST.get('meucel')
    novo_usuario.sexo = request.POST.get('meusexo')
    novo_usuario.cpf = request.POST.get('meucpf')
    novo_usuario.senha = request.POST.get('minhasenha')
    myclient = pymongo.MongoClient("mongodb+srv://phpvn:sacul0499@cluster0.u9irlhy.mongodb.net/")
    mydb = myclient["Dados"]
    mycol = mydb["Usuarios"]
    
    
    usuarioss ={
         'usuarios': Usuario.objects.all(),
         
    }    
    theemail = mycol.find_one({ "Email":  oemail})
    if theemail == None:
        mydict = { "nome": onome,"sobrenome": osobrenome, "DataDeNascimento": adata, "Email": oemail, "DDI": oddi,
               "Celular":  ocelular, "Sexo": osexo,"Cpf": ocpf, "Senha": asenha}
        x = mycol.insert_one(mydict)
        return render(request,'usuarios/usuarios.html',usuarioss)
    else:
        return render(request,'usuarios/CadastroJaConfirmado.html',usuarioss)

def login(request):
    myclient = pymongo.MongoClient("mongodb+srv://phpvn:sacul0499@cluster0.u9irlhy.mongodb.net/")
    mydb = myclient["Dados"]
    mycol = mydb["Usuarios"]
    
    login_user = Login()
    login_user.emaill = request.GET.get('emaillogin')
    login_user.senhal = request.GET.get('senhalogin')
    x = mycol.find_one({ "Email": login_user.emaill, "Senha": login_user.senhal})
    #y = mycol.find_one({ "Senha": login_user.senhal})
    #print(x)
    # Exibir todos os usuários já cadastrados em uma nova página
    global mEmail
    global mSenha
    myclientt = pymongo.MongoClient("mongodb+srv://phpvn:sacul0499@cluster0.u9irlhy.mongodb.net/")
    mydbt = myclientt["Dados"]
    mycolt = mydbt["DadosEstacao"]
    allData = []
    allIndex = 0
    saveIndex = []
    for y in mycolt.distinct("Data"):
        print(str(y))
        allIndex += 1
        print(allIndex)
        allData.append(str(y))
        saveIndex.append(allIndex)
        usuarios ={
            'usuarios': Usuario.objects.all(),
            'Data' : allData,  
            'Index': saveIndex,
        }
    # Retornar os dados para a página de listagem de usuários
    if x == None:
        
        SenhaInvalida = True
        EmailInvalido = True
        usuarioss ={
         'usuarios': Usuario.objects.all(),
         'SenhaInvalida': True,
         'EmailInvalido': True
        }
        return render(request,'usuarios/loginNaoConfirmado.html',usuarioss)
    else:
        
        mEmail = login_user.emaill
        mSenha = login_user.senhal
        return render(request,'usuarios/loginConfirmado.html',usuarios)
    
    
def retornaGraficos(request):
    myclient = pymongo.MongoClient("mongodb+srv://phpvn:sacul0499@cluster0.u9irlhy.mongodb.net/")
    mydb = myclient["Dados"]
    mycol = mydb["DadosEstacao"]
    login_user = RGraficos()
    login_user.datae = request.GET.get('datadados')
   
    print(login_user.datae)
 
    datacompleta = ''
    datacompleta = login_user.datae
    print(login_user.datae)
  
    i = 0
    leitura = []
    
    t, u, gas, q_ar, luz, rpm, v_vento, p = [], [], [], [], [], [], [], []
    y = mycol.find_one({"Data": datacompleta})
    tmax = []
    tmin = []
    hmax = []
    hmin = []
    pmax = []
    pmin = []
    vmax = []
    vmin = []
    lmax = []
    lmin = []
    rmax = []
    rmin = []
    gmax = []
    gmin = []
    qmax = []
    qmin = []
    tm = 0.0
    hm = 0.0
    pm = 0.0
    vm = 0.0
    lm = 0.0
    rm = 0.0
    gm = 0.0
    qm = 0.0
    for x in mycol.find({"Data": datacompleta}):
        
        
        i+=1
        """""""""
        if x.get("Hora")[0] == 0 or x.get("Hora")[0] == 3 or x.get("Hora")[0] == 4 or x.get("Hora")[0] == 5 or x.get("Hora")[0] == 7 or x.get("Hora")[0] == 8 or x.get("Hora")[0] == 9:
            horaCerta = x.get("Hora")[0]
        else:
            horaCerta = x.get("Hora")[0]+x.get("Hora")[1]
         leitura.append(horaCerta)
        """""""""
        leitura.append(i)
        tm += float(x.get("Temperatura"))
        hm += float(x.get("Umidade"))
        pm += float(x.get("Pressão"))
        vm += float(x.get("Vento"))
        lm += float(x.get("Luz"))
        rm += float(x.get("Rpm"))
        gm += float(x.get("Gás"))
        qm += float(x.get("Ar"))

        tmax.append(x.get("Temperatura"))
        tmin.append(x.get("Temperatura"))
        hmax.append(x.get("Umidade"))
        hmin.append(x.get("Umidade"))
        pmax.append(x.get("Pressão"))
        pmin.append(x.get("Pressão"))
        vmax.append(x.get("Vento"))
        vmin.append(x.get("Vento"))
        lmax.append(x.get("Luz"))
        lmin.append(x.get("Luz"))
        rmax.append(x.get("Rpm"))
        rmin.append(x.get("Rpm"))
        gmax.append(x.get("Gás"))
        gmin.append(x.get("Gás"))
        qmax.append(x.get("Ar"))
        qmin.append(x.get("Ar"))

        t.append(float(x.get("Temperatura")))
        u.append(float(x.get("Umidade")))
        p.append(float(x.get("Pressão")))
        v_vento.append(float(x.get("Vento")))
        luz.append(float(x.get("Luz")))
        rpm.append(float(x.get("Rpm")))
        gas.append(float(x.get("Gás")))
        q_ar.append(float(x.get("Ar")))
        print(x)
    print("{:.2f}".format(float(tm/i)))
    print("{:.2f}".format(float(hm/i)))
    print("{:.2f}".format(float(pm/i)))
    print("{:.2f}".format(float(vm/i)))
    print("{:.2f}".format(float(lm/i)))
    print("{:.2f}".format(float(rm/i)))
    print("{:.2f}".format(float(gm/i)))
    print("{:.2f}".format(float(qm/i)))
    print(max(tmax))
    print(min(tmin))
    print(max(hmax))
    print(min(hmin))
    print(max(pmax))
    print(min(pmin))
    print(max(vmax))
    print(min(vmin))
    print(max(lmax))
    print(min(lmin))
    print(max(rmax))
    print(min(rmin))
    print(max(gmax))
    print(min(gmin))
    print(max(qmax))
    print(min(qmin))
    print(y)
    if y == None:
        usuarios ={
         'usuarios': Usuario.objects.all(),
         'DataInvalida': True,
         'DataValida': False,
         'email': mEmail,
         'senha': mSenha
        }
        return render(request,'usuarios/DataConfirmada.html',usuarios)
    else:    
           img_t = cria_grafico(leitura, t, 'red')
           img_u = cria_grafico(leitura, u, 'blue')
           img_gas = cria_grafico(leitura, gas, 'grey')
           img_ar = cria_grafico(leitura, q_ar, 'orange')
           img_luz = cria_grafico(leitura, luz, 'yellow')
           img_rpm = cria_grafico(leitura, rpm, 'black')
           img_vv = cria_grafico(leitura, v_vento, 'black')
           img_p = cria_grafico(leitura, p, 'purple')

           login_user = Login()

           context = {
              'temperatura': t[-1], 
               'umidade': u[-1], 
               'gas': gas[-1], 
               'qualidade_do_ar': q_ar[-1], 
               'valor_luz': luz[-1], 
               'rpm': rpm[-1],
               'velocidade_do_vento': v_vento[-1],
               'pressao': p[-1],
               'tempMed':"{:.2f}".format(float(tm/i)),
               'umidMed':"{:.2f}".format(float(hm/i)),
               'presMed':"{:.2f}".format(float(pm/i)),
               'velMed':"{:.2f}".format(float(vm/i)),
               'luzMed':"{:.2f}".format(float(lm/i)),
               'rpmMed':"{:.2f}".format(float(rm/i)),
               'gasMed':"{:.2f}".format(float(gm/i)),
               'arMed':"{:.2f}".format(float(qm/i)),
               'tempMax':"{:.2f}".format(max(tmax)),
               'tempMin':"{:.2f}".format(min(tmin)),
               'humMax':"{:.2f}".format(max(hmax)),
               'humMin':"{:.2f}".format(min(hmin)),
               'presMax':"{:.2f}".format(max(pmax)),
               'presMin':"{:.2f}".format(min(pmin)),
               'venMax':"{:.2f}".format(max(vmax)),
               'venMin':"{:.2f}".format(min(vmin)),
               'luzMax':"{:.2f}".format(max(lmax)),
               'luzMin':"{:.2f}".format(min(lmin)),
               'rpmMax':"{:.2f}".format(max(rmax)),
               'rpmMin':"{:.2f}".format(min(rmin)),
               'gasMax':"{:.2f}".format(max(gmax)),
               'gasMin':"{:.2f}".format(min(gmin)),
               'qarMax':"{:.2f}".format(max(qmax)),
               'qarMin':"{:.2f}".format(min(qmin)),
               'img_t': img_t,
               'img_u': img_u,
               'img_gas': img_gas,
               'img_ar': img_ar,
               'img_luz': img_luz,
               'img_rpm': img_rpm,
               'img_vv': img_vv,
               'img_p': img_p,
               'DataInvalida': False,
               'DataValida': True,
               'datacompleta': datacompleta,
               'email': mEmail,
               'senha': mSenha
        }
    return render(request,'usuarios/DataConfirmada.html',context)

def esqsenha(request):
    myclient = pymongo.MongoClient("mongodb+srv://phpvn:sacul0499@cluster0.u9irlhy.mongodb.net/")
    mydb = myclient["Dados"]
    mycol = mydb["Usuarios"]
    email_user = ESenha()
    email_user.emaill = request.POST.get('emailsenha')
    email_user.senhal = request.POST.get('senhaNova')
    x = mycol.find_one({ "Email": email_user.emaill})
    print(x)
    # Exibir todos os usuários já cadastrados em uma nova página
   
    myquery = { "Email": email_user.emaill }
    newvalues = { "$set": { "Senha": email_user.senhal } }
    mycol.update_one(myquery, newvalues)
    usuarios ={
         'usuarios': Usuario.objects.all()
    }
    if x == None:
        return render(request,'usuarios/ErroDeEmail.html',usuarios)
    else:    
        return render(request,'usuarios/EsqueciMinhaSenha.html',usuarios)