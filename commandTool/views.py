from django.http import StreamingHttpResponse,HttpResponse,JsonResponse
from django.shortcuts import render
from subprocess import Popen
from datetime import datetime
from django.conf import settings as Settings
from .models import Result, Repo
import json
import os
import pytz
import datetime
import threading
import json
from django.core.paginator import Paginator

#-----------for linux-----------

import inotify.adapters
def stream(request,djID):
    def gen_message(msg):
        return '{}'.format(msg)

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

#------------for mac-------------

# import selectors 

# def stream(request, djID):
#     def gen_message(msg):
#         return '{}'.format(msg)

#     def iterator():
#         result = Result.objects.get(id=djID)
#         path = result.file
#         with open(path, 'r') as file:
#             file_content = file.read()
#             yield gen_message(file_content)

#         kqueue = selectors.DefaultSelector()
#         file_descriptor = open(path, 'rb')
#         kqueue.register(file_descriptor, selectors.EVENT_READ)

#         prev_file_size = os.path.getsize(path)
#         try:
#             while True:
#                 events = kqueue.select()
#                 for key, mask in events:
#                     if key.fileobj == file_descriptor and mask & selectors.EVENT_READ:
#                         file_size = os.path.getsize(path)
#                         if file_size > prev_file_size:
#                             with open(path, 'r') as file:
#                                 file.seek(prev_file_size)
#                                 new_lines = file.read().splitlines()
#                                 for line in new_lines:
#                                     yield gen_message(line)
#                             prev_file_size = file_size
#         except KeyboardInterrupt:
#             pass
#         finally:
#             kqueue.unregister(file_descriptor)
#             file_descriptor.close()

#     stream = iterator()
#     response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
#     response['Cache-Control'] = 'no-cache'

#     return response

#------------------------------------


def index(request):
    return render(request,'stream.html')

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
        'name' : name,
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

    return result.status

def runCommand(name,command):
    try:
        thread = threading.Thread(target=run, args=(name, command))
        thread.start()

        response_data = {
            'message': 'Command execution operation started.',
            'success': True  
        }

        return JsonResponse(response_data, json_dumps_params={'indent': 2})

    except Exception as e:
        response_data = {
            'message': 'Failed to start the command execution operation.',
            'success': False 
        }

        return JsonResponse(response_data, json_dumps_params={'indent': 2})
    
def hello(request):
    name = 'hello'
    cmd = 'echo helloWorld; echo :D'
    return runCommand(name,cmd)

def wrong(request):
    name = 'wrong'
    cmd = ':D'
    return runCommand(name,cmd)

def getList(request):
    name = 'getList'
    cmd = 'ls'
    return runCommand(name,cmd)

def showPath(request):
    name = 'showPath'
    cmd = 'pwd'
    return runCommand(name,cmd)

def longCmd(request):
    name = 'longCmd'
    # cmd = 'sleep 3;find ~;sleep 3;find ~;sleep 3;find ~'
    # cmd = 'sleep 30;pwd;sleep 5;pwd;ls;ls;sleep 5;ls;sleep 8'
    cmd = 'ping -c 60 8.8.8.8'
    return runCommand(name,cmd)

def jobs_data(request):  #change this to jobs for jsonresponse
    default_value = 20
    show = request.GET.get('show', '')

    if show:
        default_value = show

    all_records = Result.objects.all().order_by('id')
    items_per_page = default_value 

    paginator = Paginator(all_records, items_per_page)

    page_number = request.GET.get('page', 1)

    try:
        current_page = paginator.page(page_number)
    except:
        current_page = paginator.page(1) 

    response_data = {
        "total_num": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": current_page.number,
        "has_next": current_page.has_next(),
        "has_previous": current_page.has_previous(),
        "history": [ 
            {
                "ID": data.id,
                'Command Name': data.name,
                "Status": data.status,
                "Command": data.command,
                "Stime": data.start_time,
                "Etime": data.end_time,
                "File": data.file,
            } for data in current_page
        ],
    }

    return JsonResponse(response_data, json_dumps_params={'indent': 2})

def get_job(request,id):
    try:
            command = Result.objects.get(id=id)

            response = {
                "ID": command.id,
                "Command": command.command, 
                "Stime":command.start_time,
                "Etime":command.end_time,
                "File-DIR":command.file,
            }

            json_response = json.dumps(response, indent=2)

            return HttpResponse(json_response, content_type="application/json")

    except Result.DoesNotExist:
        error_response = {"error": "Command ID not found."}

        json_response = json.dumps(error_response, indent=2)

        return HttpResponse(json_response, status=404, content_type="application/json")
    
