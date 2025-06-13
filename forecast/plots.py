import matplotlib.pyplot as plt
import io
import base64

def plot_forecast(results):
    plt.figure(figsize=(8, 4))
    plt.plot(results['Week'], results['Actual'], label='Actual', marker='o')
    plt.plot(results['Week'], results['Predicted'], label='Predicted', marker='x')
    plt.title("Forecast: Actual vs Predicted")
    plt.xlabel("Week")
    plt.ylabel("Quantity Used")
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    return base64.b64encode(image_png).decode('utf-8')
