from django.shortcuts import render, redirect
from django.http import JsonResponse
import numpy as np
import json
import joblib
from django.views.decorators.csrf import csrf_exempt
from .models import Animal


# Create your views here.
def index(request):
    return render(request,"animalSign/index.html")


svm_classifier1 = joblib.load('animalSign/animal_Models/svm_animal_sign_model.pkl')
label_encoder1 = joblib.load('animalSign/animal_Models/animal_label_encoder.pkl')
scaler1 = joblib.load('animalSign/animal_Models/animal_scaler.pkl')

def predict_animal_sign(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            landmarks = np.array(data['landmarks']).reshape(1, -1)
            
            landmarks_scaled = scaler1.transform(landmarks)
            
            prediction = svm_classifier1.predict(landmarks_scaled)
            
            predicted_label = label_encoder1.inverse_transform(prediction)[0]
            
           
            return JsonResponse({'prediction': predicted_label})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)



@csrf_exempt
def gpt_search(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            sign_detected = data.get("sign")
            last_animal = data.get("last_animal")

            if sign_detected == "ok" and last_animal:
                # Query the database for the animal details
                animal = Animal.objects.filter(name__iexact=last_animal).first()
                
                if animal:
                    return JsonResponse({"animal_details": animal.introduction})
                else:
                    return JsonResponse({"error": f"Details for '{last_animal}' not found."}, status=404)
            else:
                return JsonResponse({"error": "No OK sign or animal found."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
    
    return JsonResponse({"error": "Only POST requests are allowed."}, status=405)
