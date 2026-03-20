from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import AudioUploadForm
from .utils import predict_genre
import os
import uuid
import traceback
from django.conf import settings

def upload_audio(request):
    predicted_genre = None
    error_message = None
    uploaded_file_url = None

    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save uploaded file with a safe UUID name
                audio_file = request.FILES['audio_file']
                
                # Extract original extension safely
                ext = ""
                if "." in audio_file.name:
                    ext = audio_file.name.rsplit('.', 1)[-1]
                else:
                    ext = "wav"
                
                safe_filename = f"{uuid.uuid4().hex}.{ext}"
                
                fs = FileSystemStorage()
                filename = fs.save(safe_filename, audio_file)
                uploaded_file_url = fs.url(filename)
                
                # Get absolute path for processing
                file_path = os.path.join(settings.MEDIA_ROOT, filename)
                
                # Predict genre
                predicted_genre = predict_genre(file_path)
                
            except Exception as e:
                error_message = f"An error occurred during processing: {str(e)}"
    else:
        form = AudioUploadForm()

    context = {
        'form': form,
        'predicted_genre': predicted_genre,
        'uploaded_file_url': uploaded_file_url,
        'error_message': error_message,
        'classes': ['blues', 'classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']
    }
    return render(request, 'index.html', context)
