import json
from django.shortcuts import render # type: ignore
import json
import socket
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
import requests

def information_gathering(request):
    return render(request, 'information_gathering.html', {})



def gather(request):

    if request.method != "POST":
        print(request.method)
        return render(request, "error.html", {"status" : 405})
    
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = data.get("url").strip()

            if not url:
                return JsonResponse({"result": "Invalid URL"}, status=400)

            # Get IP Address
            ip_address = socket.gethostbyname(url)
            
            # Get location info
            response = requests.get(f"https://ipinfo.io/{ip_address}/json")
            info = response.json()

            print(info)

            # result = f"IP Address: {ip_address}\n"
            # result += f"Location: {info.get('loc', 'N/A')}\n"
            # result += f"Region: {info.get('region', 'N/A')}\n"
            # result += f"City: {info.get('city', 'N/A')}\n"
            # result += f"Country: {info.get('country', 'N/A')}\n"
            
            result = ""

            for key, value in info.items():
                result += f"{key.capitalize()}: {value if value else 'N/A'}\n"

            return JsonResponse({"result": result})

        except Exception as e:
            return JsonResponse({"result": "Enter a valid URL\n" + f"Error: {str(e)}"}, status=500)

    return JsonResponse({"result": "Invalid Request"}, status=400)