from datetime import datetime, timedelta
import datetime
import time
import subprocess
import os
import threading
import pytz
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import Response
import json
from django.conf import settings as Settings


def take_time():
    time_zone = pytz.timezone("Europe/Istanbul")
    time = datetime.datetime.now(time_zone)
    return time


def set_dir():
    outputs_dir = Settings.OUTPUTS_DIR

    if not outputs_dir:
        outputs_dir = os.path.join(Settings.BASE_DIR, "outputs")

    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    return outputs_dir


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    creationTime = take_time().strftime("%Y-%m-%d_%H:%M:%S")
    file = os.path.join(dir_name, f"{creationTime}.txt")
    return file


def write_output(data, output_file):
    with open(output_file, "w") as file:
        # file.write(f'STATUS: {data["status"]}\n\n')
        # file.write(f'COMMAND: {data["command"]}\n\n')
        # file.write(f'EXECUTION_TIME: {data["execution_time"]}\n\n')
        # file.write(f'STDOUT:\n\n{data["stdout"]}\n\n')
        # if data["stderr"]:
        #     file.write(f'STDERR:\n\n{data["stderr"]}\n\n')
        # else:
        #     file.write('STDERR:\n\nNo error :)\n')
        file.write(f'{data["stdout"]}')
        if data["stderr"]:
            file.write(f'{data["stderr"]}')


def set_response_message(response, status):
    if status == 0:
        response["message"] = "Command encountered an error."
    elif status == 1:
        response["message"] = "Command executed successfully."
    elif status == 2:
        response["message"] = "Command execution in progress."
    elif status == 127:
        response["message"] = "Command not found."


def execute_command(command):
    start_time = time.time()

    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )


    stdout, stderr = process.communicate()
    process.wait()

    end_time = time.time()
    execution_time = end_time - start_time
    rounded_time = "{:.6f}".format(execution_time)

    result = {
        "command": command,
        "status": process.returncode,
        "status": 1 if process.returncode == 0 else 0,
        "stdout": stdout.strip(),
        "stderr": stderr.strip(),
        "execution_time": rounded_time,
        "start_time": start_time,
        "end_time": end_time,
    }

    return result


def execute_command_in_thread(command, response):
    result = execute_command(command)

    outputs_dir = set_dir()

    output_file = create_dir(outputs_dir)

    result["output_file"] = output_file
    result["start_time"] = take_time().strftime("%Y-%m-%d %H:%M:%S.%f")
    result["end_time"] = take_time().strftime("%Y-%m-%d %H:%M:%S.%f")

    set_response_message(response, result["status"])

    # Komut bulunamadi hatasini da status 1 e getirmek icin;
    if result["status"] == 127:
        result["status"] = 1

    response["status"] = result["status"]
    response["execution_time"] = result["execution_time"]
    response["start_time"] = result["start_time"]
    response["end_time"] = result["end_time"]
    response["output_file"] = result["output_file"]

    # response.update(result)

    print("Command execution completed:", result)

    write_output(result, output_file)

    if response["status"] != 2:  # If Command execution is not in progress
        # Update response with start time, end time, and execution time
        response["start_time"] = result["start_time"]
        response["end_time"] = result["end_time"]
        response["execution_time"] = result["execution_time"]
        response["output_file"] = result["output_file"]

        if "thread_ID" in response:
            # Thread ID exists, update the corresponding database entry
            response_data = {
                k: v for k, v in response.items() if k != "stdout" and k != "stderr" and k != "start_time"
            }
            Response.objects.filter(thread_ID=response["thread_ID"]).update(
                **response_data
            )
        else:
            # Thread ID does not exist, create a new entry in the database
            response_data = {
                k: v for k, v in response.items() if k != "stdout" and k != "stderr"
            }
            Response.objects.create(**response_data)


def run_commands(request):
    command = request.GET.get("command", "")

    outputs_dir = set_dir()

    output_file = create_dir(outputs_dir)

    response = {
        "status": 2,
        "message": "Command execution continue...",
        "command": command,
        "execution_time": "",
        "start_time": take_time().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "end_time": "",
        'output_file': output_file
    }

    thread = threading.Thread(
        target=execute_command_in_thread, args=(command, response)
    )
    thread.start()

    if thread.is_alive():
        response["thread_ID"] = threading.get_ident()
        response["status"] = 2
        response["message"] = "Command execution still in progress."
        response['output_file']
        response.pop("end_time", None)
        response.pop("execution_time", None)

        response_data = {
            k: v for k, v in response.items() if k != "stdout" and k != "stderr"
        }
        Response.objects.create(**response_data)

    json_response = json.dumps(response, indent=2)

    return HttpResponse(json_response, content_type="application/json")


