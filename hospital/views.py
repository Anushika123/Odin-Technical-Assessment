from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .forms import FileUploadForm
from .forecaster import HospitalDemandForecaster
import os

# View to handle file upload and forecasting
def upload_file(request):
    if request.method == 'POST':
        # Check if a file was uploaded
        if not request.FILES.get('file'):
            error_message = "No file uploaded. Please choose a file before submitting."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': error_message}, status=400)
            messages.error(request, error_message)
            return render(request, 'hospital/upload.html', {'form': FileUploadForm()})

        # Save uploaded file to media directory
        file = request.FILES['file']
        file_path = f'media/{file.name}'

        os.makedirs('media', exist_ok=True)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            # Run forecasting on the uploaded file
            forecaster = HospitalDemandForecaster(file_path)
            results = forecaster.run_forecasting()

            # Prepare combined chart data for all items
            combined_chart = {
                'labels': [],
                'datasets': []
            }

            for item_code, result in results.items():
                # Create forecast table (week, actual, predicted)
                result['forecast_table'] = list(zip(result['weeks'], result['actual'], result['rf_pred']))

                # Initialize chart labels only once
                if not combined_chart['labels']:
                    combined_chart['labels'] = result['weeks']

                # Add actual and predicted values to datasets for chart
                combined_chart['datasets'].append({
                    'label': f"{item_code} (Actual)",
                    'data': result['actual'],
                    'borderColor': 'rgba(75, 192, 192, 0.5)',
                    'tension': 0.1
                })
                combined_chart['datasets'].append({
                    'label': f"{item_code} (RF)",
                    'data': result['rf_pred'],
                    'borderColor': 'rgba(255, 99, 132, 0.5)',
                    'tension': 0.1
                })

            # Store results and chart data in session for later retrieval
            request.session['results'] = results
            request.session['combined_chart'] = combined_chart

            # Return JSON response for AJAX requests
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'redirect_url': '/results/'})

            # Render results page
            return render(request, 'hospital/results.html', {
                'results': results,
                'combined_chart': combined_chart
            })

        # Handle file-specific errors (e.g. format issues)
        except ValueError as ve:
            error_message = str(ve)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': error_message}, status=400)
            messages.error(request, error_message)
            return render(request, 'hospital/upload.html', {'form': FileUploadForm()})

        # Handle any unexpected errors
        except Exception as e:
            error_message = "Something went wrong while processing the file."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': error_message}, status=500)
            messages.error(request, error_message)
            return render(request, 'hospital/upload.html', {'form': FileUploadForm()})

    # Render upload form for GET requests or fallback
    return render(request, 'hospital/upload.html', {'form': FileUploadForm()})


# View to show previously processed results
def show_results(request):
    results = request.session.get('results')
    combined_chart = request.session.get('combined_chart')

    if not results or not combined_chart:
        messages.error(request, "No results available. Please upload a file first.")
        return render(request, 'hospital/upload.html', {'form': FileUploadForm()})

    return render(request, 'hospital/results.html', {
        'results': results,
        'combined_chart': combined_chart
    })
