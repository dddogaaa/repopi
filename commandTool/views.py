from django.shortcuts import render
from subprocess import Popen
from datetime import datetime
from django.conf import settings as Settings
from .models import Result
from django.http import HttpResponse,JsonResponse
import json
import os
import pytz
import datetime
import threading


def get_data_folder():
    return os.path.join(Settings.DATA_FOLDER)

def create_data_folder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        
    except OSError as e:
        print(e)

def get_date_now():
    time_zone = pytz.timezone("Europe/Istanbul")
    time = datetime.datetime.now(time_zone)
    return time.strftime('%Y-%m-%d-%H-%M-%S')

def run(name,command):
    date_now = get_date_now()
    print(name+" basladi")
    outputs_folder = get_data_folder()
    create_data_folder(outputs_folder)
    output_file = os.path.join(outputs_folder, f"{date_now}-{name}.txt")
    print(output_file)

    item = {
        'file' : output_file,
        "command": command,
        "status": 2,
        "start_time": date_now,
        "end_time": None
    }

    result = Result.objects.create(**item)
    
    log = open(output_file, 'a')
    log.write(date_now+' '+name+'\n')
    log.flush()

    proc = Popen(command, stdout=log, stderr=log, shell=True)

    proc.wait()

    returnValue = proc.poll()

    if  returnValue == 0 :
        result.status = 1
        result.message = 'Command executed successfully'
        result.end_time = get_date_now()
        print('Command finished successfully.')
    else:
        result.message = 'Command encountered an error.' 
        result.status = 0
        result.end_time = get_date_now()
        print('Command finished with error.')

    result.save()

def runCommand(name,command):
        thread = threading.Thread(
        target=run, args=(name,command))

        thread.start()

        response = {
            'message' : 'Command execution operation started.'
        }

        json_response = json.dumps(response, indent=2)

        return HttpResponse(json_response, content_type="application/json")
    
def filter_commands(request):
    status = request.GET.get("status", "")
    command = request.GET.get('command','')

    filtered_data = Result.objects.all()

    if status:
        filtered_data = filtered_data.filter(status=status)
    if command:
        filtered_data = filtered_data.filter(name=command)

    commands = []
    for data in filtered_data:
        command_info = {
            "id": data.id,
            "status": data.status,
            # "command": data.command,
            "start_time": data.start_time,
            "end_time": data.end_time,
            "file": data.file
        }
        commands.append(command_info)

    response = {"filtered_commands": commands}

    response_data = json.dumps(response, indent=2)

    return HttpResponse(response_data, content_type="application/json")

def get_output_by_id(request, command_id):
    try:
        command = Result.objects.get(id=command_id)
        output = ""
        with open(command.file, "r") as file:
            output = file.read()

        # output = output.replace('\n', '/')

        response = {"id": command.id, "command": command.command, "output": output}

        json_response = json.dumps(response, indent=2)

        return HttpResponse(json_response, content_type="application/json")

    except Result.DoesNotExist:
        error_response = {"error": "Command ID not found."}

        json_response = json.dumps(error_response, indent=2)

        return HttpResponse(json_response, status=404, content_type="application/json")
    
def list_outputs(request): 
    if request.method == "GET":
        outputs_dir = get_data_folder()

        outputs = os.listdir(outputs_dir)
        outputs.sort(key=lambda x: os.path.getmtime(os.path.join(outputs_dir, x)), reverse=True)

        response_data = {"outputs": outputs}

        response_data = json.dumps(response_data, indent=2)

        return HttpResponse(response_data, content_type="application/json")

    else:
        error_message = {"error": "Method not allowed"}
        return JsonResponse(error_message, status=405)
 
def hello(request):
    name = 'echo'
    cmd = 'echo helloWorld; echo :D'
    return runCommand(name,cmd)

def getList(request):
    name = 'ls'
    cmd = 'ls'
    return runCommand(name,cmd)

def showPath(request):
    name = 'pwd'
    cmd = 'pwd'
    return runCommand(name,cmd)

def longCmd(request):
    name = 'longCmd'
    cmd = 'sleep 3;find ~;sleep 3;find ~;sleep 3;find ~'
    return runCommand(name,cmd)

def definitions(request):
    cmdName = request.GET.get("command", "")

    commands = [
        {'name': 'hello', 'command': 'echo helloWorld; echo :D',  'desc' : 'echo is a command that outputs the strings that are passed to it'},
        {'name': 'getList', 'command': 'ls', 'desc' : 'ls, lists the files in the working directory.'},
        {'name': 'showPath', 'command': 'pwd', 'desc' :'pwd, display the current working directory. '},
        {'name': 'longCmd', 'command': 'sleep 3;find ~;sleep 3;find ~;sleep 3;find ~', 'desc' :  'longCmd is for testers to test status 2.'},
    ]

    if cmdName:
        for cmd in commands:
            if cmd['name'] == cmdName:
                response_data = {
                    'exp': cmd
                }
                response_data = json.dumps(response_data, indent=2)
                return HttpResponse(response_data, content_type="application/json")

        response_data = {
            'message': 'Command not found.'
        }
        response_data = json.dumps(response_data, indent=2)
        return HttpResponse(response_data, content_type="application/json")

    else:
        response_data = {
        'commands': commands
        }
        
        response_data = json.dumps(response_data, indent=2)

        return HttpResponse(response_data, content_type="application/json")