def filter_by_commands(request):
    command = request.GET.get("command", "")

    filtered_data = Response.objects.filter(command=command)

    commands = []
    for data in filtered_data:
        command_info = {
            "id": data.id,
            "status": data.status,
            "message": data.message,
            "command": data.command,
            "start_time": data.start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "end_time": data.end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "execution_time": data.execution_time,
            "output_file": data.output_file
            # Add other fields as needed
        }
        commands.append(command_info)

    response = {"filtered_commands": commands}

    json_response = json.dumps(response, indent=2)

    return HttpResponse(json_response, content_type="application/json")


def get_output_by_id(request, command_id):
    try:
        command = Response.objects.get(id=command_id)
        output = ""
        with open(command.output_file, "r") as file:
            output = file.read()

        # output = output.replace('\n', '/')

        response = {"id": command.id, "command": command.command, "output": output}

        json_response = json.dumps(response, indent=2)

        return HttpResponse(json_response, content_type="application/json")

    except Response.DoesNotExist:
        error_response = {"error": "Command ID not found."}

        json_response = json.dumps(error_response, indent=2)

        return HttpResponse(json_response, status=404, content_type="application/json")


def list_outputs(request):
    if request.method == "GET":
        outputs_dir = set_dir()

        file = create_dir(outputs_dir)
        outputs = os.listdir(outputs_dir)
        outputs.sort(key=lambda x: os.path.getmtime(os.path.join(outputs_dir, x)), reverse=True)

        response_data = {"outputs": outputs}

        response_data = json.dumps(response_data, indent=2)

        return HttpResponse(response_data, content_type="application/json")

    else:
        error_message = {"error": "Method not allowed"}
        return JsonResponse(error_message, status=405)


def filter_by_date(request):
    num_days = request.GET.get(
        "num_days", 30
    )  # Kullanıcıdan kaç günü filtrelemek istediğini alır

    if int(num_days) < 1:
        error_message = {
            "error": "Please write appropriate number. Method not allowed."
        }
        return JsonResponse(error_message, status=405)
    else:
        end_time = take_time()  # Şu anki zamanı alır
        start_time = end_time - timedelta(
            days=int(num_days)
        )  # Belirtilen gün sayısını kapsayan başlangıç zamanı

        filtered_data = Response.objects.filter(
            start_time__range=(
                start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            )
        )

        commands = []
        for data in filtered_data:
            command_info = {
                "id": data.id,
                "status": data.status,
                "message": data.message,
                "command": data.command,
                "start_time": data.start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "end_time": data.end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "execution_time": data.execution_time,
                "output_file": data.output_file
                # Diğer alanları isteğe bağlı olarak ekleyebilirsiniz
            }
            commands.append(command_info)

        response = {"filtered_commands": commands}

        response_data = json.dumps(response, indent=2)

        return HttpResponse(response_data, content_type="application/json")


def filter_by_status(request):
    status = request.GET.get("status", "")

    filtered_data = Response.objects.filter(status=status)

    commands = []
    for data in filtered_data:
        if status != '2':
            command_info = {
                "id": data.id,
                "status": data.status,
                "message": data.message,
                "command": data.command,
                "start_time": data.start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "end_time": data.end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                "execution_time": data.execution_time,
                "output_file": data.output_file
                # Diğer alanları isteğe bağlı olarak ekleyebilirsiniz
            }
            commands.append(command_info)
        else:
            command_info = {
                "id": data.id,
                "status": data.status,
                "message": data.message,
                "command": data.command,
                "start_time": data.start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                # Diğer alanları isteğe bağlı olarak ekleyebilirsiniz
            }
            commands.append(command_info)

    response = {"filtered_commands": commands}

    response_data = json.dumps(response, indent=2)

    return HttpResponse(response_data, content_type="application/json")
    

def get_output_by_id(request, command_id):
    try:
        command = Response.objects.get(id=command_id)
        output = ""
        with open(command.output_file, "r") as file:
            output = file.read()

        # output = output.replace('\n', '/')

        response = {"id": command.id, "command": command.command, "output": output}

        json_response = json.dumps(response, indent=2)

        return HttpResponse(json_response, content_type="application/json")

    except Response.DoesNotExist:
        error_response = {"error": "Command ID not found."}

        json_response = json.dumps(error_response, indent=2)
