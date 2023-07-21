import os
import inotify.adapters
from django.http import StreamingHttpResponse,HttpResponse,JsonResponse
from django.shortcuts import render
from subprocess import Popen
from datetime import datetime
from django.conf import settings as Settings
from .models import Result
import json
import os
import pytz
import datetime
import threading
import json

def stream(request,djID):
    def gen_message(msg):
        return '{}\n'.format(msg)

    def iterator():      
        result = Result.objects.get(id=djID)
        path = result.file
        with open(path, 'r') as file:
            file_content = file.read()
            yield gen_message(file_content)

        notifier = inotify.adapters.Inotify()
        notifier.add_watch(os.path.dirname(path))
        prev_file_size = os.path.getsize(path)
        while True:
            for event in notifier.event_gen():
                if event is not None:
                    (_, type_names, _, filename) = event
                    if filename == os.path.basename(path) and 'IN_MODIFY' in type_names:
                        file_size = os.path.getsize(path)
                        if file_size > prev_file_size:
                            with open(path, 'r') as file:
                                file.seek(prev_file_size)
                                new_lines = file.read().splitlines()
                                for line in new_lines:
                                    yield gen_message(line)
                            prev_file_size = file_size

    stream = iterator()
    response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'

    return response

def index(request,djID):
    context = {'djID': djID}
    return render(request, 'stream.html',context)

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

    proc = Popen(command, stdout=log, stderr=log, shell=True, text=True)
    
    proc.wait()

    returnValue = proc.poll()

    if  returnValue == 0 :
        result.status = 1
        result.end_time = get_date_now()
        print('Command finished successfully.')
    else:
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
    # cmd = 'sleep 30;pwd;sleep 5;pwd;ls;ls;sleep 5;ls;sleep 8'
    return runCommand(name,cmd)

def jobs(request):
    all_records = Result.objects.all()
    
    commands = []
    for data in all_records:
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

def get_job(request,id):
    try:
            command = Result.objects.get(id=id)

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