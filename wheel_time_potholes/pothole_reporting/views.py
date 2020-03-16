from django.shortcuts import render
import database as db

# Create your views here.

def index(request):
    query = "SELECT * FROM pothole"
    cursor = db.connection.cursor()
    cursor.execute(query)
    response = dict()
    response['results'] = cursor.fetchall()
    response['length'] = cursor.rowcount
    response['warnings'] = cursor.fetchwarnings()
    return render(request, 'index.html', context=response)