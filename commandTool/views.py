from subprocess import Popen
from datetime import datetime
from django.conf import settings as Settings
from .models import Result 
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from django.shortcuts import render
import json
import os
import pytz
import datetime
import threading
import json
import re

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
    # cmd = 'sleep 3;find ~;sleep 3;find ~;sleep 3;find ~'
    cmd = 'sleep 30;pwd;sleep 5;pwd;ls;ls;sleep 5;ls;sleep 8'
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

def stream(id):
    def gen_message(msg):
        return '{}\n'.format(msg)

    def iterator():
        result = Result.objects.get(id=id)
        prev_file_size = os.path.getsize(result.file)  
        while result.status == 2:
            file_size = os.path.getsize(result.file)  
            if file_size > prev_file_size:
                with open(result.file, 'r') as file:
                    file.seek(prev_file_size)  
                    new_lines = file.read().splitlines()
                    for line in new_lines:
                        yield gen_message(line)
                prev_file_size = file_size 

    stream = iterator()
    response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

def filter(request):
    status = request.GET.get("status", "")
    id = request.GET.get("id")
    url = request.build_absolute_uri()

    filtered_data = Result.objects.all()
    status = int(status)

    if status:  
        if status == 1:
            filtered_data = Result.objects.filter(status=1)  
        elif status == 0:
            filtered_data = Result.objects.filter(status=0)
        elif status == 2:
            filtered_data = Result.objects.filter(status=2)  
        elif status == 3:
            filtered_data = Result.objects.all()  
        else:
            return HttpResponse('Enter 0 or 1 or 2 or 3')
            

    if "stream" in url:
        match = re.search(r'id=(\d+)', url)
        if match:
            extracted_number = match.group(1)
            print(extracted_number)
        return stream(extracted_number)

    elif id:
        try:
            command = Result.objects.get(id=id)
            output = ""
            with open(command.file, "r") as file:
                output = file.read()

            output = output.replace('\n', '/')

            response = {
                "id": command.id,
                "command": command.command, 
                "output_path":command.file,
                "start_time":command.start_time,
                "end_time":command.end_time
            }

            json_response = json.dumps(response, indent=2)

            return HttpResponse(json_response, content_type="application/json")

        except Result.DoesNotExist:
            error_response = {"error": "Command ID not found."}

            json_response = json.dumps(error_response, indent=2)

            return HttpResponse(json_response, status=404, content_type="application/json")

    else:
        commands = []
        for data in filtered_data:
            command_info = {
                "id": data.id,
                "status": data.status,
                "command": data.command,
                "start_time": data.start_time,
                "end_time": data.end_time,
                "file": data.file
            }
            commands.append(command_info)

        response = {"filtered_commands": commands}

        response_data = json.dumps(response, indent=2)

        return HttpResponse(response_data, content_type="application/json")


