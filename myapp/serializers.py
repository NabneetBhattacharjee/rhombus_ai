from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate(self, data):
        file_obj = data.get('file') 
        if not file_obj:
            raise serializers.ValidationError("No file was submitted.")
        max_size = 20 * 1024 * 1024
        if file_obj.size > max_size:
            raise serializers.ValidationError("File size exceeds the limit")
        allowed_types = ['text/csv', 'application/vnd.ms-excel']
        if file_obj.content_type not in allowed_types:
            raise serializers.ValidationError("Unsupported file type. Please upload a CSV or Excel file.")
        
        # Return only the validated file object
        return {'file': file_obj}