# def jobs_w_status(request,status):

#     objects = Result.objects.filter(status = status)

#     if status == None:
#         message = { "message" : "Valid options are 0,1,2" }
#         return HttpResponse(message, content_type = 'application/json')
#     else:
#         items_dict = {
#             obj.id: {
#                 'ID': obj.id,
#                 'Status': obj.status,
#                 'Command': obj.command,
#                 'Stime': obj.start_time,
#                 'Etime': obj.end_time,
#                 'File-DIR': obj.file,
#             }
#             for obj in objects
#             }

#         response_json = json.dumps(items_dict, indent=4)
#         return HttpResponse(response_json, content_type='application/json')
    
def jobs_filter(request):
    command = request.GET.get('command', '')
    status = request.GET.get('status', '')

    if status and command:
        try:
            items_dict = {
                obj.id: {
                    'ID': obj.id,
                    'Command Name':obj.name,
                    'Status': obj.status,
                    'Command': obj.command,
                    'Stime': obj.start_time,
                    'Etime': obj.end_time,
                    'File-DIR': obj.file,
                }
                for obj in Result.objects.filter(status=status, name=command)
            }

            response_json = json.dumps(items_dict, indent=4)
            return HttpResponse(response_json, content_type='application/json')
        except:
            message = {"message": "Invalid status or command."}
            return HttpResponse(json.dumps(message), content_type='application/json')

    elif status:
        try:
            items_dict = {
                obj.id: {
                    'ID': obj.id,
                    'Command Name':obj.name,
                    'Status': obj.status,
                    'Command': obj.command,
                    'Stime': obj.start_time,
                    'Etime': obj.end_time,
                    'File-DIR': obj.file,
                }
                for obj in Result.objects.filter(status=status)
            }

            response_json = json.dumps(items_dict, indent=4)
            return HttpResponse(response_json, content_type='application/json')
        except:
            message = {"message": "Valid options for status are 0, 1, or 2."}
            return HttpResponse(json.dumps(message), content_type='application/json')

    elif command:
        try:
            items_dict = {
                obj.id: {
                    'ID': obj.id,
                    'Command Name':obj.name,
                    'Status': obj.status,
                    'Command': obj.command,
                    'Stime': obj.start_time,
                    'Etime': obj.end_time,
                    'File-DIR': obj.file,
                }
                for obj in Result.objects.filter(name=command)
            }

            response_json = json.dumps(items_dict, indent=4)
            return HttpResponse(response_json, content_type='application/json')
        except:
            message = {"message": "Invalid command."}
            return HttpResponse(json.dumps(message), content_type='application/json')

    else:
        message = {"message": "Please provide either 'status' or 'command' parameter."}
        return HttpResponse(json.dumps(message), content_type='application/json')
   
def base(request):
    return render(request, 'base.html')

def repo(request):
    return render(request, 'repo.html')

def jobs(request):
    return render(request, 'jobs.html')

def mirrorNFF(request):
    name = 'm_NonFreeFirmware'
    create = {
        'mirrorName': 'pardus-23deb-firmware-arm64',
        'mirrorType': 'create',
        'archiveUrl': Repo._meta.get_field('archiveUrl').get_default(),  
        'dist': 'yirmiuc-deb',
        'components': 'non-free-firmware',
        'architectures': 'arm64'
    }

    if create['architectures']:
        cmd = f"aptly mirror create -architectures='{create['architectures']}' {create['mirrorName']} {create['archiveUrl']} {create['dist']} {create['components']}"
    else:
        cmd = f"aptly mirror create {create['mirrorName']} {create['archiveUrl']} {create['dist']} {create['components']}"
    
    Repo.objects.create(**create)

    return runCommand(name,cmd)

def mirrorUpdate(request):
    name='mu_NonFreeFirmware'
    cmd = 'aptly mirror update pardus-23deb-firmware-arm64'

    create = {
        'mirrorName': 'pardus-23deb-firmware-arm64',
        'mirrorType': 'update'
    }

    Repo.objects.create(**create)

    return runCommand(name,cmd)

def mirrorDrop(request):
    name='md_NonFreeFirmware'

    cmd = 'aptly mirror drop pardus-23deb-firmware-arm64'

    create = {
        'mirrorName': 'pardus-23deb-firmware-arm64',
        'mirrorType': 'drop'
    }

    Repo.objects.create(**create)

    return runCommand(name,cmd)
