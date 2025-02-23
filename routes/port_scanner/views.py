import json
import re
from django.http import JsonResponse
from django.shortcuts import render
import nmap # type: ignore
from django.views.decorators.csrf import csrf_exempt

def port_scanner(request):
    return render(request, 'port_scanner.html', {})

# def scan(request):
#     for i in range(1, 100000000):
#         pass
#     print("received payload")
#     return JsonResponse({"result": "Ekdhum badiya"})

def scan(request):
    if request.method != "POST":
        print(request.method)
        return render(request, "error.html", {"status" : 405})
        # return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # Parse JSON payload
        data = json.loads(request.body)
        target_host = data.get("host", "").strip()
        target_ports = data.get("ports", "").strip()

        # Validate Host (IP or Domain)
        host_pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$|^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")
        if not host_pattern.match(target_host):
            return JsonResponse({"error": "Invalid host. Enter a valid IP or domain."}, status=400)

        # Validate Ports (Comma-separated numbers)
        if not re.fullmatch(r"(\d{1,5})(,\d{1,5})*", target_ports):
            # return render(request, "error.html", {"status" : 400})

            return JsonResponse({"error": "Invalid port format. Use comma-separated numbers (e.g., 22,80,443)."}, status=400)

        ports = target_ports.split(",")

        # Initialize Nmap Scanner
        nm = nmap.PortScanner()
        scan_results = {}

        for port in ports:
            try:
                nm.scan(target_host, port)
                port_int = int(port)

                state = nm[target_host]["tcp"][port_int]["state"] or "Unknown"
                service = nm[target_host]["tcp"][port_int].get("name") or "Unknown"  # Retrieve service name


                scan_results[port] = {"state": state, "service": service}
            except Exception as e:

                scan_results[port] = {"state": "Error", "service": str(e)}

        # Format result similar to the first format
        result = "\n".join(f"Port {port}: {info['state']} (Service: {info['service']})" for port, info in scan_results.items())

        return JsonResponse({"result": result})

    except json.JSONDecodeError:
        # return render(request, "error.html", {"status" : 400})
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)
    except Exception as e:
        # return render(request, "error.html", {"status" : 500, "error": f"Server error: {str(e)}"})

        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)