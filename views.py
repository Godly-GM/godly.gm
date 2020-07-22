from django.shortcuts import render
from add_places.models import Place
from add_places.serializer import Addplaceserializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage


# Create your views here.
def addplace(request):
    if request.method == "POST":
        obj = Place()
        obj.pname = request.POST.get("place")

        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        obj.image = myfile.name
        obj.lat = request.POST.get("lat")
        obj.longi = request.POST.get("long")
        obj.description = request.POST.get("des")
        obj.save()
    return render(request,'add_places/addplace.html')



def viewplace(request):
    objlist = Place.objects.all()
    context = {
        'objval': objlist,
    }
    return render(request, 'add_places/viewplace.html',context)


class Viewplace(APIView):
    def get(self, request):
        s = Place.objects.all()
        ser = Addplaceserializer(s, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = Addplaceserializer(data=request.data)
        if ser.is_valid():
            ser.save()
        return HttpResponse("ok")