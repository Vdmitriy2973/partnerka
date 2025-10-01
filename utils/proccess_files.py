import base64

from django.core.files.uploadedfile import UploadedFile

def process_uploaded_file(uploaded_file, max_size_mb=25):
    """
    Обрабатывает UploadedFile для передачи через Celery
    
    Args:
        uploaded_file: файл из request.FILES
        max_size_mb: максимальный размер файла в MB
    
    Returns:
        dict: данные файла в base64
    """
    if not isinstance(uploaded_file, UploadedFile):
        raise ValueError("Expected UploadedFile instance")
    
    # Проверяем размер файла
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        raise ValueError(f"Файл слишком большой: {file_size_mb:.2f}MB (максимум {max_size_mb}MB)")
    
    # Читаем содержимое файла
    file_content = uploaded_file.read()
    
    # Получаем оригинальное имя
    filename = uploaded_file.name
    
    # Определяем content_type
    content_type = uploaded_file.content_type
    if not content_type:
        # Если content_type не определен, пытаемся определить по расширению
        import mimetypes
        content_type, _ = mimetypes.guess_type(filename)
        content_type = content_type or 'application/octet-stream'
    
    # Кодируем в base64
    return {
        'filename': filename,
        'content': base64.b64encode(file_content).decode('utf-8'),
        'content_type': content_type,
        'size': uploaded_file.size
    }

def process_multiple_files(request_files_key, request, max_size_mb=25):
    """
    Обрабатывает multiple файлы из request.FILES
    """
    attachments = []
    
    if request_files_key in request.FILES:
        uploaded_files = request.FILES.getlist(request_files_key)
        
        for uploaded_file in uploaded_files:
            try:
                file_data = process_uploaded_file(uploaded_file, max_size_mb)
                attachments.append(file_data)
            except Exception as e:
                # Логируем ошибку, но продолжаем обработку других файлов
                print(f"Ошибка обработки файла {uploaded_file.name}: {e}")
                continue
    
    return attachments