from django.shortcuts import render
from subprocess import Popen
from datetime import datetime,timedelta
from django.conf import settings as Settings
from .models import Result
from django.http import HttpResponse,JsonResponse
import json
import os
import time
import pytz
import datetime
import threading


COMMANDS = [
    {'name': 'echo','command': 'echo yusuf;echo duzgun'},
    {'name': 'ls','command': 'ls'},
    {'name': 'pwd','command': 'pwd'},
    {'name': 'longCmd','command': 'sleep 3;find ~;sleep 3;find ~;sleep 3;find ~'},
    {'name': 'stream','command': 'sleep 5;ls;sleep 3;pwd'},
    {'name': 'shortCmd','command': 'sleep 3'}, 
    {'name': 'sl200','command': 'sleep 200'},
    {'name': 'sl500','command': 'sleep 500'},
    {'name': 'sl1200','command': 'sleep 1200'},
    {'name': 'exit','command': 'exit 7'},
    {'name': 'mousepad','command': 'mousepad'},
    {'name': 'touch','command': 'touch'},
]

def get_data_folder():
    return Settings.DATA_FOLDER

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

def run(name, command):
    print(name+" basladi")
    time_start = time.time()
    date_now = get_date_now()

    outputs_folder = get_data_folder()
    create_data_folder(outputs_folder)
    output_file = os.path.join(outputs_folder, f"{date_now}-{name}.txt")
    print(output_file)

    item = {
        'name' : name,
        'message':'Command execution in progress.',
        'file' : output_file,
        "command": command,
        "status": 2,
        "execution_time": None,
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
    print(returnValue)


    if  returnValue == 0 :
        result.status = 1
        result.message = 'Command executed successfully'
        result.end_time = get_date_now()
        time_end = time.time()
        result.execution_time = time_end -time_start
        print('Cmd ended.')
    else:

        result.message = 'Command encountered an error.' 
        result.status = 0
        result.end_time = get_date_now()
        time_end = time.time()
        result.execution_time = time_end -time_start
        print('Cmd has problem.')

    result.save()

def runCommand(request):
    name = request.GET.get('command','') 

    command = next((cmd for cmd in COMMANDS if cmd['name'] == name), None)
    if command:
        thread = threading.Thread(
        target=run, args=(command['name'], command['command']))

        thread.start()

        response = {
            'message' : 'Command execution started.'
        }

        json_response = json.dumps(response, indent=2)

        return HttpResponse(json_response, content_type="application/json")
    else:
        response_data = {
            'message': 'Command not found'
        }
        
        json_response = json.dumps(response_data, indent=2)

        return HttpResponse(json_response, content_type="application/json")
    
def filter_commands(request):
    status = request.GET.get("status", "")
    command = request.GET.get('command','')

    command_names = [cmd['name'] for cmd in COMMANDS]

    filtered_data = Result.objects.all()

    if status:
        filtered_data = filtered_data.filter(status=status)
    if command:
        filtered_data = filtered_data.filter(command__in=command_names)

    commands = []
    for data in filtered_data:
        command_info = {
            "id": data.id,
            "status": data.status,
            "message": data.message,
            'command_name': data.name,
            # "command": data.command,
            "start_time": data.start_time,
            "end_time": data.end_time,
            "execution_time": data.execution_time,
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