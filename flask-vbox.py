#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# Librerias requeridas para correr aplicaciones basadas en Flask
from flask import Flask, jsonify, make_response,request, abort, make_response
from subprocess import PIPE, Popen, call, check_output

app = Flask(__name__)

# Web service que se invoca al momento de ejecutar el comando
# curl http://localhost:5000
@app.route('/',methods = ['GET'])
def index():
	return "Hola Javeriana"

# Este metodo retorna la lista de sistemas operativos soportados por VirtualBox
# Los tipos de sistemas operativos soportados deben ser mostrados al ejecutar 
# el comando
# curl http://localhost:5000/vms/ostypes
# Este es el codigo del item 1
@app.route('/vms/ostypes',methods = ['GET'])
def ostypes():
	
	# Tu codigo aqui
        command_line = 'VBoxManage ​list ostypes'
        
        proceso = Popen(['VBoxManage', 'list' , 'ostypes'], stdout=PIPE, stderr=PIPE)
        error_econtrado = proceso.stderr.read()
        proceso.stderr.close() 
        listado = proceso.stdout.read()
        proceso.stdout.close()
	output =  listado 
        return output

# Este metodo retorna la lista de maquinas asociadas con un usuario al ejecutar
# el comando
# curl http://localhost:5000/vms
# Este es el codigo del item 2a
@app.route('/vms',methods = ['GET'])
def listvms():
        proceso = Popen(['VBoxManage', 'list' , 'vms'], stdout=PIPE, stderr=PIPE)
        error_econtrado = proceso.stderr.read()
        proceso.stderr.close()
        listado = proceso.stdout.read()
        proceso.stdout.close()
        output =  listado
        return output

# Este metodo retorna aquellas maquinas que se encuentran en ejecucion al 
# ejecutar el comando
# curl http://localhost:5000/vms/running
# Este es el codigo del item 2b
@app.route('/vms/running',methods = ['GET'])
def runninglistvms():
	# Tu codigo aqui VBoxManage ​list runningvms 
        proceso = Popen(['VBoxManage', 'list' , 'runningvms'], stdout=PIPE, stderr=PIPE)
        error_econtrado = proceso.stderr.read()
        proceso.stderr.close()
        listado = proceso.stdout.read()
        proceso.stdout.close()
        output =  listado
        return output
# Este metodo retorna las caracteristica de una maquina virtual cuyo nombre es
# vmname 3.
@app.route('/vms/info/<vmname>', methods = ['GET'])
def vminfo(vmname):
	# Tu codigo aqui
	proceso1 = Popen(['VBoxManage','list','vms'],stdout=PIPE)
	grep = Popen(['grep','-w', vmname],stdin=proceso1.stdout,stdout=PIPE)
	info = Popen(['cut', '-d', ' ','-f', '1'],stdin=grep.stdout,stdout=PIPE)
	valor = check_output(['uniq'],stdin=info.stdout)
	error = "maquina no existe"
	if len(valor) == 0:
		output = jsonify({'Error': error})
	else:
        	proceso = Popen(['VBoxManage', 'showvminfo', vmname], stdout=PIPE)
        	grep = Popen(['grep', 'Name:'], stdin = proceso.stdout, stdout = PIPE)
        	name = check_output(['cut' , '-d', ' ', '-f', '13'], stdin = grep.stdout)
		proceso2 = Popen(['VBoxManage', 'showvminfo', vmname], stdout=PIPE)
        	grep = Popen(['grep', 'Memory size:'], stdin = proceso2.stdout, stdout = PIPE)
        	memoria = check_output(['cut' , '-d', ' ', '-f', '7'], stdin = grep.stdout)
		proceso3 = Popen(['VBoxManage', 'showvminfo', vmname], stdout=PIPE)
        	grep = Popen(['grep', 'Number of CPUs:'], stdin = proceso3.stdout, stdout = PIPE)
        	CPUs = check_output(['cut' , '-d', ' ', '-f', '5'], stdin = grep.stdout)
		proceso4 = Popen(['VBoxManage', 'showvminfo', vmname], stdout=PIPE)
        	grep = Popen(['grep', 'Attachment:'], stdin = proceso4.stdout, stdout = PIPE)
        	red = check_output(['cut' , '-d', ':', '-f', '4'], stdin = grep.stdout)
        	output = jsonify({'Red': red, 'CPUs': CPUs, 'Ram': memoria, 'Nombre': name})
	return output
# Usted deberá realizar además los items 4 y 5 del enunciado del proyecto 
# considerando que:
# - El item 4 deberá usar el método POST del protocolo HTTP

@app.route('/vms/crear/<name>/<memoria>/<disco>/<cpus>', methods=['POST'])
def create_vm(name,memoria,disco,cpus):
  	proceso = Popen(['./crearmv.sh', name , memoria , disco, cpus], stdout=PIPE ,  stderr=PIPE)
        return jsonify({'Se creo la maquina': name})

# - El item 5 deberá usar el método DELETE del protocolo HTTP
@app.route('/vms/borrar/<string:name_vm>', methods=['DELETE'])
def delete_task(name_vm):
	proceso1 = Popen(['VBoxManage','list','vms'],stdout=PIPE)
        grep = Popen(['grep','-w', name_vm],stdin=proceso1.stdout,stdout=PIPE)
        info = Popen(['cut', '-d', ' ','-f', '1'],stdin=grep.stdout,stdout=PIPE)
        valor = check_output(['uniq'],stdin=info.stdout)
        error = "maquina no existe"
	if len(valor)==0:
		output = jsonify({'error': error})
	else:
        	proceso = Popen(['VBoxManage', 'unregistervm' , name_vm ,'--delete'], stdout=PIPE ,  stderr=PIPE)
		output = jsonify({'Se borro la maquina': name_vm})
        return output
if __name__ == '__main__':
        app.run(debug = True, host='0.0.0.0')

