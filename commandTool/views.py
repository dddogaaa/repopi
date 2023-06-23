from django.shortcuts import render
from django.http import HttpResponse , JsonResponse


import os
import subprocess
import datetime
import pytz

from django.conf import settings as Settings
from .models import CommandExecution
from django.utils import timezone

TR = pytz.timezone('Europe/Istanbul')

def execute_command(request):
    if request.method == 'GET':
        command = request.GET.get('command')
        if command:
            try:
                logs_dir = set_dir(request)
                creationTime = datetime.datetime.now(TR).strftime("%Y-%m-%d_%H-%M-%S")
                output_file = os.path.join(logs_dir, f"{creationTime}---{command}.output")
                with open(output_file, 'w') as file:
                    start_time = datetime.datetime.now(TR).strftime("%Y-%m-%d_%H-%M-%S")
                    result = subprocess.run (
                        command,
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    end_time = datetime.datetime.now(TR).strftime("%Y-%m-%d_%H-%M-%S")
                    status = result.returncode
                    # Buraya doğanın file.write gelecek.
                    file.write(result.stdout)
                    file.write(result.stderr)
                    #execution = CommandExecution(command=command, status=status, output_file=output_file,start_execution=start_time, end_execution=end_time)
                    #execution.save()
                    #execution_time = 
                    # return JsonResponse'da execution time eklenecek.
                    return JsonResponse({'command': command, 'output_file': output_file, 'status': status })

            except subprocess.CalledProcessError as e:
                error_message = str(e)
                return JsonResponse({'error': error_message})

    else:
        return JsonResponse({'error': 'Method not allowed'})


def serve_log_file(request):
    try:
        file_name = request.GET.get('file_name')
        logs_dir = set_dir(request)
        file_path = os.path.join(logs_dir, file_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_content = file.read()
            return JsonResponse({'file_content': file_content}, safe=False)
        else:
            return JsonResponse({'error': f'Output file {file_name} not found.'})

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'})

def list_logs(request):

    if request.method == 'GET':
        logs_dir = set_dir(request)
        logs = os.listdir(logs_dir)
        logs.sort(key=lambda x: os.path.getmtime(os.path.join(logs_dir,x)))

        response_data = {'logs': logs}
        return JsonResponse(response_data)
    else:
        error_message = {'error': 'Method not allowed'}
        return JsonResponse(error_message, status=405)


def set_dir(request):
    logs_dir = Settings.LOGS_DIR

    if not logs_dir:
        logs_dir = os.path.join(Settings.BASE_DIR, 'logs')

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    return logs_dir


     














