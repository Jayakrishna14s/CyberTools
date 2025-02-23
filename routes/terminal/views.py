import io
import socket
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render # type: ignore
from barcode.ean import EAN13
from barcode.writer import ImageWriter
from PIL import Image, ImageOps, ImageDraw

import phonenumbers
from phonenumbers import geocoder, carrier
import pyqrcode


def terminal(request):
    return render(request, 'terminal.html', {})

def getMyIP(request):
    try:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0] 
        else:
            ip = request.META.get('REMOTE_ADDR')  

        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = "Hostname could not be resolved"

        return JsonResponse({"ip": ip, "hostname": hostname})
    
    except Exception as e:
        return JsonResponse({"error": str(e)})
    

def genbarcode(request):
    try:
        number = request.GET.get("number")
        if not number or len(number) != 12 or not number.isdigit():
            return HttpResponse("Invalid input! Must be a 12-digit number.", status=400)

        # Generate barcode
        barcode_buffer = io.BytesIO()
        my_code = EAN13(number, writer=ImageWriter())
        my_code.write(barcode_buffer)

        # Load barcode image and convert to RGBA (for transparency support)
        barcode_buffer.seek(0)
        barcode_img = Image.open(barcode_buffer).convert("RGBA")

        # Define colors
        line_color = (34, 197, 94, 255)  # Green-500 (#22c55e)
        transparent = (0, 0, 0, 0)  # Fully transparent

        # Process each pixel
        pixels = barcode_img.load()
        width, height = barcode_img.size

        for x in range(width):
            for y in range(height):
                r, g, b, a = pixels[x, y]

                if r < 100 and g < 100 and b < 100:  # Detect dark pixels (barcode lines)
                    pixels[x, y] = line_color  # Change to green
                else:
                    pixels[x, y] = transparent  # Set background to transparent

        # Save the modified barcode
        final_buffer = io.BytesIO()
        barcode_img.save(final_buffer, format="PNG")
        final_buffer.seek(0)

        return HttpResponse(final_buffer.getvalue(), content_type="image/png")

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    
    
def genqrcode(request):
    try:
        # Get URL from the request
        url = request.GET.get("URL")
        if not url:
            return HttpResponse("Invalid input! URL is required.", status=400)

        # Generate QR Code
        qr_code = pyqrcode.create(url)

        # Save QR Code as PNG in memory
        qr_buffer = io.BytesIO()
        qr_code.png(qr_buffer, scale=6)  # Generate QR as PNG
        qr_buffer.seek(0)

        # Convert PNG to PIL Image
        qr_pil = Image.open(qr_buffer).convert("RGBA")  # Convert to RGBA for transparency

        # Change QR code color to Green (#22c55e) & make background transparent
        data = qr_pil.getdata()
        new_data = []
        for item in data:
            # If pixel is black, replace with green
            if item[:3] == (0, 0, 0):  
                new_data.append((34, 197, 94, 255))  # Green-500 color
            else:
                new_data.append((255, 255, 255, 0))  # Transparent background

        qr_pil.putdata(new_data)

        # Save the modified QR code as PNG
        final_buffer = io.BytesIO()
        qr_pil.save(final_buffer, format="PNG")
        final_buffer.seek(0)

        # Return QR code as PNG image response
        return HttpResponse(final_buffer.getvalue(), content_type="image/png")

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def scanphone(request):
    try:
        phone = request.GET.get("phone")

        # Validate phone number format
        if not phone or not phone.startswith("+") or not phone[1:].isdigit() or not (10 <= len(phone[1:]) <= 15):
            return JsonResponse({"error": "Phone number must start with '+' and contain 10-15 digits."}, status=400)

        # Parse the phone number
        number = phonenumbers.parse(phone)

        # Get country and carrier information
        country = geocoder.description_for_number(number, "en")
        supplier = carrier.name_for_number(number, "en")

        # Return response as JSON
        return JsonResponse({
            "phone": phone,
            "country": country if country else "Unknown",
            "supplier": supplier if supplier else "Unknown",
            "status": "success"
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
