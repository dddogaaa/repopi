# Imports
import os
import inotify.adapters
import json
import os
import pytz
import datetime
import threading
import json

# Other Imports
from django.http import StreamingHttpResponse,HttpResponse,JsonResponse
from django.shortcuts import render
from subprocess import Popen
from datetime import datetime
from django.conf import settings as Settings
from .models import Result

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

def jobs_w_status(request,status):

    objects = Result.objects.filter(status = status)

    if status == None:
        message = { "message" : "Valid options are 0,1,2" }
        return HttpResponse(message, content_type = 'application/json')
    else:
        items_dict = {
            obj.id: {
                'ID': obj.id,
                'Status': obj.status,
                'Command': obj.command,
                'Stime': obj.start_time,
                'Etime': obj.end_time,
                'File-DIR': obj.file,
            }
            for obj in objects
            }

        response_json = json.dumps(items_dict, indent=4)
        return HttpResponse(response_json, content_type='application/json')

def jobs(request):

    objects = Result.objects.all()
    
    items_dict = {
        obj.id: {
            'ID': obj.id,
            'Status': obj.status,
            'Command': obj.command,
            'Stime': obj.start_time,    
            'Etime': obj.end_time,
            'File-DIR': obj.file,
        }
        for obj in objects
    }


    response_json = json.dumps(items_dict, indent=4)
    return HttpResponse(response_json, content_type='application/json')

def jobs_w_id(request,id):
    
    if id == "":
        message = {"error" : "Enter 0 or 1 or 2."}
        return HttpResponse(message, content_type='application/json')
    else:
        objects = Result.objects.filter(id = id)

    items_dict = {
        obj.id: {
            'ID': obj.id,
            'Status': obj.status,
            'Command': obj.command,
            'Stime': obj.start_time,    
            'Etime': obj.end_time,
            'File-DIR': obj.file,
        }
        for obj in objects
    }
    response_json = json.dumps(items_dict, indent=4)
    return HttpResponse(response_json, content_type='application/json')


def stream2(request):
    return render(request, "stream_request.html")