from django.http import JsonResponse
from .data_processing import process_uploaded_file

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file_obj = request.FILES['file']
        processed_data = process_uploaded_file(file_obj)
        return JsonResponse({'processed_data': processed_data}, status=200)
    else:
        return JsonResponse({'error': 'File not provided or invalid request'}, status=400)



import pandas as pd
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .data_processing import infer_and_convert_data_types
from .serializers import FileUploadSerializer
import logging

# Create a logger
logger = logging.getLogger(__name__)

class FileUploadAPIView(APIView):
     def get(self, request, format=None):
        # Perform any necessary operations to retrieve data
        # For example, you might retrieve data from a database
        # and serialize it before returning the response
        data = {'message': 'GET method is working'}
        return Response(data, status=status.HTTP_200_OK)
     def post(self, request, format=None):
        logger.info("Received file upload request.")

        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']

            # Check file extension and read data accordingly
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file, na_values=['Not Available'])
                elif file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                    df = pd.read_excel(file)
                else:
                    return Response({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)

                # Handle NaN values
                df.replace([np.inf, -np.inf], np.nan, inplace=True)
                df.fillna(0, inplace=True)

                # Infer and convert data types
                processed_df = infer_and_convert_data_types(df)

                # Replace NaN with None
                processed_df = processed_df.where(pd.notnull(processed_df), None)

                # Log the DataFrame
                logger.info("Processed DataFrame:")
                logger.info(processed_df)

                # Convert DataFrame to dictionary for JSON response
                processed_data_dict = processed_df.to_dict(orient='records')

                return Response({'message': 'Data processed successfully', 'processed-data': processed_data_dict}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error("Error processing file: %s", str(e))
                return Response({'error': 'Error processing file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error("Serializer is not valid: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)