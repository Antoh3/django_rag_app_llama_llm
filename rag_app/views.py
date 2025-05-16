import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


from .chroma_utils import load_documents,split_documents,add_to_chroma,clear_database
from .query_vector_db import query_rag

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@api_view(['POST'])
def test(request):
    return HttpResponse("Hello iam testing if route works")


@csrf_exempt
@api_view(['POST'])
def upload_pdf_view(request):
    file = request.FILES.get('file')
    if not file or not file.name.endswith('.pdf'):
        return Response({'error': 'Only PDF files are supported.'}, status=status.HTTP_400_BAD_REQUEST)

    file_path = os.path.join(UPLOAD_DIR, file.name)
    with default_storage.open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    try:
        documents = load_documents()
        chunks = split_documents(documents)
        add_to_chroma(chunks)
        return Response({'message': 'PDF uploaded, indexed, and saved to Chroma DB.'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['POST'])
def query_chroma_view(request):
    query = request.data.get('query')
    if not query:
        return Response({'error': 'Query text is required.'}, status=400)

    try:
        response = query_rag(query)
        return Response({'response': response})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@csrf_exempt
@api_view(["POST"])
def reset_chroma():
    clear_database()
    return HttpResponse({"message": "Chroma database cleared."})