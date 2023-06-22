from django.shortcuts import render
from django.http import HttpResponse
import os
import subprocess
import datetime
from django.conf import settings as Settings
from .models import CommandExecution
from django.utils import timezone


def run_command(command):
    creationTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logs_dir = "logs"

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file = os.path.join(logs_dir, f"{creationTime}-{command}.log")

    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    with open(log_file, 'w') as file:
        file.write(process.stdout)
        file.write(process.stderr)

    status = process.returncode

    return status, log_file


def execute_command(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        log_content = ""

        start_time = timezone.now()
        
        status, log_file = run_command(command)

        end_time = timezone.now()


        if os.path.isfile(log_file):
            with open(log_file, 'r') as file:
                log_content = file.read()


        execution = CommandExecution(command=command, status=status, log_file=log_file, start_execution=start_time,end_execution=end_time)
        execution.save()

        return render(request, 'result.html', {'command': command, 'log_file': log_file, 'log_content': log_content, 'status': status, 'duration_seconds': execution.duration})

    return render(request, 'index.html')


def serve_log_file(request, log_file_name):
    try:
        with open(log_file_name, 'r') as file:
            file_content = file.read()
            
            # If you want the file downloadable:
            # response = HttpResponse(file_content, content_type='text/plain')
            # response['Content-Disposition'] = f'attachment; filename={log_file_name}'
            # return response
            
            return HttpResponse(file_content, content_type='text/plain')

    except FileNotFoundError:
        return HttpResponse(f'Log file {log_file_name} not found.', status=404)

def list_logs(request):

    logs_dir = Settings.LOGS_DIR
    logs = os.listdir(logs_dir)
    logs.sort(key=lambda x: os.path.getmtime(os.path.join(logs_dir,x)))

    context = {'logs': logs}
    return render(request, 'lists.html', context)





