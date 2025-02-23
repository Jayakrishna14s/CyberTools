import json
from django.http import JsonResponse
from django.shortcuts import render
import requests

def subdomain_scanner(request):
    return render(request, 'subdomain_scanner.html', {})


def scan(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    # Parse JSON request
    data = json.loads(request.body)
    domain = data.get("url").strip()

    if not domain:
        return JsonResponse({"error": "Domain is required"}, status=400)

    # Predefined subdomain list
    subdomains = [
        "app", "src", "abc", "docs", "mail", "cdn", 
        "blog", "test", "portal", "admin", "shop", "api"
    ]

    discovered_subdomains = []

    # Subdomain scanning
    for subdomain in subdomains:
        url = f"https://{subdomain}.{domain}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                discovered_subdomains.append(url)
        except requests.ConnectionError:
            continue  # Ignore failed subdomains

    print(discovered_subdomains)

    return JsonResponse({"found": discovered_subdomains})

